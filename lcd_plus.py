#!/usr/bin/python
import sys
import time

import Adafruit_CharLCD as LCD

class LCDPlus(LCD.Adafruit_CharLCDPlate):
    """
        More features adding to the Adafruit LCD Plate class.
    """
    BK_BLUE = 1
    BK_GREEN = 2
    BK_RED = 4
    BK_YELLOW = 6
    BK_CYAN = 3
    BK_MAGENTA = 5
    BK_WHITE = 7

    def __init__(self):
        # for debouncing buttons
        self._buttons = [0, 0, 0, 0, 0]
        super(LCDPlus, self).__init__()

    def set_rgb(self, v):
        """
            Set background using color constants above.
            v is 0-7, RGB bits
        """
        r = (v & 4) >> 2
        g = (v & 2) >> 1
        b = v % 2
        self.set_color(r, g, b)

    def button_pressed(self, b):
        v = self.is_pressed(b)
        if self._buttons[b] and not v:
            self._buttons[b] = False
            return False
        if not self._buttons[b] and v:
            self._buttons[b] = True
            return True
        return False

    def get_my_ip(self):
        from subprocess import check_output
        self.ip = check_output(['hostname', '--all-ip-addresses'])
        return self.ip

    def demo_time(self):
        self.clear()
        self.message('Select=exit')
        while not self.button_pressed(LCD.SELECT):
            self.set_cursor(11, 1)
            t = time.localtime()
            c = ':' if t.tm_sec % 2 == 0 else ' '
            self.message('%02d%c%02d' % (t.tm_hour, c, t.tm_min))


if __name__ == '__main__':
    my_lcd = LCDPlus()
    my_lcd.demo_time()
