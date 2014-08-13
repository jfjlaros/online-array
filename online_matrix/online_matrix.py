#!/usr/bin/env python

"""
This module provides a matrix-like object that calls an arbitrary function when
the value of an element is requested.
"""

import numpy

class OnlineMatrix(numpy.ndarray):
    """
    This class mimics a multidimensional numpy array, except it does not store
    any data, instead all values are calculated on the fly. This can be
    convenient when a matrix gets too large and the receiving function only
    accepts a matrix.
    """

    def __getitem__(self, index):
        """
        Retrieve an item from the matrix.

        :arg index: The index of the element.
        :type index: int or tuple(int)
        """

        # NumPy style indexing.
        if type(index) == tuple:
            return self.function(*index)

        # Nested list style indexing.
        if self.dimensions > 1:
            # We create a {dimensions} - 1 matrix that has knowledge
            # about its position in the higher dimensional matrices. This is
            # done by adding the index to the member variable {parameters} of
            # {sub_matrix}, when the recursion comes to an end, the
            # {parameters} variable will contain all but one indices.

            sub_matrix = OnlineMatrix(self.shape[1:])
            sub_matrix.function = self.function
            sub_matrix.parameters = self.parameters + (index, )
            sub_matrix.dimensions = self.dimensions - 1

            return sub_matrix
        #if
        # Recursion has ended, all indices are known.
        else:
            return self.function(*self.parameters + (index, ))
    #__getitem__

    def __str__(self):
        return "{} contains no data".format(self.__repr__())

    def __repr__(self):
        return str(self.__class__)
#OnlineMatrix

def online_matrix(function, shape=()):
    """
    Make an OnlineMatrix instance and initialise it.

    :arg function: General function having only integer arguments.
    :type function: function(*(int))
    :arg shape: Shape of the matrix (not used, but receiving functions may rely
        on it).
    :type shape: tuple(int)
    """
    # We use the number of parameters of {function} to set the number of
    # dimensions of the matrix.

    matrix = OnlineMatrix(shape)
    matrix.function = function
    matrix.parameters = ()
    matrix.dimensions = function.func_code.co_argcount

    return matrix
#online_matrix
