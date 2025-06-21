


class Vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        __rmul__ = self.__mul__


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vec2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Vec2(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Vec2(self.x // other.x, self.y // other.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        for coordinate in [self.x, self.y]:
            yield coordinate
    
    def __hash__(self):
        return hash(tuple(self))
#a = Vec2(1, 4)
#b = Vec2(2, 3)

#a-=b
#print(b-a)