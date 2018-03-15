
import math

class Vector2D:
    def __init__(self, _x:float = 0.0, _y:float = 0.0):
        self.x = _x
        self.y = _y

    def length_squared(self):
        return (self.x * self.x) + (self.y * self.y)

    def length(self):
        return math.sqrt(self.length_squared())

    def __eq__(self, rhs):
        return (self.x == rhs.x) and (self.y == rhs.y)

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)

    def __iadd__(self, rhs):
        self.x += rhs.x; self.y += rhs.y
        return self

    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)

    def __isub__(self, rhs):
        self.x -= rhs.x; self.y -= rhs.y
        return self
        
    def __mul__(self, rhs):
        if (isinstance(rhs, Vector2D)): return ((self.x * rhs.x) + (self.y * rhs.y))
        else: return Vector2D(self.x * rhs, self.y * rhs)
        
    def __rmul__(self, rhs):
        if (isinstance(rhs, Vector2D)): return ((self.x * rhs.x) + (self.y * rhs.y))
        else: return Vector2D(self.x * rhs, self.y * rhs)
        
    def __muli__(self, rhs:float):
        self.x *= rhs; self.y *= rhs
        return self

    def __floordiv__(self, rhs:float):
        return Vector2D(self.x / rhs, self.y / rhs)
        
    def __truediv__(self, rhs:float):
        return Vector2D(self.x / rhs, self.y / rhs)

    def __divi__(self, rhs:float):
        self.x /= rhs; self.y /= rhs;
        return self

    def cross(self, rhs):
        return Vector2D(self.x * rhs.y - self.y * rhs.x)