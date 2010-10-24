from copy import deepcopy
from optparse import OptionParser

def cli_args(args=None):
    """Parse command line arguments"""
    parser = OptionParser()
    parser.add_option("-c", "--conffile", dest="conffile",
        default='firelet.ini', help="configuration file", metavar="FILE")
    parser.add_option("-D", "--debug",
        action="store_true", dest="debug", default=False,
        help="run in debug mode and print messages to stdout")
    parser.add_option("-q", "--quiet",
        action="store_true", dest="quiet", default=False,
        help="print less messages to stdout")
    if args:
        return parser.parse_args(args=args)
    return parser.parse_args()

class Alert(Exception):
    """Custom exception used to send an alert message to the user"""


class Bunch(object):
    """A dict that exposes its values as attributes."""
    def __init__(self, **kw):
        self.__dict__ = dict(kw)

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, name):
        return self.__dict__.__getitem__(name)

    def __setitem__(self, name, value):
        return self.__dict__.__setitem__(name, value)

    def __iter__(self):
        return self.__dict__.__iter__()

    def keys(self):
        return self.__dict__.keys()

    def _token(self):
        """Generate a simple hash"""
        return hex(abs(hash(str(self.__dict__))))[2:]

    def validate_token(self, t): #TODO: unit testing
        assert t == self._token(), \
        "Unable to update: one or more items has been modified in the meantime."

    def attr_dict(self):
        """Provide a copy of the internal dict, with a token"""
        d = deepcopy(self.__dict__)
        d['token'] = self._token()
        return d

    def update(self, d):
        """Set/update the internal dictionary"""
        for k in self.__dict__:
            self.__dict__[k] = d[k]


def flag(s):    #TODO: unit testing
    if s in (1, True, '1', 'True', 'y', 'on' ):
        return '1'
    elif s in (0, False, '0', 'False', 'n', 'off', ''):
        return '0'
    else:
        raise Exception, '"%s" is not a valid flag value' % s

def extract(d, keys):
    """Returns a new dict with only the chosen keys, if present"""
    return dict((k, d[k]) for k in keys if k in d)

def extract_all(d, keys):
    """Returns a new dict with only the chosen keys"""
    return dict((k, d[k]) for k in keys)

