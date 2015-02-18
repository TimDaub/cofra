def conv_to(fn):
    """
    Curryable function:
        Converts an item with a given (curried) function to another datatype
    """
    def conv_to_cur(item):
        try:
            return fn(item)
        except:
            return item
    return conv_to_cur