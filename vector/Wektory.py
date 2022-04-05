from math import pi, acos, cos, sin


class Vector():

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __add__(self, other):
        return Vector(self._x+other._x, self._y+other._y)

    def __repr__(self):
        return f"({self._x}, {self._y})"

    def __abs__(self):
        return self.lenght()

    def dot_product(self, other):
        return self._x*other._x+self._y*other._y

    def __mul__(self, other):
        if other.isinstanse(int) or other.isinstanse(float):
            self._x *= other
            self._y *= other
            return self
        return self.dot_product(other)

    def recipicle(self):
        self._x *= (-1)
        self._y *= (-1)
        return self

    def __neg__(self):
        return self.recipicle()

    def lenght(self):
        return (self._x**2+self._y**2)**0.5

    def angle(self, other):
        lenghts_product = self.lenght()*other.lenght()
        if lenghts_product == 0:
            return 0
        else:
            return 180*acos(self.dot_product(other)/lenghts_product)/(pi)

    def rotate(self, angle):
        angle *= pi/180
        buf_x = self._x*cos(angle) - self._y*sin(angle)
        buf_y = self._y*cos(angle) + self._x*sin(angle)
        self._x = buf_x
        self._y = buf_y
        return self


v = Vector(2, 5)
w = Vector(8, -3)

print(v+w)
print(v*w)
print(v.angle(w))
print(v.rotate(45))
print(v.lenght())
print(w.lenght())
print(-w)
print(w.rotate(90))

print(v+w)

print(v*4)
