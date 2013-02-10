=====================
pylibra documentation
=====================

:Author: Tom Oakley
:Copyright: Copyright (c) 2008 - 2013 Tom Oakley.

..
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the file "COPYING_DOCS".
    
    This document is written in the reStructuredText format.
    Please abide by the format conventions when editing.
..

``pylibra`` is an application to read data from a serial port, parse it
into useful chunks, and write the data to a file.

User instructions
=================

Support
-------
If you notice any problems, please `create a new ticket`_.

.. _create a new ticket: https://github.com/blokeley/pylibra/issues/new


Windows
-------

Installation
~~~~~~~~~~~~

#. Download the Windows executable (-win32.zip) from
   https://docs.google.com/file/d/0Bzv_VsGhPlilOWxyWWxZeW43YkE/edit?usp=sharing 
   Ensure you download the entire ZIP archive, not individual files. To do this 
   from Google Drive, select `File > Download`.
#. Unzip the ZIP archive to wherever you want it.
#. Note that, for legal licensing reasons, you may have to install 
   a file called MSVCP90.dll which can be downloaded from 
   http://www.microsoft.com/downloads/en/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en

Use
~~~

1. edit the libra.cfg file to set the correct serial settings and column
   headings for your data. the regular expression line ("regex") defines how
   pylibra searches serial data for the data you want. see
   http://docs.python.org/library/re.html for details on regular expression formats.
2. for the graphical user interface, run ``pylibragui.exe``
3. for the command line interface, open a command prompt window 
   (``cmd.exe``), then use `cd` to change directory to where pylibra is and 
   run `pylibra.exe`
4. select `start` to start polling the serial port for data. data are 
   automatically saved in a file called `data.csv` in the current working directory.

linux, os x etc.
----------------

installation
~~~~~~~~~~~~

1. install pyserial. for example, on ubuntu or debian open a terminal as root 
   and type ``apt-get install pyserial``
2. run `git clone https://github.com/blokeley/pylibra.git`

use
~~~

To run the command line interface, open a shell terminal, `cd` to the 
directory containing pylibra and type ``python pylibra.py``

To run the graphical user interface, either double-click on `pylibragui.py` 
in a graphical file manager, or open a shell terminal, `cd` to the 
directory containing pylibra and type ``python pylibragui.py``

Developer instructions
======================

Tools
-----
To develop pylibra you need a python interpreter and a couple
of libraries. If you are using Windows, use the Windows installers for 
pyserial, py2exe and wxPython rather than setuptools/easy_install.

* Python_ 2.6+ interpreter. Note that 3.0+ has not been tested and probably will not work.
* pySerial_ serial port library. Install pyserial using the Windows executable 
  rather than easy_install so that py2exe can find the serial package.
* py2exe_ to create the Windows executable.
* wxPython_ for the GUI.
* A good text editor.
  
.. links..
.. _Python: http://www.python.org/
.. _pySerial: http://pyserial.wiki.sourceforge.net/pySerial
.. _py2exe: http://www.py2exe.org/
.. _wxPython: http://www.wxpython.org/
.. _docutils: http://docutils.sourceforge.net/docs/

Recommended work flow
---------------------

1. Choose a ticket to address from https://github.com/blokeley/pylibra/issues
2. Make a server-side clone on `github`
3. Clone from your server-side repo using `git clone https://github.com/USER/pylibra.git` 
   where USER is your user name
4. If at all possible, write a unit test or tests to expose the problem.
5. Create a feature branch on your local repo using `git checkout -n BRANCHNAME` 
6. Solve the problem.
7. If you want to build a Windows executable, open a terminal and run
   ``python setup.py py2exe``.
8. Test as much as possible.
9. Update the documentation if you make any changes noticeable to the user.
10. Commit using ``git commit -m`` with a helpful commit message, preferably
    referencing the ticket with ``#xx`` where xx is the ticket number.
11. Push your changes to your server-side repo using `git push`
12. Create a `pull request <https://help.github.com/articles/using-pull-requests>`_ on `github`.

Installing docutils (on Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download docutils_.
2. Make sure that ``C:\Python26\Scripts`` is on your ``PATH`` environment
   variable.
