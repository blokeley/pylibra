=====================
pylibra documentation
=====================

:Author: Tom Oakley
:Copyright: Copyright (c) 2008, 2009, 2010  Tom Oakley.

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

.. _create a new ticket: http://trac-hg.assembla.com/pylibra/newticket


Windows
-------

Installation
~~~~~~~~~~~~

#. Download the Windows executable (-win32.zip) from
   http://www.assembla.com/spaces/pylibra/documents
#. Unzip the ZIP archive to wherever you want it.

Use
~~~

1. Edit the libra.cfg file to set the correct serial settings and column
   headings for your data. The regular expression line ("regex") defines how
   pylibra searches serial data for the data you want. See
   http://docs.python.org/library/re.html for details on regular expression formats.
2. For the graphical user interface, run ``pylibragui.exe``
3. For the command line interface, open a command prompt window 
   (``cmd.exe``), then use `cd` to change directory to where pylibra is and 
   run `pylibra.exe`

Linux, OS X etc.
----------------

Installation
~~~~~~~~~~~~

1. Install pyserial. For example, on ubuntu open a terminal and type
   ``apt-get install pyserial``

2. Then either:

   * (Users) Copy the relevant (-src.zip) file from
     http://www.assembla.com/spaces/pylibra/documents; or
   * (Developers) Use the mercurial command
     ``hg clone http://hg.assembla.com/pylibra``

Use
~~~

Open a shell terminal and type ``python pylibra.py``



Developer instructions
======================

Tools
-----
To develop pylibra you need a python interpreter and a couple
of libraries:

* Python_ 2.6+ interpreter. Note that 3.0+ will not work.
* pySerial_ serial port library.
* py2exe_ to create the Windows executable. At the time of writing, trying to
  `easy_install py2exe` does not work!
* wxPython_ for the GUI. Note that `easy_install wxpython` does not work!
  See
  http://stackoverflow.com/questions/477573/easyinstall-of-wxpython-has-setup-script-error
* A good text editor.
  
.. links..
.. _Python: http://www.python.org/
.. _pySerial: http://pyserial.wiki.sourceforge.net/pySerial
.. _py2exe: http://www.py2exe.org/
.. _wxPython: http://www.wxpython.org/
.. _docutils: http://docutils.sourceforge.net/docs/

Recommended workflow
--------------------

1. Choose a ticket to address from http://trac-hg.assembla.com/pylibra/report/1
2. Update your copy of the source using ``hg update``.
3. If at all possible, write a unit test or tests to expose the problem.
4. Solve the problem.
5. If you want to build a Windows executable, open a terminal and run
   ``python setup.py py2exe``.
6. Test as much as possible.
7. Update the documentation (see below) if you make any changes noticeable to the user.
8. Commit using ``hg commit -m`` with a helpful commit message, preferably
   referencing the ticket with ``ticket:xx`` where xx is the ticket number.
9. Create a changegroup file using ``hg bundle --base BASE`` where BASE is the
   last revision you got from the online repository (the last before your
   changes).
10. Upload the changegroup file to the ticket and update the ticket.

Documentation process
---------------------

1. Update all files under the ``doc`` directory of the source.
2. Create HTML files and PDFs as necessary. If you have installed docutils 
   (see below), use ``rst2html.py README.txt > README.html`` at the 
   command prompt.
   Alternatively, you can use the rst2a_ website to
   create both HTML and PDF files. Note that rst2a_ does not convert internal
   links properly in the HTML output.

.. _rst2a: http://rst2a.com/create/

Installing docutils (on Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download docutils_.
2. Make sure that ``C:\Python26\Scripts`` is on your %PATH% environment
   variable.
