======
pyTUIO
======

A Python library that understands the TUIO protocol.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This library is able to receive and parse data following the `TUIO protocol`_,
which was specially designed for transmitting the state of tangible objects and multi-touch control on a table surface.

Installation
============

In order to use this library you need to have the cross-plattform  
reacTIVision_ application that does the heavy lifting of tracking the tangible 
objects, so-called fiducials_. It transmits the received data (e.g. positional 
information) as OSC_ messages via an UDP socket to your client software which
uses this library.

If you haven't downloaded a copy of django-registration already,
you'll need to do so. You can download a packaged version of the
latest release here::

    http://pytuio.googlecode.com/files/pytuio-0.1.tar.gz

Open up the package (on most operating systems you can double-click, or you
can use the command ``tar zxvf pytuio-0.1.tar.gz`` to manually unpack it), 
and, at a command line, navigate to the directory ``pytuio-0.1``, then type::

    python setup.py install

This will install pytuio into a directory on your Python import path. For 
system-wide installation on Linux/Unix and Mac OS, you can use ``sudo``::

    sudo python setup.py install

Alternatively, you can do a Subversion checkout to get the latest
development code (though this may also include bugs which have not yet
been fixed)::

    svn co http://pytuio.googlecode.com/svn/trunk/tuio/

For best results, do that in a directory that's on your Python import
path.

If you prefer you can also simply place the included ``tuio`` directory 
somewhere on your Python path, or symlink to it from somewhere on your Python 
path; this is useful if you're working from a Subversion checkout.

If you plan to use this library together with Nodebox.app please copy the 
``tuio`` directory to ``~/Library/Applications Support/Nodebox/`` to enable
Nodebox to find it.

.. _TUIO protocol: http://modin.yuri.at/publications/tuio_gw2005.pdf
.. _reacTIVision: http://reactable.iua.upf.edu/?software
.. _fiducials: http://reactable.iua.upf.edu/pdfs/fiducials.pdf
.. _OSC: http://en.wikipedia.org/wiki/OpenSound_Control

Basic use
=========

To use this library in general you should follow these steps:

#. Get a camera or webcam, like iSight, Quickcam, etc., install its drivers if 
   necessary, try it with the reacTIVision_ software
#. Look in the ``examples`` directory to get started with Python code. Ask 
   your local Python guru if needed.
#. Build the tangible interface, table, stage, vehicle, game, whatever.
#. Combine it with Blender_, Pygame_ or Nodebox_
#. Use the source, Luke.

.. _Blender: http://blender.org 
.. _Pygame: http://pygame.org
.. _Nodebox: http://nodebox.net

What is in the library
======================

The library consists of several parts and submodules:

    * Tracking_
    * Objects_
    * Profiles_
    * OSC_

Tracking
--------

The ``Tracking`` class should be used to initialize a socket connection for
receiving the OSC messages from reacTIVision_. It handles all incoming data
and calls the appropriate functions, depending on the type of message.

When started it loads every possible profile from the ``profiles`` submodule
and initializes a callback manager from the ``OSC`` module.

A simple example can be found in the ``examples`` directory in 
``example1.py``:

1. Import it::

    import tuio

2. Initializes the receiving of tracking data::

    tracking = tuio.Tracking()

3. Print all TUIO profiles that have been found and loaded::

    print "loaded profiles:", tracking.profiles.keys()

4. Print available helper functions, that can be used to access the objects of
   each loaded profile::
   
    print "list functions to access tracked objects:", tracking.get_helpers()

5. Prepare to receive the data in an infinite loop::

    try:
        while 1:
            tracking.update()
            for obj in tracking.objects():
                print obj
    except KeyboardInterrupt:
        tracking.stop()

  a) You need to update the tracking information on each loop manually.

  b) Access the tracked objects by using one of the helper function that 
     return a list of these objects.

  c) Stop the tracking manually on every exception to prevent socket 
     errors

Objects
-------

Profiles
--------

OSC
---


