#!/usr/bin/env python

"""
This module provides an array-like object that calls an arbitrary function when
the value of an element is requested.
"""

import numpy

class OnlineArray(numpy.ndarray):
    """
    This class mimics a multidimensional numpy array, except it does not store
    any data, instead all values are calculated on the fly. This can be
    convenient when an array gets too large and the receiving function only
    accepts an array.
    """
    def __new__(cls, shape, dtype=float, buffer=None, offset=0,
              strides=None, order=None, function=None, index=()):
        """
        Constructor for OnlineArray.

        For more documentation, see the help of {ndarray}.

        :arg function: General function having only integer arguments.
        :type function: function
        :arg index: The index of this arrray in its parent array.
        :type index: tuple(int)
        """
        array = super(OnlineArray, cls).__new__(cls, shape, dtype, buffer,
            offset, strides, order)
        array.function = function
        array.index = index

        return array
    #__new__

    def __getitem__(self, index):
        """
        Retrieve an item from the array.

        :arg index: The index of the element.
        :type index: int or tuple(int)

        :returns: Either a sub-array or an element.
        :rtype: OnlineArray or unknown
        """
        # NumPy style indexing.
        if type(index) == tuple:
            # A sub-array was requested.
            if len(index) < self.ndim:
                return OnlineArray(self.shape[len(index):],
                    function=self.function, index=self.index + index)

            # An element was requested.
            return self.function(*index)
        #if

        # Nested list style indexing.
        if self.ndim > 1:
            return OnlineArray(self.shape[1:],
                function=self.function, index=self.index + (index, ))

        # Recursion has ended, all indices are known.
        return self.function(*self.index + (index, ))
    #__getitem__

    def __str__(self):
        return "{} contains no data".format(repr(self))

    def __repr__(self):
        return str(self.__class__)
#OnlineArray

def online_array(function, shape):
    """
    Make an OnlineArray instance and initialise it.

    Currently, the {shape} parameter is used only for determining the number of
    dimensions. For an unbounded array please use 0 in the {shape} tuple. For
    example, an unbounded 2-dimensional array should be created with:

    >>> array = online_array((0, 0))

    :arg function: General function having only integer arguments.
    :type function: function(*(int))
    :arg shape: Shape of the array (not used, but receiving functions may rely
        on it).
    :type shape: tuple(int)
    """
    return OnlineArray(shape, function=function)
#online_array
