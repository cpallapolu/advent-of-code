
class Position2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'(x, y): ({self.x}, {self.y})'

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def __add__(self, other):
        return Position2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Position3D:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'(x, y, z): ({self.x}, {self.y}, {self.z})'

    def __hash__(self):
        return hash(tuple((self.x, self.y, self.z)))

    def __add__(self, other):
        return Position3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
