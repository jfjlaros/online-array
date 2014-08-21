#!/usr/bin/env python

import numpy

class OnlineArray(numpy.ndarray):
    """
    This class mimics a multidimensional numpy array, except it does not store
    any data, instead all values are calculated on the fly. This can be
    convenient when an array gets too large and the receiving function only
    accepts an array.
    """
    def __new__(cls, shape, dtype=float, buffer=None, offset=0, strides=None,
            order=None, function=None, index=(), unbounded=False, start=0,
            step=1):
        """
        Constructor for OnlineArray.

        For more documentation, see the help of {ndarray}.

        :arg function: General function having only integer arguments.
        :type function: function
        :arg index: The index of this arrray in its parent array.
        :type index: tuple(int)
        :arg unbounded: Create an unbounded array.
        :type unbounded: bool
        :arg start:
        :type start: int
        :arg step:
        :type step: int
        """
        array = super(OnlineArray, cls).__new__(cls, shape, dtype, buffer,
            offset, strides, order)
        array.function = function
        array.index = index
        array.unbounded = unbounded
        array.start = start
        array.step = step

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
        if type(index) == slice:
            corrected_slice = self._correct_slice(index)

            return OnlineArray(
                (self.shape[0] - corrected_slice.start,) + self.shape[1:],
                function=self.function, index=self.index,
                unbounded=self.unbounded,
                start=self.start + corrected_slice.start,
                step=self.step * corrected_slice.step)
        #if

        if type(index) == tuple:
            # NumPy style indexing.
            corrected_index = self._correct_index(index[0])

            if len(index) > 1:
                return OnlineArray(self.shape[1:], function=self.function,
                    index=self.index + (corrected_index, ),
                    unbounded=self.unbounded)[index[1:]]
        #if
        else:
            corrected_index = self._correct_index(index)

        if self.ndim > 1:
            return OnlineArray(self.shape[1:], function=self.function,
                index=self.index + (corrected_index, ),
                unbounded=self.unbounded)

        return self.function(*self.index + (corrected_index, ))
    #__getitem__

    def __setitem__(self, index, value):
        raise TypeError("{} object does not support item assignment".format(
            repr(self)))

    def __getslice__(self, a, b):
        return self.__getitem__(slice(a, b, 1))

    #def __str__(self):
    #    return "{} contains no data".format(repr(self))

    def __repr__(self):
        return str(self.__class__)

    def _correct_index(self, index):
        """
        Check the boundaries and correct for negative indices.

        :arg index: The index of the element.
        :type index: int

        :returns: Checked and corrected indices.
        :rtype: int
        """
        if self.unbounded:
            return index * self.step + self.start

        if not -self.shape[0] <= index < self.shape[0]:
            raise IndexError("index {} is out of bounds for axis {} with "
                "size {}".format(index, self.ndim - 1, self.shape[0]))

        return (index % self.shape[0]) * self.step + self.start
    #_correct_index

    def _correct_slice(self, index):
        return slice(index.start or 0, index.stop or 0, index.step or 1)
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
    return OnlineArray(shape, function=function)
#online_array
