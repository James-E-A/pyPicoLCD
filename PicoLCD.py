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
		# drv_pLG_open
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
		# drv_pLG_close
		usb.util.release_interface(self._dev,0)
#		self._dev.reset()
	
	def write(self, data): #drv_pLG_send
		if self._DEBUG:
			sys.stderr.buffer.write(data)
		return self._dev.write(usb.util.ENDPOINT_OUT+1, data)
	
	def read(self, n): #drv_pLG_read
		return self._dev.read(usb.util.ENDPOINT_IN+1, n)
	
	def clear(self):
		return self.write(b'\x93\x01\x00')
	
	def init_img_quadrant(self, i):
		# This function name is a GUESS
		return self.write(bytes([
		 OUT_REPORT_CMD,
		 i*4,
		 0x02,0x00,0x64,0x3F,0x00,0x64,0xC0
		]))
	
	def put_block(self, col, row, payload):
		if col%2:
			raise NotImplementedError
		if len(payload)<=32:
			return self._cmd3(col*4,row,payload)
		else:
			assert len(payload)<=64
			return self._cmd3(col*4,row,payload[:32]) \
			     + self._cmd4(col*4,payload[32:])
	
	def _cmd3(self, chipsel, line, payload=[0x00]*32):
		return self.write(bytes([
		 OUT_REPORT_CMD_DATA,
		 chipsel,
		 0x02,0x00,0x00,
		 0xb8|line,
		 0x00,0x00,0x40,0x00,0x00,
		 len(payload),
		 *payload
		]))
	def _cmd4(self, chipsel, payload=[0x00]*32):
		return self.write(bytes([
			OUT_REPORT_DATA,
			chipsel|0x01,#NOTE: no idea what chipsel actually sets
			0x00,0x00,
			len(payload),
			*payload
		]))
	def drv_pLG_clear(self):
		self.clear()
		for i in range(4):
			self.init_img_quadrant(i)
		for cs in range(0,4):
			for line in range(8):
				self._cmd3(chipsel=cs*4, line=line)
				self._cmd4(chipsel=cs*4)
	
	def set_backlight(self, brightness): #drv_pLG_backlight
		if brightness<15 and brightness!=0:
			pass #Backlight is off, maybe TODO warn or something
		return self.write(bytes([
		 OUT_REPORT_LCD_BACKLIGHT,
		 brightness
		]))
	
	def set_contrast(self, contrast): #drv_pLG_contrast
		return self.write(bytes([
		 OUT_REPORT_LCD_CONTRAST,
		 contrast
		]))

if __name__ == "__main__":
	from datetime import datetime
	p = PicoLcd(DEBUG=True)
	p.drv_pLG_clear()
	for i in [0,*range(15,256)]:
		p.set_backlight(i)
		p.put_block(0,0,f68enc("TEST 123 W0Wo"))
		time.sleep(0.2)
