import usb
import time

def bytes(*b):
    return "".join([chr(x) for x in b])

OUT_REPORT_LED_STATE            = 0x81
OUT_REPORT_LCD_BACKLIGHT        = 0x91
OUT_REPORT_LCD_CONTRAST         = 0x92
OUT_REPORT_LCD_CONTROL          = 0x93
OUT_REPORT_LCD_CLEAR            = 0x94
OUT_REPORT_LCD_TEXT             = 0x98
OUT_REPORT_LCD_FONT             = 0x9C

class PicoLcd:

    def __init__(self):
        buses = usb.busses()
        for bus in buses:
            for device in bus.devices:
                if device.idVendor == 0x04d8 and device.idProduct == 0xc001:
                    lcd = device

        self.handle = lcd.open()

        try:
            self.handle.detachKernelDriver(0)
        except usb.USBError:
            pass
        self.handle.claimInterface(0)
        self.handle.setAltInterface(0)

    def wr(self, m):
        return self.handle.interruptWrite(usb.ENDPOINT_OUT + 1, m, 1000)

    def draw_text(self, row, col, text):
        addr = {0: 0x80, 1: 0xc0, 2:0x94, 3:0xd4}[row] + col
        self.wr(bytes(0x94, 0x00, 0x01, 0x00, 0x64, addr))
        self.wr(bytes(0x95, 0x01, 0x00, 0x01, len(text)) + text)

    def clear(self):
        for row in range(4):
            self.draw_text(row, 0, " " * 20)

    def backlight(self, brightness):
        self.wr(bytes(OUT_REPORT_LCD_BACKLIGHT, brightness))

    def leds(self, state):
        self.wr(bytes(OUT_REPORT_LED_STATE, state))

    def flash(self):
        for brightness in range(20, 0, -1) + range(0, 21):
            self.backlight(brightness)
            time.sleep(.01)

if __name__ == "__main__":
    from datetime import datetime
    p = PicoLcd()
    p.clear()
    p.draw_text(0, 0, "It worked!")
    p.draw_text(3, 0, datetime.now().ctime()[:20])
