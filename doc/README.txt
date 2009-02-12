=====================
pylibra documentation
=====================

:Author: Tom Oakley
:Copyright: Copyright (c) 2008, 2009  Tom Oakley.

..
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the file "COPYING_DOCS".
    
    This document is written in the reStructuredText format.
    Please abide by the format conventions when editing.
..

pylibra is an application to read data from a serial port, parse it
into useful chunks, and write the data to a file. The original version 
was in Java but this port was written in Python to reduce development 
time, and for fun!

User instructions
=================

Windows
-------

#. Download the Windows executable (-win32.zip) from
   http://www.assembla.com/spaces/pylibra/documents
#. Unzip the ZIP archive to wherever you want it.

Linux, OS X etc.
----------------

1. Install pyserial. For example, on ubuntu open a terminal and type
   ``apt-get install pyserial``

2. Then either:

   * (Users) Copy the relevant (-src.zip) file from
     http://www.assembla.com/spaces/pylibra/documents; or
   * (Developers) Use the mercurial command
     ``hg clone http://hg.assembla.com/pylibra``

Running pylibra
---------------

1. Edit the libra.cfg file to set the correct serial settings and column
   headings for your data. The regular expression line ("regex") defines how
   pylibra searches serial data for the data you want. See
   http://docs.python.org/library/re.html for details on regular expression formats.
2. On Windows, double-click ``pylibra.exe``.
3. On other operating systems, open a shell terminal and type ``python pylibra.py``

Developer instructions
======================

Tools
-----
To develop Libra you simply need a python interpreter and a couple 
of libraries:

* Python_ 2.5.x interpreter. Note that 2.6 or 3.0 will not work.
* pySerial_ serial port library.
* py2exe_ to create the Windows executable.
* A good text editor. Note that jEdit has a syntax highlighting mode for
  reStructuredText.

.. links..
.. _Python: http://www.python.org/
.. _pySerial: http://pyserial.wiki.sourceforge.net/pySerial
.. _py2exe: http://www.py2exe.org/
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
7. Update the documentation_ if you make any changes noticeable to the user.
8. Commit using ``hg commit -m`` with a helpful commit message, preferably
   referencing the ticket with ``ticket:xx`` where xx is the ticket number.
9. Create a changegroup file using ``hg bundle --base BASE`` where BASE is the
   last revision you got from the online repository (the last before your
   changes).
10. Upload the changegroup file to the ticket and update the ticket.

Documentation
-------------

1. Update all files under the ``doc`` directory of the source.
2. Create HTML files and PDFs as necessary. You can use the rst2a_ website to
   create both HTML and PDF files. Note that rst2a_ does not convert internal
   links properly in the HTML output.

Alternatively, if you do not want to use rst2a_, do the following:

.. _rst2a: http://rst2a.com/create/

Windows
~~~~~~~
1. Download docutils_.
2. Make sure that ``C:\Python25\Tools\docutils`` is on your %PATH% environment
   variable.
3. Open a command prompt.
4. ``cd`` to the pylibra source doc directory.
5. Type ``buildhtml.py``.

Ubuntu linux
~~~~~~~~~~~~

1. Run ``apt-get install docutils``.
2. Open a terminal.
3. ``cd`` to the pylibra source doc directory.
4. Type ``rst-buildhtml``

Support
-------
Please `create a new ticket`_.

.. _create a new ticket: http://trac-hg.assembla.com/pylibra/newticket
