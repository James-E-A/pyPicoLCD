import usb.core,usb.util
import time
import sys
from font68 import f68enc

picoLCD_VENDOR=0x04d8
picoLCD_DEVICE=0xc002

OUT_REPORT_LED_STATE		= 0x81
OUT_REPORT_LCD_BACKLIGHT        = 0x91
OUT_REPORT_LCD_CONTRAST         = 0x92

OUT_REPORT_CMD			= 0x94
OUT_REPORT_DATA			= 0x95
OUT_REPORT_CMD_DATA		= 0x96

OUT_REPORT_GPO			= 0x81
OUT_REPORT_WRITE		= 0x98

SCREEN_H			= 64
SCREEN_W			= 256

class PicoLcd:
	def __init__(self, idProduct=picoLCD_DEVICE, idVendor=picoLCD_VENDOR, DEBUG=False):
		"""Templated vaguely off drv_pLG_open"""
		self._dev=usb.core.find(idVendor=idVendor, idProduct=idProduct)
		
		self.errors=[]
		try:
			self._dev.detach_kernel_driver(0)
		except usb.core.USBError as e:
			self.errors.append(e)
			if e.errno != 2:
				raise
		self._dev.set_configuration()
		time.sleep(0.0001)
		usb.util.claim_interface(self._dev,0)
		self._dev.set_interface_altsetting(0)
		self._DEBUG=DEBUG
	
	def __del__(self):
		"""Templated vaguely off drv_pLG_close"""
		usb.util.release_interface(self._dev,0)
#		self._dev.reset()#SEGFAULTS
	
	def _write(self, data):
		"""Write the data to the device
		
		Templated vaguely off drv_pLG_send
		
		TODO: document WHETHER this is blocking,
		 and add an option to do the other way
		"""
		if self._DEBUG:
			sys.stderr.buffer.write(data)
		return self._dev.write(usb.util.ENDPOINT_OUT+1, data)
	
	def _read(self, n):
		"""Read n bytes from the device
		
		Templated vaguely off drv_pLG_read
		
		TODO: document WHETHER this is blocking,
		 and add an option to do the other way
		"""
		return self._dev.read(usb.util.ENDPOINT_IN+1, n)
	
	def set_backlight(self, brightness):
		"""Set the backlight to "brightness".
		
		* min:0
		* max:255
		* 1 through 14 are the same as 0
		* Every brightness level from 15 through about 24 is noticeable
		
		Templated vaguely off drv_pLG_backlight
		"""
		if brightness<15 and brightness!=0:
			pass#TODO: warn?
		return self._write(bytes([
		  OUT_REPORT_LCD_BACKLIGHT,
		  brightness
		]))
	
	def set_contrast(self, contrast):
		"""Templated vaguely off drv_pLG_contrast"""#TODO: physical errata
		return self._write(bytes([
		  OUT_REPORT_LCD_CONTRAST,
		  contrast
		]))
	
	def clear(self):
		"""cmd[3] from drv_pLG_clear, SEEMS TO do the following:
		
		Visually immediately blanks the entire screen. Pixels
		 [can PRESUMABLY be written during this time, but]
		 will not be displayed until re-enabled via OUT_REPORT_CMD.
		"""
		return self._write(bytes([
		  0x93,0x01,0x00
		]))
	
	def _out_report_cmd(self, i):
		"""cmd2[9] from drv_pLG_clear, SEEMS TO do the following:
		
		Given an integer i in range(4),
		
		Undo the effects of clear() on the (zero-inded) "i"th
		 quadrant of the screen, revealing the "underlying" image
		 that was present before the clear(), and re-enabling
		 that quadrant's image-display functionality.
		"""
		return self._write(bytes([
		  OUT_REPORT_CMD,
		  i*4,
		  0x02,0x00,0x64,0x3F,0x00,0x64,0xC0
		]))
	
	def _out_report_cmd_data(self, chipsel, line, payload):
		"""cmd3[64] from drv_pLG_update_img and drv_pLG_clear
		
		Cannibalized "magic" code, still testing
		
		TODO: description
		"""
		return self._write(bytes([
		  OUT_REPORT_CMD_DATA,
		  chipsel,
		  0x02,0x00,0x00,
		  line|0b10111000, #TODO: fuzz testing or something
		  0x00,0x00,0x40,0x00,0x00,
		  len(payload),
		  *payload
		]))
	
	def _out_report_data(self, chipsel, payload):
		"""cmd4 from drv_pLG_update_img and drv_pLG_clear
		
		Cannibalized "magic" code, still testing
		
		TODO: description
		"""
		return self._write(bytes([
		  OUT_REPORT_DATA,
		  chipsel|0b1, #TODO: fuzz testing or something
		  0x00,0x00,
		  len(payload),
		  *payload
		]))
	
	def _drv_pLG_clear(self):
		"""Legacy "clear" command from drv_picoLCDGraphic.c
		 SVN rev1204, line 340
		 https://lcd4linux.bulix.org/browser/trunk/drv_picoLCDGraphic.c?rev=1204#L340
		
		All 4 of the cmd* variables were initially
		 modularized/cannibalized from this function.
		
		Kept around mainly for interest, since it looks
		 like it has very few secrets left to yield.
		"""
		self.clear()
		for i in range(4):
			self.init_img_quadrant(i)
		payload=bytes(32)#b'\x00'*32
		for cs in range(0,4):
			for line in range(8):
				self._out_report_cmd_data(chipsel=cs*4, line=line, payload=payload)
				self._out_report_data(chipsel=cs*4, payload=payload)
	
	def put_block(self, col, row, payload):
		"""ALPHA-QUALITY function to draw pixels to the screen"""
		if col%2:
			raise NotImplementedError
		if len(payload)<=32:
			return self._cmd3(col*4,row,payload)
		else:
			assert len(payload)<=64
			return self._cmd3(col*4,row,payload[:32]) \
			     + self._cmd4(col*4,payload[32:])

if __name__ == "__main__":
	from datetime import datetime
	p = PicoLcd(DEBUG=True)
	p.drv_pLG_clear()
	for i in [0,*range(15,256)]:
		p.set_backlight(i)
		time.sleep(0.2)
	p.put_block(0,0,f68enc("TEST 123 W0Wo"))
