#!/usr/bin/env python
#
# Copyright 2008 Tom Oakley
# This file is part of pylibra.
#
# pylibra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylibra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibra.  If not, see http://www.gnu.org/licenses/.
#
# Style note: this module deviates from http://www.python.org/dev/peps/pep-0008/
# because wxPython uses Microsoft C++ styles and we have to override some
# wxPython methods.
#
# FIXME: Make Grid fill available area. Test with long strings.
# TODO: Check unit tests work
# TODO: Make parser start on different thread from GUI
# TODO: Check pylibra command line still works
# TODO: Add decent help support
# TODO: Release as v0.4

"""Graphical user interface for pylibra."""

import logging
import logging.config
import webbrowser
import os
import sys
import traceback
import wx
import wx.grid

import libra

_RESOLUTION_VGA = (640, 480)
_URL_HELP = 'http://trac-hg.assembla.com/pylibra/wiki/UserInstructions'
_EXCEPTION_MSG = '''An error occurred. This is normally a problem with
configuration, connection to peripherals, or bad input data.
'''
_QUIT_MSG = 'Do you want to quit?'


class App(wx.App):
    
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        # Read or create the model (table)
        # TODO: Read columns from config file
        logging.config.fileConfig('logging.cfg')

        # Backup the old data file if it exists
        outfile = 'data.csv'
        if os.path.isfile(outfile):
            backup = outfile[:-4] + '.bak'
            if os.path.isfile(backup): os.remove(backup)
            os.rename(outfile, backup)

        # Get column headings
        columns = libra.getColumns()
        if columns: libra.writetofile(outfile, (columns,))
 
        # Set up the serial port reader
        controller = libra.Libra(outfile)
        self.table = Table(columns)
        controller.datacallbacks.append(self.table.DataReceived)

        self.frame = Frame(None, 'pylibra', self.table, controller)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True # No errors during init

    def OnExit(self):
        """Clear up (close any db connections etc.).

        Called after last top-leve frame is closed.

        """
        # Placeholder for later code

    def ExceptHook(self, type, value, tb):
        """Display any uncaught exception in a dialog box."""
        _LOGGER = logging.getLogger('App.ExceptHook')
        _LOGGER.error(value)

        msg = '%s\n%s\n\n%s' % (_EXCEPTION_MSG, value, _QUIT_MSG)
        dlg = wx.MessageDialog(self.frame, msg, 'Error', wx.YES_NO | wx.ICON_ERROR)
        returnCode = dlg.ShowModal()
        dlg.Destroy()
        
        if returnCode == wx.ID_YES:
            wx.Exit()


class Frame(wx.Frame):
    """The application's main frame (window)."""
    
    def __init__(self, parent, title, table, controller):
        wx.Frame.__init__(self, parent, title=title, size=(_RESOLUTION_VGA))
        
        self.statusbar = self.CreateStatusBar()
        self.SetIcon(wx.Icon('../resources/dot.ico', wx.BITMAP_TYPE_ICO))

        self.controller = controller

        # Add the main panel
        self.panel = wx.Panel(self)
        self.startbutton = wx.Button(self.panel, label='Start')
        self.Bind(wx.EVT_BUTTON, self.StartButtonClick, self.startbutton)

        self.stopbutton = wx.Button(self.panel, label='Stop')
        self.Bind(wx.EVT_BUTTON, self.StopButtonClick, self.stopbutton)

        self.helpbutton = wx.Button(self.panel, label='Help')
        self.Bind(wx.EVT_BUTTON, self.HelpButtonClick, self.helpbutton)

        self.table = table
        self.grid = Grid(self.panel, self.table)
        self.table.AddObserver(self.grid)

        # Layout
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer.Add(self.startbutton)
        buttonsizer.Add(self.stopbutton)
        buttonsizer.Add(self.helpbutton)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(buttonsizer)
        mainsizer.Add(self.grid, wx.EXPAND)
        self.panel.SetSizer(mainsizer)

        self.Reading = False

    def StartButtonClick(self, evt):
        self.controller.startParser()
        self.Reading = True

    def StopButtonClick(self, evt):
        self.controller.stopParser()
        self.Reading = False

    def HelpButtonClick(self, evt):
        webbrowser.open_new_tab(_URL_HELP)

    def OnAbout(self, evt):
        wx.MessageBox('pylibra serial port reader', 'About pylibra',
                    wx.OK | wx.ICON_INFORMATION, self)

    def OnExit(self, evt):
        self.Close()

    def _SetReading(self, b):
        """Sets whether the serial reading is active."""
        if b:
            self.reading = True
            self.startbutton.Enable(False)
            self.stopbutton.Enable(True)
        else:
            self.reading = False
            self.startbutton.Enable(True)
            self.stopbutton.Enable(False)

    def _IsReading(self):
        """Whether the app is reading the serial port."""
        return self.reading

    Reading = property(_IsReading, _SetReading)


class Table(wx.grid.PyGridTableBase):
    """Table model of data."""

    def __init__(self, columns):
        wx.grid.PyGridTableBase.__init__(self)
        self.columns = columns
        
        # A list of observers (such as grids) to refresh after data changes
        self.views = []
        self.data = []

    def AddObserver(self, observer):
        # TODO: Change self.views to a set and remove if statement
        if observer not in self.views:
            self.views.append(observer)

    def RemoveObserver(self, observer):
        try:
            self.views.remove(observer)
        except ValueError:
            pass

    def GetNumberRows(self):
        numrows = len(self.data)
        return numrows

    def GetNumberCols(self):
        return len(self.columns)

    def GetColLabelValue(self, col):
        return self.columns[col]

    def GetRowLabelValue(self, row):
        return row

    def IsEmptyCell(self, row, col):
        return self.data[row][col] is not None

    def GetValue(self, row, col):
        value = self.data[row][col]
        if value is None:
            return ''
        else:
            return value

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def DataReceived(self, data):
        """Add new data to the table.

        data -- a list of lists containing strings of data
        
        """
        for row in data:
            self.data.append(row)

        msg = wx.grid.GridTableMessage(self,
            wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, len(data))

        # Refresh any views such as grids
        for view in self.views:
            view.ProcessTableMessage(msg)
            #view.ForceRefresh()


class Grid(wx.grid.Grid):
    """Graphical widget showing the table.

    See Table for table model logic.
    
    """
    def __init__(self, parent, table):
        wx.grid.Grid.__init__(self, parent)
        self.SetTable(table)
        self.EnableEditing(False)


if __name__ == "__main__":
    app = App()
    # Set up the exception handler
    sys.excepthook = app.ExceptHook
    app.MainLoop()
