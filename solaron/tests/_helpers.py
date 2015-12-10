"""Some useful helper functions used during testing
"""

def getTestHashCode():
    import traceback
    stack = traceback.extract_stack()
    frame = next(x for x in stack if x[2].startswith('test'))
    return frame[2].__hash__()
