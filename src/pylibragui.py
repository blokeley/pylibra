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
# Style note: some methods in this module deviate from
# http://www.python.org/dev/peps/pep-0008/
# because wxPython uses Microsoft C++ styles and we have to override some
# wxPython methods.
#
# FIXME: Make Grid fill available area. Test with long strings.

"""Graphical user interface for pylibra."""

import logging
import logging.config
import webbrowser
import os
import sys
import traceback
import wx
import wx.grid

import core

_RESOLUTION_VGA = (640, 480)
_URL_HELP = 'http://trac-hg.assembla.com/pylibra/wiki/UserInstructions'
_EXCEPTION_MSG = '''An error occurred. This is normally a problem with
configuration, connection to peripherals, or bad input data.
'''
_QUIT_MSG = 'Do you want to quit?'


class App(wx.App):
    
    def __init__(self):
        wx.App.__init__(self, redirect=False)
        # Set up the exception handler
        sys.excepthook = self.except_hook

    def OnInit(self):
        """Override `wx.App.OnInit()`."""
        # Read or create the model (table)
        # TODO: Read columns from config file
        logging.config.fileConfig('logging.cfg')

        # Backup the old data file if it exists
        outfile = 'data.csv'
        if os.path.isfile(outfile):
            backup = outfile[:-4] + '.bak'
            if os.path.isfile(backup):
                os.remove(backup)
            os.rename(outfile, backup)

        # Get column headings
        columns = core.get_columns()
        if columns:
            core.write_to_file(outfile, (columns,))
 
        # Set up the serial port reader
        controller = core.DataManager(outfile)
        self.table = Table(columns)
        controller.datacallbacks.append(self.table.data_received)

        self.frame = Frame(None, 'pylibra', self.table, controller)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True # No errors during init

    def OnExit(self):
        """Clear up (close any db connections etc.).

        Called after last top-leve frame is closed.
        Overrides `wx.App.OnExit()`.
        """
        _LOGGER = logging.getLogger('App.OnExit')
        _LOGGER.info('Exit OK')

    def except_hook(self, type, value, tb):
        """Display any uncaught exception in a dialog box."""
        _LOGGER = logging.getLogger('App.ExceptHook')
        _LOGGER.error(''.join(traceback.format_exception(type, value, tb)))

        msg = '%s\n%s\n\n%s' % (_EXCEPTION_MSG, value, _QUIT_MSG)
        dlg = wx.MessageDialog(self.frame, msg, 'Error', wx.YES_NO | wx.ICON_ERROR)
        returnCode = dlg.ShowModal()
        dlg.Destroy()
        
        if returnCode == wx.ID_YES:
            wx.Exit()


class Frame(wx.Frame):
    """The application's main frame (window)."""
    
    def __init__(self, parent, title, table, controller):
        """Override `wx.Frame.__init__()`."""
        wx.Frame.__init__(self, parent, title=title, size=(_RESOLUTION_VGA))
        
        self.statusbar = self.CreateStatusBar()
        self.SetIcon(wx.Icon('resources/dot.ico', wx.BITMAP_TYPE_ICO))

        self.controller = controller

        # Add the main panel
        self.panel = wx.Panel(self)
        self.startbutton = wx.Button(self.panel, label='Start')
        self.Bind(wx.EVT_BUTTON, self.start_button_click, self.startbutton)

        self.stopbutton = wx.Button(self.panel, label='Stop')
        self.Bind(wx.EVT_BUTTON, self.stop_button_click, self.stopbutton)

        self.helpbutton = wx.Button(self.panel, label='Help')
        self.Bind(wx.EVT_BUTTON, self.help_button_click, self.helpbutton)

        self.table = table
        self.grid = Grid(self.panel, self.table)
        self.table.add_observer(self.grid)

        # Layout
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer.Add(self.startbutton)
        buttonsizer.Add(self.stopbutton)
        buttonsizer.Add(self.helpbutton)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(buttonsizer)
        mainsizer.Add(self.grid, flag=wx.EXPAND)
        self.panel.SetSizer(mainsizer)

        self._reading = False

    def start_button_click(self, evt):
        self.controller.start_parser()
        self.Reading = True

    def stop_button_click(self, evt):
        self.controller.stop_parser()
        self.Reading = False

    def help_button_click(self, evt):
        webbrowser.open_new_tab(_URL_HELP)

    def OnAbout(self, evt):
        wx.MessageBox('pylibra serial port reader', 'About pylibra',
                    wx.OK | wx.ICON_INFORMATION, self)

    def OnExit(self, evt):
        """Override `wx.Frame.OnExit()`."""
        self.Close()

    @property
    def reading(self):
        """Whether the app is reading the serial port."""
        return self._reading

    @reading.setter
    def reading(self, b):
        """Sets whether the serial reading is active."""
        if b:
            self._reading = True
            self.startbutton.Enable(False)
            self.stopbutton.Enable(True)
        else:
            self._reading = False
            self.startbutton.Enable(True)
            self.stopbutton.Enable(False)


class Table(wx.grid.PyGridTableBase):
    """Table model of data."""

    def __init__(self, columns):
        wx.grid.PyGridTableBase.__init__(self)
        self.columns = columns
        
        # A list of observers (such as grids) to refresh after data changes
        self.views = set()
        # A list of lists holding the data
        self.data = []

    def add_observer(self, observer):
        self.views.add(observer)

    def remove_observer(self, observer):
        try:
            self.views.remove(observer)
        except KeyError:
            pass

    def GetNumberRows(self):
        """Override `wx.grid.PyGridTableBase.GetNumberRows()`."""
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

    def data_received(self, data):
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
        """Override `wx.grid.Grid.__init__()`."""
        wx.grid.Grid.__init__(self, parent)
        self.SetTable(table)
        self.EnableEditing(False)


if __name__ == "__main__":
    app = App()
    app.MainLoop()
