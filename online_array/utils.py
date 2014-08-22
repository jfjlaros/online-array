#!/usr/bin/env python

def fill_array(array, function, index=(), depth=0):
    """
    Fill an array with the values specified by {function}.

    :arg array: A numpy array.
    :type array: ndarray
    :arg function: Function that specifies the values.
    :type function: function
    :arg index: Index up to {depth} number of dimensions.
    :type index: tuple(int)
    :arg depth: Depth of the recursion.
    :type depth: int
    """
    for i in range(array.shape[depth]):
        if array.ndim > depth + 1:
            fill_array(array, function, index=index + (i, ),
                depth=depth + 1)
        else:
            array[(index) + (i, )] = function(*(index) + (i, ))
    #for
#fill_array
