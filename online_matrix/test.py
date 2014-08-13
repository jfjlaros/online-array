#!/usr/bin/env python

import online_matrix

def f(x, y):
    return x + y + 1

def test_matrix(matrix, function, i, j):
    print "matrix[{}][{}] returns {}, should be {}".format(i, j, matrix[i][j],
        function(i, j))
    print "matrix[{}, {}] returns {}, should be {}".format(i, j, matrix[i, j],
        function(i, j))
#test_matrix

def main():
    matrix = online_matrix.online_matrix(f, 2, (4, 3))

    for i in range(3):
        for j in range(4):
            test_matrix(matrix, f, i, j)
    print matrix.shape
    print matrix
    print repr(matrix)
#main

if __name__ == "__main__":
    main()
