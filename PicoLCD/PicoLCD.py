import usb.core,usb.util
import time
import sys
import os.path
from psf import Psf
from random import randint
from PIL import Image
assert sys.version_info>=(3,),"Python2 not supported (yet?)"

picoLCD_VENDOR=0x04d8
picoLCD_DEVICE=0xc002

picoLCD_USB_IFACE=0
picoLCD_USB_ENDPOINT_OFFSET=1

OUT_REPORT_GPO			= 0x81

OUT_REPORT_LCD_BACKLIGHT	= 0x91
OUT_REPORT_LCD_CONTRAST		= 0x92
OUT_REPORT_INIT			= 0x93
OUT_REPORT_CMD			= 0x94
OUT_REPORT_DATA			= 0x95
OUT_REPORT_CMD_DATA		= 0x96

OUT_REPORT_WRITE		= 0x98

SCREEN_W,SCREEN_H		= 256,64

b = lambda o: bytes(o if hasattr(o,'__len__') else (o,))

class PicoLcd:
	def __init__(self, idProduct=picoLCD_DEVICE, idVendor=picoLCD_VENDOR, DEBUG=False):
		"""Templated vaguely off drv_pLG_open"""
		self._dev=usb.core.find(idVendor=idVendor, idProduct=idProduct)
		
		self.errors=[]
		try:
			self._dev.detach_kernel_driver(picoLCD_USB_IFACE)
		except usb.core.USBError as e:
			self.errors.append(e)
			if e.errno != 2:
				raise
		self._dev.set_configuration()
		time.sleep(0.0001)
		usb.util.claim_interface(self._dev,picoLCD_USB_IFACE)
		self._dev.set_interface_altsetting(picoLCD_USB_IFACE)
		self._DEBUG=DEBUG
	
#	def __del__(self):
#		"""Templated vaguely off drv_pLG_close"""
#		usb.util.release_interface(self._dev,picoLCD_USB_IFACE)
#		self._dev.reset() #Segfaults, but only if the script was exiting anyway
#	
	def _write(self, data):
		"""Write the data to the device
		
		Templated vaguely off drv_pLG_send
		
		TODO: document WHETHER this is blocking,
		 and add an option to do the other way
		"""
		if self._DEBUG:
			sys.stderr.buffer.write(data)
