from abc import ABC, abstractmethod


class Shape(ABC):

    def __init__(self, c: str):
        self.color = c

    def get_color(self) -> str:
        return self.color

    @abstractmethod
    def get_area(self) -> float:
        pass

class Square(Shape):

    def __init__(self, c: str, side: float):
        super().__init__(c)
        self.side = float(side)

    def get_area(self) -> float:
        return self.side * self.side

color = input("Enter square color: ")
side = float(input("Enter square side length: "))

sq = Square(color, side)
print(f"Color: {sq.get_color()}")
print(f"Area: {sq.get_area()}")