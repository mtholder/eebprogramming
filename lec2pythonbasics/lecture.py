5 + 5
5 + 2.3
3*2
3.0*2
3.5*10 + 7
# strings
"hello"
'hello, there world!'
print 'hello, there world'
print """This
is a triple-
quoted string that can
span multiple lines."""
print 6
"hi"*3
"hi" + 5
#types
type(3)
type(3.0)
type("hi")
#variables
radius = 2
circum = 2*radius*3.141592653589793
print circum
radius = 4
print circum
another_variable = radius
print radius
print another_variable
radius = 10
print radius
print another_variable
print locals()
a="some string"
print locals()
3.15*10 + 7
print locals()
print globals()
del circum
del a
print locals()
#dynamictyping
type(radius)
copy_of_radius = radius
radius="the distance from the center of a circle to a point on the circle"
type(radius)
type(copy_of_radius)
#functions
def calc_circumference(radius):
    circumference =  2*radius*3.141592653589793
    return circumference
type(calc_circumference)
type(circumference)
calc_circumference(2)
calc_circumference(4)
x = calc_circumference(4)
type(x)
#scope
locals()
globals()
def calc_circumference(radius):
    print locals()
    circumference =  2*radius*3.141592653589793
    print locals()
    return circumference
locals()
#multiargs
def square_prism_volume(square_length, height):
    """Returns the volume of a rectangular prism with two sides that have a
    length of `square_length`. The length in the third dimension is `height`."""
    return square_length*square_length*height
help(square_prism_volume)
square_prism_volume(4, 10)
square_prism_volume(10, 4)
square_prism_volume(height=10, square_length=4)
def prism_volume(x, y, z):
    """Returns the volume of a rectangular prism with side lengths `x`, `y`, and `z`"""
    print "x =", x, ", y =", y, ", z =", z
    return x*y*z
prism_volume(1,2,3)
prism_volume(1,z=2,y=3)
prism_volume(z=2,y=3,1)
prism_volume('length', 'width', 'height')
prism_volume('length', 2, 3)
#flow
def checker(x, y):
    if x > y:
        print x, 'is bigger than', y
        return x
    else:
        print x, 'is not bigger than', y
        return y
bigger = checker(4, 6)
print(bigger)

def better_checker(x, y):
    if x > y:
        print x, 'is bigger than', y
        return x
    elif x == y:
        print x, 'is equal to than', y
        return y
    else:
        print x, 'is smaller than', y
        return y
better_checker(4, 4)
better_checker(4, 4.5)
better_checker(y=4, x=1)
