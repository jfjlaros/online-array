#!/usr/bin/env python

"""
This module provides a array-like object that calls an arbitrary function when
the value of an element is requested.
"""

import numpy

class OnlineArray(numpy.ndarray):
    """
    This class mimics a multidimensional numpy array, except it does not store
    any data, instead all values are calculated on the fly. This can be
    convenient when a array gets too large and the receiving function only
    accepts a array.
    """

    def _make_sub_array(self, shape, parameters):
        number_of_parameters = len(parameters)

        sub_array = OnlineArray(self.shape[number_of_parameters:])
        sub_array.function = self.function
        sub_array.parameters = self.parameters + parameters
        sub_array.dimensions = self.dimensions - number_of_parameters

        return sub_array
    #_make_sub_array

    def __getitem__(self, index):
        """
        Retrieve an item from the array.

        :arg index: The index of the element.
        :type index: int or tuple(int)
        """

        # NumPy style indexing.
        if type(index) == tuple:
            number_of_parameters = len(index)

            if number_of_parameters < self.dimensions:
                sub_array = OnlineArray(self.shape[number_of_parameters:])
                sub_array.function = self.function
                sub_array.parameters = self.parameters + index
                sub_array.dimensions = self.dimensions - number_of_parameters

                return sub_array
            #if
            return self.function(*index)

        # Nested list style indexing.
        if self.dimensions > 1:
            # We create a {dimensions} - 1 array that has knowledge
            # about its position in the higher dimensional matrices. This is
            # done by adding the index to the member variable {parameters} of
            # {sub_array}, when the recursion comes to an end, the
            # {parameters} variable will contain all but one indices.

            sub_array = OnlineArray(self.shape[1:])
            sub_array.function = self.function
            sub_array.parameters = self.parameters + (index, )
            sub_array.dimensions = self.dimensions - 1

            return sub_array
        #if
        # Recursion has ended, all indices are known.
        else:
            return self.function(*self.parameters + (index, ))
    #__getitem__

    def __str__(self):
        return "{} contains no data".format(repr(self))

    def __repr__(self):
        return str(self.__class__)
#OnlineArray

def online_array(function, shape=()):
    """
    Make an OnlineArray instance and initialise it.

    :arg function: General function having only integer arguments.
    :type function: function(*(int))
    :arg shape: Shape of the array (not used, but receiving functions may rely
        on it).
    :type shape: tuple(int)
    """
    # We use the number of parameters of {function} to set the number of
    # dimensions of the array.

    array = OnlineArray(shape)
    array.function = function
    array.parameters = ()
    array.dimensions = function.func_code.co_argcount

    return array
#online_array
