class A(object):
    def __init__(self, x):
        self._x = x
    def get_x(self):
        print "in get_x"
        return self._x
    def get_z(self):
        return self._x*self._x
    def set_x(self, new_val):
        print "in set_x"
        self._x = new_val
    x = property(get_x, set_x)
    z = property(get_z)


obj = A(2)
print obj.x
# don't use this 
print obj._x
print "z =", obj.z
obj.z = 3
obj.x = (2,3)

#obj.x = 3

print obj.x
# don't use this 
print obj._x

# don't use this 
obj._x = 10
print obj.x
# don't use this 
print obj._x

print obj.__dict__
print A.__dict__
print "z =", obj.z
