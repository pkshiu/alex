#!/usr/bin/python
import sys
import time

import Adafruit_CharLCD as LCD
from lcd_plus import LCDPlus
from snow import Snow
from scroller import Scroller
import schedule as sched


class Mood(object):
    """
    A how-i-am-feeling display
    """
    def __init__(self):
        self.m = 0
        self.msgs = [
            ('Happy Day!', LCDPlus.BK_BLUE),
            ('So So feeling today...', LCDPlus.BK_YELLOW),
            ('Arrgghhh !!', LCDPlus.BK_RED),
        ]
        self.update()

    def update(self):
        self.color = self.msgs[self.m][1]
        self.text = self.msgs[self.m][0]

    def next(self):
        self.m = self.m + 1
        if self.m >= len(self.msgs):
            self.m = 0
            # if no wrap around, self.m = len(self.msgs) - 1
        self.update()

    def prev(self):
        self.m = self.m - 1
        if self.m < 0:
            self.m = len(self.msgs) - 1
            # if no wrap around, self.m = 0
        self.update()

    def add_message(self, message, color=LCDPlus.BK_WHITE):
        self.msgs.append((message, color))


class App(object):

    def __init__(self):
        self.lcd = LCDPlus()

        self.snow = Snow()
        self.weather_scroller = Scroller()
        self.weather_scroller.set_region(0, 1, 10)

        self.mood = Mood()
        self.mood_scroller = Scroller()
        self.mood_scroller.set_region(0, 0, 10)

    def show_weather(self):
        self.weather_scroller.scroll(self.lcd)

    def show_time(self):
        self.lcd.set_cursor(11, 1)
        t = time.localtime()
        c = ':' if t.tm_sec % 2 == 0 else ' '
        self.lcd.message('%02d%c%02d' % (t.tm_hour, c, t.tm_min))

    def show_mood(self):
        self.mood_scroller.scroll(self.lcd)

    def update_mood(self):
        self.mood_scroller.set_text(self.mood.text)
        self.lcd.set_rgb(self.mood.color)

    def update_weather(self):
        self.snow.weather()
        self.weather_scroller.set_text('%s %dF %s %d%%' % \
            (self.snow.location, self.snow.temp, self.snow.description,
             self.snow.humidity))

    def go(self):
        sched.every(5).minutes.do(self.update_weather)

        self.lcd.clear()
        self.update_weather()
        # self.update_mood()
        print self.lcd.get_my_ip()
        self.mood_scroller.set_text(self.lcd.ip)
        self.mood.add_message(self.lcd.ip)

        prev_tick = 0
        while True:
            # tick in milli seconds
            tick = int(round(time.time() * 1000))
            if (tick - prev_tick) > 400:
                self.show_weather()
                self.show_time()
                self.show_mood()
                prev_tick = tick
                sched.run_pending()

            # if self.lcd.is_pressed(LCD.SELECT):
            if self.lcd.button_pressed(LCD.SELECT):
                self.lcd.set_rgb(LCDPlus.BK_WHITE)
                self.lcd.enable_display(False)
                break

            # if self.lcd.is_pressed(LCD.DOWN):
            if self.lcd.button_pressed(LCD.DOWN):
                self.mood.next()
                self.update_mood()

            # if self.lcd.is_pressed(LCD.UP):
            if self.lcd.button_pressed(LCD.UP):
                self.mood.prev()
                self.update_mood()

if __name__ == '__main__':
    # optional delay so that this can be run in rc.local
    if len(sys.argv) == 2 and sys.argv[1] == 'delay':
        time.sleep(30)

    app = App()
    app.go()
