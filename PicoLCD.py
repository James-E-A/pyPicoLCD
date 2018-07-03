import usb.core,usb.util
import time

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
	def __init__(self, idProduct=picoLCD_DEVICE, idVendor=picoLCD_VENDOR):
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
	
	def __del__(self):
		# drv_pLG_close
		usb.util.release_interface(self._dev,0)
#		self._dev.reset()
	
	def write(self, data): #drv_pLG_send
		time.sleep(1)
		print(repr(data[:8]), '+', len(data)-8)
		return self._dev.write(usb.util.ENDPOINT_OUT+1, data)
	
	def read(self, n): #drv_pLG_read
		return self._dev.read(usb.util.ENDPOINT_IN+1, n)
	
	def clear(self):
		return self.write(b'\x93\x01\x00')
	def restore_block(self, i):
		return self.write(bytes([
		 OUT_REPORT_CMD,
		 i*4,
		 0x02,0x00,0x64,0x3F,0x00,0x64,0xC0
		]))
	def drv_pLG_clear(self):
		self.clear()
		for i in range(4):
			self.restore_block(i)
		cmd3=bytearray(64)
		cmd4=bytearray(64)
		for cs in range(4):
			chipsel = (cs << 2);
			for line in range(8):
				cmd3[0]=OUT_REPORT_CMD_DATA
				cmd3[1]=chipsel
				cmd3[2]=0x02
				cmd3[3]=0x00
				cmd3[4]=0x00
				cmd3[5]=0xb8|line
				cmd3[6]=0x00
				cmd3[7]=0x00
				cmd3[8]=0x40
				cmd3[9]=0x00
				cmd3[10]=0x00
				cmd3[11]=32
				temp=0x00
				for index in range(32):
					cmd3[12+index]=temp
				self.write(cmd3)
				cmd4[0]=OUT_REPORT_DATA
				cmd4[1]=chipsel|0x01
				cmd4[2]=0x00
				cmd4[3]=0x00
				cmd4[4]=32
				for index in range(32,64):
					temp=0x00
					cmd4[5+(index-32)] = temp
				self.write(cmd4)

	
	def set_backlight(self, brightness): #drv_pLG_backlight
		return self.write(bytes([
		 OUT_REPORT_LCD_BACKLIGHT,
		 brightness
		]))
	
	def set_contrast(self, contrast): #drv_pLG_contrast
		return self.write(bytes([
		 OUT_REPORT_LCD_CONTRAST,
		 contrast
		]))
	
	def text(self, text, row=0,col=0): #drv_pL_write from drv_PicoLCD.c
		# https://lcd4linux.bulix.org/browser/trunk/drv_picoLCD.c#L250
		# I have no idea why this isn't working...
		return self.write(bytes([
		 OUT_REPORT_WRITE,
		 row,
		 col,
		 len(text),
		 *text
		]))

if __name__ == "__main__":
	from datetime import datetime
	p = PicoLcd()
	p.clear()
	for i in range(8):
		p.set_backlight(1<<i)
		p.text("HELLO 123 TESTING TESTING 123".encode('ascii'), i, 5)
		time.sleep(0.2)
