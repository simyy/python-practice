#!/usr/bin/env python
# encoding:utf-8

class _const:
    class ConstError(TypeError): 
        print 'const variablies, don\'t change'
    def __setattr__(self,name,value):
            raise self.ConstError
    A = 0
    B = 1
    
const = _const()
