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

    def _make_sub_array(self, index):
        """
        We create a sub-array that has knowledge about its position in the
        higher dimensional arrays. This is done by passing all known indices
        to the member variable {index} of {sub_array}.

        :arg index: List on indices.
        :type index: tuple(int)

        :returns: A sub-array.
        :rtype: OnlineArray
        """
        sub_array = OnlineArray(self.shape[len(index):])
        sub_array.function = self.function
        sub_array.index = self.index + index

        return sub_array
    #_make_sub_array

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
            if len(index) < len(self.shape):
                return self._make_sub_array(index)
            return self.function(*index)
        #if

        # Nested list style indexing.
        if len(self.shape) > 1:
            return self._make_sub_array((index, ))

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

    :arg function: General function having only integer arguments.
    :type function: function(*(int))
    :arg shape: Shape of the array (not used, but receiving functions may rely
        on it).
    :type shape: tuple(int)
    """
    array = OnlineArray(shape)
    array.function = function
    array.index = ()

    return array
#online_array
