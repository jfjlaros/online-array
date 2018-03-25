"""Tests for the `online_array` module."""
import numpy

from online_array import OnlineArray, fill_array


def _f(x):
    return x


def _g(x, y):
    return x + y + 1


def _h(x, y, z):
    return x * y + z + 1


def _make_array_pair(shape, function):
    """Make a named pair of arrays (online, real) and add it to the
    {arrays} dictionary.

    :arg tuple shape: Shape of the arrays.
    :arg function function: Function that specifies the values.

    :returns dict: A named pair of arrays.
    """
    array = OnlineArray(shape, function=function)

    real_array = numpy.ndarray(shape)
    fill_array(real_array, function)

    return {'online': array, 'real': real_array}


def _test_boundary(array, index):
    """Check whether an `IndexError` is raised.

    :arg OnlineArray array: A one-dimensional array.
    :arg int index: An index that is out of bound.
    """
    try:
        array[index]
    except IndexError, error:
        assert(
            str(error) ==
            'index {} is out of bounds for axis 0 with size {}'.format(
                index, array.shape[0]))
    else:
        raise IndexError('boundary check failed')


def _test_loop(array, maximum):
    """See how far a loop goes.

    :arg OnlineArray array: A one-dimensional array.
    :arg int maximum: Stop the test after this number of iterations.
    """
    iterator = iter(array)

    for index in range(maximum):
        try:
            iterator.next()
        except StopIteration:
            break
    return index


def _test_content(array, mirror, index=(), depth=0):
    """Test whether the complete content of {array} equals that of
    {mirror}.

    :arg OnlineArray/ndarray array: Either an online or a real array.
    :arg OnlineArray/ndarray mirror: Either an online or a real array.
    :arg tuple index: Index up to {depth} number of dimensions.
    :arg int depth: Depth of the recursion.
    """
    for i in range(array.shape[depth]):
        if array.ndim > depth + 1:
            _test_content(array, mirror, index=index + (i, ), depth=depth + 1)
        else:
            assert(array[(index) + (i, )] == mirror[(index) + (i, )])


def _test_assignment(assignment_test):
    """Test whether an assignment fails.

    :arg str assignment_test: A python code snippet.

    :returns bool: True if {assignment_test} fails with a TypeError.
    """
    try:
        eval(assignment_test)
    except TypeError:
        return True
    return False


class TestOnlineArray(object):
    def setup(self):
        """Create some arrays."""
        self.arrays = {}

        self.array_1 = _make_array_pair((5, ), _f)
        self.array_2 = _make_array_pair((4, 3), _g)
        self.array_3 = _make_array_pair((4, 3, 5), _h)

        self.unbounded_array = OnlineArray((0, ), function=_f, unbounded=True)

    def test_index_1(self):
        assert(self.array_2['online'][2][2] == 5)

    def test_index_2(self):
        assert(self.array_3['online'][2][2][1] == 6)

    def test_index_3(self):
        row = self.array_3['online'][0][1]
        assert(row[2] == 3)

    def test_index_4(self):
        assert(self.array_1['online'][-2] == self.array_1['online'][3])

    def test_numpy_index_1(self):
        assert(self.array_2['online'][2, 2] == 5)

    def test_numpy_index_2(self):
        assert(self.array_3['online'][2, 2, 1] == 6)

    def test_numpy_index_3(self):
        row = self.array_3['online'][0, 1]
        assert(row[2] == 3)

    def test_numpy_index_4(self):
        assert(self.array_2['online'][0, -2] == self.array_2['online'][0, 1])

    def test_boundary_1(self):
        assert(self.array_1['online'][4] == 4)

    def test_boundary_2(self):
        assert(self.array_1['online'][-5] == 0)

    def test_boundary_3(self):
        _test_boundary(self.array_1['online'], 5)

    def test_boundary_4(self):
        _test_boundary(self.array_1['online'], -6)

    def test_unbounded_1(self):
        assert(self.unbounded_array[10] == 10)

    def test_unbounded_2(self):
        assert(self.unbounded_array[-10] == -10)

    def test_loop(self):
        assert(_test_loop(self.array_1['online'], 10) == 5)

    def test_unbounded_loop(self):
        assert(_test_loop(self.unbounded_array, 10) == 9)

    def test_assignment_1(self):
        assert("self.array_1['online'][0] = 1")

    def test_assignment_2(self):
        assert('self.array_1.put(0, 1)')

    def test_assignment_3(self):
        assert('self.array_1.sort()')

    def test_content_1(self):
        _test_content(self.array_1['online'], self.array_1['real'])

    def test_content_2(self):
        _test_content(self.array_1['real'], self.array_1['online'])

    def test_content_3(self):
        _test_content(self.array_3['online'], self.array_3['real'])

    def test_content_4(self):
        _test_content(self.array_3['real'], self.array_3['online'])

    def test_slicing_1(self):
        assert(self.array_1['online'][0:][0] == self.array_1['online'][0])

    def test_slicing_2(self):
        assert(self.array_1['online'][2:][0] == self.array_1['online'][2])

    def test_slicing_3(self):
        _test_content(self.array_1['online'][2:], self.array_1['real'][2:])

    def test_slicing_4(self):
        _test_content(self.array_1['online'][2:], self.array_1['real'][2:])

    def test_slicing_5(self):
        _test_content(
            self.array_1['online'][1:][1:], self.array_1['real'][1:][1:])

    def test_slicing_6(self):
        _test_content(self.array_1['online'][::], self.array_1['real'][::])

    def test_slicing_7(self):
        _test_content(
            self.array_1['online'][1:3:2], self.array_1['real'][1:3:2])

    def test_slicing_8(self):
        _test_content(
            self.array_1['online'][1::2][1::2],
            self.array_1['real'][1::2][1::2])

    def test_max_1(self):
        assert(max(self.array_1['online']) == 4)

    def test_max_2(self):
        assert(self.array_1['online'].max() == 4)

    def test_min_1(self):
        assert(min(self.array_1['online']) == 0)

    def test_min_2(self):
        assert(self.array_1['online'].min() == 0)

    def test_sum_1(self):
        assert(sum(self.array_1['online']) == 10)

    def test_sum_2(self):
        assert(self.array_1['online'].sum() == 10)

    def test_prod(self):
        assert(self.array_1['online'][1:].prod() == 24)

    def test_any(self):
        assert(self.array_1['online'].any())

    def test_all(self):
        assert(not self.array_1['online'].all())
