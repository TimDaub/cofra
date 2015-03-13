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