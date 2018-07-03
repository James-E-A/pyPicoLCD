import usb.core,usb.util
import time

OUT_REPORT_LED_STATE            = 0x81
OUT_REPORT_LCD_BACKLIGHT        = 0x91
OUT_REPORT_LCD_CONTRAST         = 0x92
OUT_REPORT_LCD_CONTROL          = 0x93
OUT_REPORT_LCD_CLEAR            = 0x94
OUT_REPORT_LCD_TEXT             = 0x98
OUT_REPORT_LCD_FONT             = 0x9C

OUT_REPORT_CMD			= 0x94
OUT_REPORT_DATA			= 0x95
OUT_REPORT_CMD_DATA		= 0x96

class PicoLcd:
	def __init__(self):
		self._dev=usb.core.find(idVendor=0x04d8, idProduct=0xc002)
		try:
			self._dev.detach_kernel_driver(0)
			self._dev.set_configuration()
			usb.util.claim_interface(self._dev,0)
			self._dev.set_interface_altsetting(0)
		except usb.core.USBError:
			pass
#		self._handle=usb.util.find_descriptor(
#		 self._dev.get_active_configuration()[(0,0)],
#		 custom_match = \
#		  lambda e: \
#		   usb.util.endpoint_direction(e.bEndpointAddress) \
#		   == \
#		   usb.util.ENDPOINT_OUT
#		)
#		assert self._handle is not None
	
	def write(self, data):
		print(repr(data))
		return self._dev.write(usb.util.ENDPOINT_OUT+1, data)
	
	def draw_text(self, text, row=0, col=0):
		addr = [0x80,0xc0,0x94,0xd4][row] + col
		self.write(bytes([
		 0x94,0x00,0x01,0x00,0x64,addr,
		 0x95,0x01,0x00,0x01,
		 len(text),*text.encode('ascii')
		]))
	
	def clear(self): #drv_pLG_clear from drv_picoLCDGraphic.c
		self.write(b'\x93\x01\x00')
		cmd2=bytearray(9)
		cmd3=bytearray(64)
		cmd4=bytearray(64)
		for i in range(4):
			cs=((i << 2) & 0xFF)
			cmd2[0]=OUT_REPORT_CMD
			cmd2[1]=cs
			cmd2[2]=0x02
			cmd2[3]=0x00
			cmd2[4]=0x64
			cmd2[5]=0x3F
			cmd2[6]=0x00
			cmd2[7]=0x64
			cmd2[8]=0xC0
			self.write(cmd2)
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
				temp=0
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

	def LEGACY_clear(self):
		for row in range(4):
			self.draw_text(row, 0, " " * 20)
	
	def set_backlight(self, brightness):
		return self.write(bytes([0x91, brightness]))
	
	def LEGACY_leds(self, state):
		self.wr(bytes(OUT_REPORT_LED_STATE, state))
	
	def LEGACY_flash(self):
		for brightness in range(20, 0, -1) + range(0, 21):
			self.backlight(brightness)
			time.sleep(.01)

	def text2(self, text, row=0,col=0): #drv_pL_write from drv_PicoLCD.c
		Q=bytearray()
		Q.append(0x98)
		Q.append(row)
		Q.append(col)
		Q.append(len(text))
		for char in text:
			Q.append(char)
		return self.write(bytes(Q))

if __name__ == "__main__":
	from datetime import datetime
	p = PicoLcd()
	p.clear()
	for i in range(256):
		p.set_backlight(i)
		time.sleep(0.2)
