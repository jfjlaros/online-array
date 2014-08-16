"""
Tests for the `online_array` module.
"""

from online_array import online_array

class TestOnlineArray(object):
    def setup(self):
        """
        Create some arrays.
        """
        self.array_1 = online_array.OnlineArray((5, ), function=lambda x: x)
        self.array_2 = online_array.OnlineArray((4, 3),
            function=lambda x, y: x + y + 1)
        self.array_3 = online_array.OnlineArray((4, 3, 5),
            function=lambda x, y, z: x * y + z + 1)
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

    def test_index_1(self):
        assert(self.array_2[2][2] == 5)

    def test_index_2(self):
        assert(self.array_3[2][2][1] == 6)

    def test_index_3(self):
        row = self.array_3[0][1]

        assert(row[2] == 3)
    #test_index_3

    def test_numpy_index_1(self):
        assert(self.array_2[2, 2] == 5)

    def test_numpy_index_2(self):
        assert(self.array_3[2, 2, 1] == 6)

    def test_numpy_index_3(self):
        row = self.array_3[0, 1]

        assert(row[2] == 3)
    #test_index_3

    def test_boundary_1(self):
        assert(self.array_1[4] == 4)

    def test_boundary_2(self):
        assert(self.array_1[-5] == 0)

    def test_boundary_3(self):
        self._test_boundary(self.array_1, 5)

    def test_boundary_4(self):
        self._test_boundary(self.array_1, -6)
#TestOnlineArray
