import ConfigParser

class CfgParser():
    """
    Receives a path to a .cfg file and a section keyword and then parses
    keys from a .cfg file.
    """
    def __init__(self, path, section):
        self.path = path
        self.section = section

    def get_key(self, key, method_name='get'):
        """
        Reads from the <path> file and allows
        to select specific values from it that will - if found - be returned.
        """
        config_parser = ConfigParser.ConfigParser()
        config_parser.readfp(open(self.path))
        try:
            return getattr(config_parser, method_name)(self.section, key)
        except:
            print 'Combination of section and key has not been found in .cfg file.'
            print 'key = ' + key + ', section = ' + self.section
            return None