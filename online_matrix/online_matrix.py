#!/usr/bin/env python

import numpy

class OnlineMatrix(numpy.ndarray):
    def __getitem__(self, index):
        if type(index) == tuple:
            return self.function(*index)

        if self.dimensions > 1:
            sub_matrix = OnlineMatrix(self.shape[1:])
            sub_matrix.function = self.function
            sub_matrix.parameters = self.parameters + (index, )
            sub_matrix.dimensions = self.dimensions - 1

            return sub_matrix
        #if
        else:
            return self.function(*self.parameters + (index, ))
    #__getitem__

    def __str__(self):
        return "{} contains no data".format(self.__repr__())

    def __repr__(self):
        return str(self.__class__)
#OnlineMatrix

def online_matrix(function, shape=()):
    matrix = OnlineMatrix(shape)
    matrix.function = function
    matrix.parameters = ()
    matrix.dimensions = function.func_code.co_argcount

    return matrix
#online_matrix
