import operator
import sys

import numpy


class OnlineArray(numpy.ndarray):
    """This class mimics a multidimensional NumPy array where all values are
    calculated on the fly.
    """
    def _raise_type_error(self):
        raise TypeError(
            '{} cannot return unbounded content'.format(repr(self)))

    def _raise_assignment_error(self):
        raise TypeError(
            '{} object does not support item assignment'.format(repr(self)))

    def _protected_parent_call(self, function):
        """Protect parent calls from unbounded arrays.

        :arg function function: The arithmetic function.

        :returns any: The result of {function}.
        """
        if self.unbounded:
            self._raise_type_error()

        return getattr(super(OnlineArray, self), function)()

    def _protected_arithmetc_operation(self, function):
        """Protect arithmetic operations from unbounded arrays.

        :arg function function: The arithmetic function.

        :returns dtype: The result of {function}.
        """
        if self.unbounded:
            self._raise_type_error()

        return function([value for value in self])

    def _correct_index(self, index):
        """Check the boundaries and correct for negative indices.

        :arg int index: The index of the element.

        :returns int: Checked and corrected indices.
        """
        if self.unbounded:
            return index * self.step + self.start

        if not -self.shape[0] <= index < self.shape[0]:
            raise IndexError(
                'index {} is out of bounds for axis {} with size {}'.format(
                    index, self.ndim - 1, self.shape[0]))

        return (index % self.shape[0]) * self.step + self.start

    def _correct_slice(self, index):
        return slice(
            index.start or 0, index.stop or sys.maxint, index.step or 1)

    def __new__(
            cls, shape, dtype=float, buffer=None, offset=0, strides=None,
            order=None, function=None, index=(), unbounded=False, start=0,
            step=1):
        """Constructor for OnlineArray.

        For more documentation, see the help of {ndarray}.

        :arg function function: General function having only integer arguments.
        :arg tuple index: The index of this arrray in its parent array.
        :arg bool unbounded: Create an unbounded array.
        :arg int start:
        :arg int step:

        :returns OnlineArray:
        """
        array = super(OnlineArray, cls).__new__(
            cls, shape, dtype, buffer, offset, strides, order)
        array.function = function
        array.index = index
        array.unbounded = unbounded
        array.start = start
        array.step = step

        return array

    def __getitem__(self, index):
        """Retrieve an item from the array.

        :arg int/tuple index: The index of the element.

        :returns rtype: Either a sub-array or an element.
        """
        if type(index) == slice:
            corrected_slice = self._correct_slice(index)

            return OnlineArray(
                (int(min(self.shape[0], corrected_slice.stop) -
                    corrected_slice.start + corrected_slice.step - 0.5) //
                    corrected_slice.step, ) + self.shape[1:],
                dtype=self.dtype, function=self.function, index=self.index,
                unbounded=self.unbounded,
                start=self.start + (self.step * corrected_slice.start),
                step=self.step * corrected_slice.step)

        if type(index) == tuple:
            # NumPy style indexing.
            corrected_index = self._correct_index(index[0])

            if len(index) > 1:
                return OnlineArray(
                    self.shape[1:], dtype=self.dtype, function=self.function,
                    index=self.index + (corrected_index, ),
                    unbounded=self.unbounded)[index[1:]]
        else:
            corrected_index = self._correct_index(index)

        if self.ndim > 1:
            return OnlineArray(
                self.shape[1:], dtype=self.dtype, function=self.function,
                index=self.index + (corrected_index, ),
                unbounded=self.unbounded)

        return self.function(*self.index + (corrected_index, ))

    def __getslice__(self, a, b):
        return self.__getitem__(slice(a, b, 1))

    # Protected parent functions.
    def __repr__(self):
        return self._protected_parent_call('__repr__')

    def __str__(self):
        return self._protected_parent_call('__str__')

    # Arithmetic operations.
    def max(self):
        return self._protected_arithmetc_operation(max)

    def min(self):
        return self._protected_arithmetc_operation(min)

    def sum(self):
        return self._protected_arithmetc_operation(sum)

    def prod(self):
        return self._protected_arithmetc_operation(
            lambda value: reduce(operator.mul, value))

    def any(self):
        return self._protected_arithmetc_operation(any)

    def all(self):
        return self._protected_arithmetc_operation(all)

    # Unsupported operations.
    def __setitem__(self, index, value):
        self._raise_assignment_error()

    def put(self, ind, v, mode='raise'):
        self._raise_assignment_error()

    def sort(self):
        self._raise_assignment_error()


def _get_dtype(function):
    return type(function(*((0, ) * function.func_code.co_argcount)))


def online_array(function, shape):
    """Make an online array.

    :arg function function: General function having only integer arguments.
    :arg tuple shape: Shape of the array (not used, but receiving functions may
        rely on it).
    """
    return OnlineArray(shape, dtype=_get_dtype(function), function=function)


def unbounded_online_array(function):
    """Make an unbounded online array.

    :arg function function: General function having only integer arguments.
    """
    return OnlineArray(
        (0, ) * function.func_code.co_argcount, dtype=_get_dtype(function),
        function=function, unbounded=True)
