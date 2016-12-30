class Scroller(object):

    def set_region(self, col, row, width):
        """
            Set the region that we are scrolling
            within the lcd.
            col/row 0-N
        """
        self.col = col
        self.row = row
        self.width = width
        self.cp = 0
        self.set_text('hello')

    def set_text(self, text):
        # to make things easier, padd text to guarrentee that
        # there are width worth of spaces before and after
        self.text = ' ' * self.width + text + ' ' * self.width
        self.cp = 0
        self.end_cp = len(self.text) - self.width

    def scroll(self, lcd=None):
        """
        Scroll one char. return updated display text.
        Also avail in display_text
        """
        if self.cp > self.end_cp:
            self.cp = 0
        else:
            self.cp = self.cp + 1
        t = self.text[self.cp:self.cp+self.width]
        if lcd is not None:
            lcd.set_cursor(self.col, self.row)
            lcd.message(t)
        return t


if __name__ == '__main__':
    s = Scroller()
    s.set_region(0, 0, 5)
    s.set_text('hi')
    for x in range(20):
        print '>%s<' % s.scroll()
