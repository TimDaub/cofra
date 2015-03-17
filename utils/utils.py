import ConfigParser

def conv_to(fn, item=None):
    """
    Curryable function:
        Converts an item with a given (curried) function to another datatype
    """
    def conv_to_cur(item):
        try:
            return fn(item)
        except:
            return item
    if item == None: 
        return conv_to_cur
    else: 
        return conv_to_cur(item)

def get_config(section, key, method_name='get'):
    """
    Reads the 'config.cfg' file in the root directory and allows
    to select specific values from it that will - if found - be returned.
    """
    config_parser = ConfigParser.ConfigParser()
    config_parser.readfp(open(r'config.cfg'))
    try:
        return getattr(config_parser, method_name)(section, key)
    except:
        print 'Combination of section and key has not been found in config.cfg file.'
        return None