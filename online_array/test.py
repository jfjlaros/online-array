#!/usr/bin/env python

import online_array

def f(x, y):
    return x + y + 1

def g(x, y, z):
    return x * y + z + 1

def main():
    matrix = online_array.online_array(f, (4, 3))
    assert(matrix[2][2] == 5)
    assert(matrix[2, 2] == 5)
    assert(matrix.shape == (4, 3))
    assert(matrix.dimensions == 2)

    matrix = online_array.online_array(g, (4, 3, 5))
    assert(matrix[2][2][1] == 6)
    assert(matrix[2, 2, 1] == 6)
    assert(matrix.shape == (4, 3, 5))
    assert(matrix.dimensions == 3)

    row = matrix[0][1]
    assert(row[2] == 3)

    row = matrix[0, 1]
    assert(row[2] == 3)
#main

if __name__ == "__main__":
    main()
