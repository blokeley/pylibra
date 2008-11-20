..
    Copyright (c)  2008  Tom Oakley.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the file "COPYING_DOCS".
..

Libra documentation
===================
Libra is an application to read data from a serial port, parse it 
into useful chunks, and write the data to a file. The original version 
was in Java but this port was written in Python to reduce development 
time, and for fun!

User instructions
-----------------
To install libra, simply copy the source files to a directory on your 
favourite drive.

To run libra, type ``python textui.py`` or ``python wxui.py`` for a 
text-based user interface or graphical user interface respectively.

Developer instructions
----------------------
Tools
~~~~~
To develop Libra you simply need a python interpreter and a couple 
of libraries:

* Python interpreter. For example, `Python 2.5+ <http://www.python.org/>`_

* `pySerial <http://pyserial.wiki.sourceforge.net/pySerial>`_ serial port library.

* `py2exe <http://www.py2exe.org/>`_ to create the Windows executable.

* A good text editor. I use `eclipse 3.4 <http://www.eclipse.org/>`_ 
  with `pyDev <http://pydev.sourceforge.net/download.html>`_, or the excellent 
  `jEdit <http://www.jedit.org/>`_.

Building
~~~~~~~~
To build documentation (on debian-based machines with docutils installed) use 
``rst-buildhtml libra/doc``

Building the Windows exectuble has not been implemented at the time of writing.

Support
-------
You might have some joy going to `the project page <http://www.assembla.com/>`_ 
and filing a bug on trac.

