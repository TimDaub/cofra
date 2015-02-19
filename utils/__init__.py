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

def extr_from_concept_net_edge(s):
    """
    ConceptNet returnes on lookup edges that are named in this fashion:

        'c/en/autobahn'

    From this we can extract:
        - type
        - language-code
        - name of the node
    """
    params_list = s.split('/')
    if len(params_list) < 3: 
        raise Exception('The given string did not contain at least two slashes.')
    return {
        'type': params_list[1],
        'lang_code': params_list[2],
        'name': params_list[3]
    }