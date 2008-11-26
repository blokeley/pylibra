===================
Libra documentation
===================
:Author: Tom Oakley
:Copyright: Copyright (c)  2008  Tom Oakley.

..
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the file "COPYING_DOCS".
    
    This document is written in the reStructuredText format.
    Please abide by the format conventions when editing.
..

Libra is an application to read data from a serial port, parse it 
into useful chunks, and write the data to a file. The original version 
was in Java but this port was written in Python to reduce development 
time, and for fun!

User instructions
=================
To install libra, simply copy the Python (.py) source files to a directory on your 
favourite drive.

To run libra, type ``python textui.py`` or ``python wxui.py`` for a 
text-based user interface or graphical user interface respectively.

Developer instructions
======================
Tools
-----
To develop Libra you simply need a python interpreter and a couple 
of libraries:

* Python interpreter. For example, `Python 2.5+`__.

* `pySerial`__ serial port library.

* `py2exe`__ to create the Windows executable.

* A good text editor. I use `eclipse 3.4`__ with `pyDev`__, or the excellent 
  `jEdit`__. Note that jEdit has a syntax highlighting  mode for reStructuredText.

__ http://www.python.org/
__ http://pyserial.wiki.sourceforge.net/pySerial
__ http://www.py2exe.org/
__ http://www.eclipse.org/
__ http://pydev.sourceforge.net/
__ http://www.jedit.org/

Building
~~~~~~~~
To build documentation (on debian-based machines with docutils installed) use 
``rst-buildhtml doc``

Building the Windows exectuble has not been implemented at the time of writing.

Support
-------
You might have some joy going to `the project page`__  and filing a bug on trac.

__ http://trac-hg.assembla.com/pylibra

