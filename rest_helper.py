"""

"""
import urllib2
import json
from collections import namedtuple


def to_obj(json_string):
    """ Convert json string to object with attributes. """
    o = json.loads(json_string, object_hook=lambda d: namedtuple('JsonData', d.keys(), rename=True)(*d.values()))
    return o


class RestHelper(object):
    def __init__(self):
        self.response = None

    def get(self, endpoint, payload, is_json=True):
        """
            Issue get request to endpoint with payload as data.
            set self.response to raw response, and
            self.data to data object from json response
        """
        s = ''
        for k, v in payload.items():
            if len(s) == 0:
                s = '?%s=%s' % (k, v)
            else:
                s += '&%s=%s' % (k, v)

        f = urllib2.urlopen(endpoint + s)
        self.response = f.read()
        if is_json:
            self.data = to_obj(self.response)

    def debug(self):
        """ Debug by pretty printing json string """
        print 'DEBUG-----:'
        print json.dumps(self.data, indent=4, sort_keys=True,
                         separators=(',', ': '))
        print '-----'