#			print(repr(data))
#			time.sleep(0.5)
		return self._dev.write(usb.util.ENDPOINT_OUT+picoLCD_USB_ENDPOINT_OFFSET, data)
	
	def _read(self, n=3, timeout=100):
		"""Read n bytes from the device
		
		Templated vaguely off drv_pLG_read
		
		TODO: document WHETHER this is blocking,
		 and add an option to do the other way
		"""
		return self._dev.read(usb.util.ENDPOINT_IN+picoLCD_USB_ENDPOINT_OFFSET, n, timeout)
	
	def _do(self, command, *payloads):
		return self._write(
		 bytes().join([
		  b(command),
		  *payloads
		 ])
		)
	def _out_report_init(self, *payloads):
		return self._do(OUT_REPORT_INIT,
		  *payloads
		)
	def _out_report_cmd(self, *payloads):
		return self._do(OUT_REPORT_CMD,
		  *payloads
		)
	def _out_report_data(self, *payloads):
		return self._do(OUT_REPORT_DATA,
		  *payloads
		)
	def _out_report_cmd_data(self, *payloads):
		return self._do(OUT_REPORT_CMD_DATA,
		  *payloads
		)
	
	def set_backlight(self, brightness):
		"""Set the backlight to "brightness".
		
		* min:0 (backlight fully OFF)
		* max:255
		* 1 through 14 are the same as 0
		* Every single brightness level from 15
		  through about 24 is HIGHLY noticeable
		* 127 is not much different from 255
		
		Templated vaguely off drv_pLG_backlight
		"""
		if brightness<15 and brightness!=0:
			pass#TODO: warn?
		return self._do(OUT_REPORT_LCD_BACKLIGHT,
		 b(brightness)
		)
	
	def set_contrast(self, contrast):
		"""Templated vaguely off drv_pLG_contrast"""#TODO: physical errata
		return self._do(OUT_REPORT_LCD_CONTRAST,
		  b(contrast)
		)
	
	def _cmd1(self):
		"""cmd[3] from drv_pLG_clear, SEEMS TO do the following:
		
		Visually immediately blanks the entire screen. Pixels
		 [can PRESUMABLY be written during this time, but]
		 will not be displayed until re-enabled via OUT_REPORT_CMD.
		"""
		return self._out_report_init(b'\x01\x00')
	
	def _cmd2(self, i, i_op=(lambda i: i<<2)):
		"""cmd2[9] from drv_pLG_clear, SEEMS TO do the following:
		
		Given an integer i in range(4),
		
		Undo the effects of clear() on the (zero-indexed) "i"th
		 quadrant of the screen, revealing the "underlying" image
		 that was present before the clear(), and re-enabling
		 that quadrant's image-display functionality.
		"""
		return self._out_report_cmd(
		  b(i_op(i)),
		  b'\x02\x00\x64\x3F\x00\x64\xC0'
		)
	
	def _cmd3(self, chipsel, line, data, line_op=(lambda line: line|0b10111000)):
		"""cmd3[64] from drv_pLG_update_img and drv_pLG_clear
		
		Considering the screen as an 8x8 grid of 32px-by-8px "chunks",
		 write up to one chunk of data to the screen.
		
		When chipsel is even (i.e., chipsel&0x01 == 0):
		
			Beginning at the left boundary of
			 the chunk which is
			 (zero-indexedly speaking,)
			 the Xth from the left, and
			 the Yth from the top, where
			 X=(chipsel&~2)>>1 and
			 Y=line,
			
			Write the data to the screen,
			 beginning with the first byte,
			 filling the columns left-to-right,
			 one byte per 1x8 column,
			 the low~high bits becoming
			 the top~bottom pixels
			 (respectively)
		
		When chipsel is odd (i.e., chipsel&0x01 == 1):
			
			This functions [exactly?] like cmd4,
			 with one quirk:
			
			It seems to forcibly prepend the data with
			 vaguely the right half of a downward-facing arrow
			 comprising two bytes.
			The length of the stem has a [TODO] connection
			 with the value of line.
			
			The value of line does not affect the row; just
			 the shape of the arrow.
		"""
		
		assert len(data)<=32 or self._DEBUG
		
		return self._out_report_cmd_data(
		  b(chipsel),
		  b'\x02\x00\x00',
		  b(line_op(line)), #TODO: fuzz testing or something (priority: range(8) and range(64,64+8))
		  b'\x00\x00\x40\x00\x00',
		  b(len(data)),
		  data
		)
	
	def _cmd4(self, chipsel, data, chipsel_op=(lambda chipsel: chipsel|0b1)):
		"""cmd4 from drv_pLG_update_img and drv_pLG_clear
		
		Cannibalized "magic" code, still testing
		
		TODO: description
		"""
		return self._out_report_data(
		  b(chipsel_op(chipsel)), #TODO: fuzz testing or something
		  b'\x00\x00',
		  b(len(data)),
		  data
		)
	
	def _drv_pLG_clear(self):
		"""Legacy "clear" command from drv_picoLCDGraphic.c
		 SVN rev1204, line 340
		 https://lcd4linux.bulix.org/browser/trunk/drv_picoLCDGraphic.c?rev=1204#L340
		
		All 4 of the cmd* variables were initially
		 modularized/cannibalized from this function.
		
		Kept around mainly for interest, since it looks
		 like it has very few secrets left to yield.
		"""
		self._cmd1()
		
		for i in range(4):
			self._cmd2(i)
		
		data=bytes(32)#b'\x00'*32
		for cs in range(0,4):
			for line in range(8):
				
				self._cmd3(chipsel=cs*4, line=line, data=data)
				
				self._cmd4(chipsel=cs*4, data=data)
	
	def put_block(self, col, row, data):
		"""ALPHA-QUALITY function to draw pixels to the screen"""
		if col&0b1:
			raise NotImplementedError
		if type(data) is str:
			data=_f68enc(data)
		if len(data)<=32:
			return self._cmd3((col<<1)&~0b10, row, data)
		else:
			assert len(data)<=64
			return self._cmd3((col<<1)&~0b10, row, data[:32]) \
			     + self._cmd4((col<<1)&~0b10, data[32:])

_Font_6x8=Psf(os.path.join(os.path.dirname(__file__),'Font_6x8.psf'))
_Font_6x8.glyphs = [
	Image.frombytes(
	 '1',_Font_6x8.size,glyph
	).transpose(Image.ROTATE_270).tobytes()
	for glyph in _Font_6x8.glyphs
]

def _f68enc(s, font=_Font_6x8):
	if type(s) is str:
		s=s.encode('ibm437')
	if type(s) is int:
		s=bytes((s,))
	#TODO char-glyph mappings whatever whatever
	# probably pypsf's job
	return bytes().join(
		font.glyphs[c]
		for c in s
	)

if __name__ == "__main__":
	from datetime import datetime
	p = PicoLcd(DEBUG=True)
	p._drv_pLG_clear()
	for i in [0,0,
	  *range(15,24,1),
	  *range(24,30,2),
	  *range(30,38,4),
	  *range(38,64,8),
	  *range(64,128,16),
	  *range(128,256,32),
	  255,255>>1
	]:
		p.set_backlight(i)
		if not randint(0,3):
			p._cmd3(
			  chipsel=randint(0,31), line=randint(0,8),
			  data=_f68enc(repr(i))
			)
		else:
			p._cmd4(
			  chipsel=randint(0,31),
			  data=_f68enc(repr(i))
			)
		time.sleep(0.1)
	p.put_block(0,0,"TEST 123")
