#!/usr/bin/env python

import numpy

class OnlineMatrix(numpy.ndarray):
    def __getitem__(self, index):
        if type(index) == tuple:
            return self.function(*index)

        if self.dimensions == 1:
            return self.function(*self.parameters + (index, ))
        else:
            sub_matrix = OnlineMatrix([])
            sub_matrix.function = self.function
            sub_matrix.parameters = self.parameters + (index, )
            sub_matrix.dimensions = self.dimensions - 1
            return sub_matrix
    #__getitem__

    def __str__(self):
        return "{} contains no data".format(str(self.__class__))

    def __repr__(self):
        return self.__str__()
#OnlineMatrix

def online_matrix(function, dimensions=2, shape=()):
    matrix = OnlineMatrix(shape)
    matrix.function = function
    matrix.parameters = ()
    matrix.dimensions = dimensions

    return matrix
#online_matrix
