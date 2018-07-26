=========
pyPicoLCD
=========

A library to interact with the PicoLCD 256x64 from Mini-Box, written in Python

.. note:: If on Windows, you should download `libusb0`__ (`libusb1`__ does `not yet work`__), put ``libusb0.dll`` into ``%WINDIR%\System32``, put ``libusb0.sys`` into ``%WINDIR%\System32\Drivers``, and then assign libusb to the PicoLCD device via ``install-filter-win.exe``.

.. __: https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/
.. __: https://libusb.info/
.. __: https://github.com/pyusb/pyusb/issues/186#issuecomment-407926048
