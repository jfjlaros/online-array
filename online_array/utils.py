def fill_array(array, function, index=(), depth=0):
    """Fill an array with the values specified by {function}.

    :arg ndarray array: A NumPy array.
    :arg function function: Function that specifies the values.
    :arg tuple index: Index up to {depth} number of dimensions.
    :arg int depth: Depth of the recursion.
    """
    for i in range(array.shape[depth]):
        if array.ndim > depth + 1:
            fill_array(
                array, function, index=index + (i, ), depth=depth + 1)
        else:
            array[(index) + (i, )] = function(*(index) + (i, ))
