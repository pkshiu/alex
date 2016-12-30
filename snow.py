import datetime

from rest_helper import RestHelper


class Snow(object):
    def __init__(self):
        self.rest = RestHelper()
        super(Snow, self).__init__()

    def ask(self, req, data):
        """
        req is the endpoint verb
        data is a dictionary of query key,value pairs.
        """
        payload = {'APPID' : 'xx',
                   'units': 'imperial',
                   # 'lang': 'zh'
                   }
        payload.update(data)
        uri = 'http://api.openweathermap.org/data/2.5/%s' % req
        self.rest.get(uri, payload)
        self.rest.debug()

    def weather(self):
        self.now_str = datetime.datetime.now().strftime('%c')
        self.ask('weather', {'q': 'Lexington,MA'})
        print self.rest.data
        print self.rest.data.name
        print self.rest.data.weather[0].description
        print self.rest.data.main.humidity
        print self.rest.data.main.temp
        # set these for use
        self.location = self.rest.data.name
        self.description = self.rest.data.weather[0].description
        self.humidity = self.rest.data.main.humidity
        self.temp = self.rest.data.main.temp

    def forcast(self):
        self.ask('forecast', {'q': 'Lexington,MA'})
        print self.rest.data

    def display(self):
        return
        oledExp.clear()
        y = 0
        oledExp.write(self.now_str)
        y += 1
        oledExp.setCursor(y, 0)
        oledExp.write(self.data.name)
        y += 1
        oledExp.setCursor(y, 0)
        oledExp.write(self.data.weather[0].description)
        y += 1
        oledExp.setCursor(y, 0)
        oledExp.write('%sF  %s%%' % (self.data.main.temp, self.data.main.humidity))


def do_weather(snow):
    snow.weather()
    snow.display()

if __name__ == '__main__':
    s = Snow()

    Snow().weather()
