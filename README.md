# Online array: A function that behaves like a NumPy array.
This package provides a class that mimics a multidimensional NumPy array. These
arrays however, do not contain any data, all values are calculated on the fly
instead. In this way, a function can be passed as an array to any function that
only accepts arrays.

The function that gives the values of the online array is passed to the
constructor of the class. The online array supports indexing, slicing and
various arithmetic operations. Additionally, *unbounded* arrays can be defined.


## Installation
Via [PyPI](https://pypi.python.org/pypi/online-array):

    pip install online-array

From source:

    git clone https://github.com/jfjlaros/online-array.git
    cd online-array
    pip install .


## Usage
Suppose we have the following function that we want to pass as an array to an
other function:

```python
def f(x, y):
    return x + y + 1
```

The easiest way to use the `OnlineArray` class is to pass a function and a
shape to the convenience function `online_array`:

```python
>>> from online_array import online_array
>>> a = online_array(f, (3, 3))
```

We now have a 3 by 3 online array. Values can be retrieved in the standard way
by using indexes:

```python
>>> a[1][2]
4
>>> a[1,2]
4
```

Slicing and stepping is supported:

```python
>>> a[1:]
OnlineArray([[             2,              3,              4],
             [             3,              4,              5]])
>>> a[::2]
OnlineArray([[              1,               2,               3],
             [              3,               4,               5]])
>>> a[::2][1][0]
3
```

To create an unbounded array, the convenience function `unbounded_online_array`
can be used:

```python
>>> from online_array import unbounded_online_array
>>> a = unbounded_online_array(f)
>>> a[31415926535897932384626433][27182818284590452353602874]
58598744820488384738229308L
```

Finally, the class `OnlineArray` can be used directly.
```python
>>> from online_array import OnlineArray
>>> help(OnlineArray)
```
