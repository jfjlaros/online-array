"""
Tests for the `online_array` module.
"""

import numpy

from online_array import online_array
from online_array import utils

class TestOnlineArray(object):
    def _f(self, x):
        return x

    def _g(self, x, y):
        return x + y + 1

    def _h(self, x, y, z):
        return x * y + z + 1

    def _make_array_pair(self, shape, function):
        """
        Make a named pair of arrays (online, real) and add it to the {arrays}
        dictionary.

        :arg shape: Shape of the arrays.
        :type shape: tuple(int)
        :arg function: Function that specifies the values.
        :type function: function

        :returns: A named pair of arrays.
        :rtype: dict
        """
        array = online_array.OnlineArray(shape, function=function)

        real_array = numpy.ndarray(shape)
        utils.fill_array(real_array, function)

        return {'online': array, 'real': real_array}
    #_make_array_pair

    def setup(self):
        """
        Create some arrays.
        """
        self.arrays = {}

        self.arrays['1d'] = self._make_array_pair((5, ), self._f)
        self.arrays['2d'] = self._make_array_pair((4, 3), self._g)
        self.arrays['3d'] = self._make_array_pair((4, 3, 5), self._h)

        self.unbounded_array = online_array.OnlineArray((0, ),
            function=self._f, unbounded=True)
    #setup

    def _test_boundary(self, array, index):
        """
        Check whether an `IndexError` is raised.

        :arg array: A one-dimensional array.
        :type array: OnlineArray
        :arg index: An index that is out of bound.
        :type index: int
        """
        try:
            array[index]
        except IndexError, error:
            assert(str(error) ==
                "index {} is out of bounds for axis 0 with size {}".format(
                    index, array.shape[0]))
        else:
            raise IndexError("boundary check failed")
    #_test_boundary

    def _test_loop(self, array, maximum):
        """
        See how far a loop goes.

        :arg array: A one-dimensional array.
        :type array: OnlineArray
        :arg maximum: Stop the test after this number of iterations.
        :type maximum: int
        """
        iterator = iter(array)

        for index in range(maximum):
            try:
                iterator.next()
            except StopIteration:
                break
        #for
        return index
    #_test_loop

    def _test_content(self, array, mirror, index=(), depth=0):
        """
        Test whether the complete content of {array} equals that of {mirror}.

        :arg array: Either an online or a real array.
        :type array: OnlineArray or ndarray
        :arg mirror: Either an online or a real array.
        :type mirror: OnlineArray or ndarray
        :arg index: Index up to {depth} number of dimensions.
        :type index: tuple(int)
        :arg depth: Depth of the recursion.
        :type depth: int
        """
        for i in range(array.shape[depth]):
            if array.ndim > depth + 1:
                self._test_content(array, mirror, index=index + (i, ),
                    depth=depth + 1)
            else:
                assert(array[(index) + (i, )] == mirror[(index) + (i, )])
        #for
    #_fill_array

    def test_index_1(self):
        assert(self.arrays['2d']['online'][2][2] == 5)

    def test_index_2(self):
        assert(self.arrays['3d']['online'][2][2][1] == 6)

    def test_index_3(self):
        row = self.arrays['3d']['online'][0][1]

        assert(row[2] == 3)
    #test_index_3

    def test_index_4(self):
        assert(self.arrays['1d']['online'][-2] ==
            self.arrays['1d']['online'][3])

    def test_numpy_index_1(self):
        assert(self.arrays['2d']['online'][2, 2] == 5)

    def test_numpy_index_2(self):
        assert(self.arrays['3d']['online'][2, 2, 1] == 6)

    def test_numpy_index_3(self):
        row = self.arrays['3d']['online'][0, 1]

        assert(row[2] == 3)
    #test_index_3

    def test_numpy_index_4(self):
        assert(self.arrays['2d']['online'][0, -2] ==
            self.arrays['2d']['online'][0, 1])

    def test_boundary_1(self):
        assert(self.arrays['1d']['online'][4] == 4)

    def test_boundary_2(self):
        assert(self.arrays['1d']['online'][-5] == 0)

    def test_boundary_3(self):
        self._test_boundary(self.arrays['1d']['online'], 5)

    def test_boundary_4(self):
        self._test_boundary(self.arrays['1d']['online'], -6)

    def test_unbounded_1(self):
        assert(self.unbounded_array[10] == 10)

    def test_unbounded_2(self):
        assert(self.unbounded_array[-10] == -10)

    def test_loop(self):
        assert(self._test_loop(self.arrays['1d']['online'], 10) == 5)

    def test_unbounded_loop(self):
        assert(self._test_loop(self.unbounded_array, 10) == 9)

    def test_assignment(self):
        try:
            self.arrays['1d']['online'][0] = 1
        except TypeError:
            pass
        else:
            raise TypeError("assignment check failed")
    #test_assignment

    def test_content_1(self):
        self._test_content(self.arrays['1d']['online'],
            self.arrays['1d']['real'])

    def test_content_2(self):
        self._test_content(self.arrays['1d']['real'],
            self.arrays['1d']['online'])

    def test_content_3(self):
        self._test_content(self.arrays['3d']['online'],
            self.arrays['3d']['real'])

    def test_content_4(self):
        self._test_content(self.arrays['3d']['real'],
            self.arrays['3d']['online'])

    def test_slicing_1(self):
        assert(self.arrays['1d']['online'][0:][0] ==
            self.arrays['1d']['online'][0])

    def test_slicing_2(self):
        assert(self.arrays['1d']['online'][2:][0] ==
            self.arrays['1d']['online'][2])

    def test_slicing_3(self):
        self._test_content(self.arrays['1d']['online'][2:],
            self.arrays['1d']['real'][2:])

    def test_slicing_4(self):
        self._test_content(self.arrays['1d']['online'][2:],
            self.arrays['1d']['real'][2:])

    def test_slicing_5(self):
        self._test_content(self.arrays['1d']['online'][1:][1:],
            self.arrays['1d']['real'][1:][1:])

    def test_slicing_6(self):
        self._test_content(self.arrays['1d']['online'][::],
            self.arrays['1d']['real'][::])

    #def test_slicing_6(self):
    #    self._test_content(self.arrays['1d']['online'][1::2][1::2],
    #        self.arrays['1d']['real'][1::2][1::2])
#TestOnlineArray
