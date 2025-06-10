from __future__ import annotations

'''Import shape class from Shape.py file'''
from Shape import Shape # type: ignore

class Triangle(Shape):
    '''Represents a Triangle, a subclass of Shape

    Attributes:
        _base (float): The base length of the triangle
        _height (float): The height of the triangle
    '''
    __slots__ = ("_base", "_height")

    def __init__(self, name: str, base: float, height: float) -> None:
        '''Initializes a Triangle instance with a name, base, and height
        Parameters:
            name (str): name of the triangle.
            base (float): length of the triangle's base.
            height (float): height of the triangle.

        Attributes:
            _base (float): Stores the base of the triangle
            _height (float): Stores the height of the triangle
        '''
        super().__init__(name)
        self._base = base
        self._height = height
        self._area = 0.5 * self._base * self._height

    def getBase(self) -> float:
        '''Returns the base of the Triangle'''
        return self._base
    
    def getHeight(self) -> float: 
        '''Returns the height of the Triangle'''
        return self._height
    
    def setBase(self, base: float) -> None:
        '''Sets a new base length for the Triangle.
        Parameters:
            base (float): The new base length
        '''
        self._base = base
        self._area = 0.5 * self._base * self._height

    def setHeight(self, height: float) -> None:
        '''Sets a new height for the Triangle.
        Parameters:
            height (float): The new height
        '''
        self._height = height
        self._area = 0.5 * self._base * self._height

    def __str__(self) -> str:
        '''Returns a string representation of the Triangle, including its name, base, height, and area
        Returns:
            str: A formatted string "Triangle {name}: base = {base} height = {height} area = {area}".
        '''
        return f"Triangle {self._name}: base = {self._base} height = {self._height} area = {self.getArea()}"
    
    def __eq__(self, other: Triangle) -> bool:
        '''Checks if two Triangle instances are equal. Two triangles are considered equal if they have the same name, base, and height
        Parameters:
            other (object): object to compare with this Triangle.
        Returns:
            boolean: True if the triangles have the same name and the same base/height values,
            otherwise False.
        '''
        if isinstance(other, Triangle):
            return self._name == other._name and self._base == other._base and self._height == other._height
        return False
    
def main() -> None:
    print(f"Defining triangles to test:")
    triangle_1 = Triangle("thomas", 3.0, 4.0)
    triangle_2 = Triangle("teresa", 1.25, 6)
    triangle_3 = Triangle("teresa", 6, 1.25)

    print(f"Triangle 1: b = 3.0  h = 4.0")
    print(f"Triangle 2: b = 1.25 h = 6")
    print(f"Triangle 3: b = 6    h = 1.25\n")

    print(f"Test __str__")
    print(f"Actual output:   {triangle_1.__str__()}")
    print(f"Expected output: Triangle thomas: base = 3.0 height = 4.0 area = 6.0")
    print(f"Actual output:   {triangle_2.__str__()}")
    print(f"Expected output: Triangle teresa: base = 1.25 height = 6 area = 3.75\n")

    print(f"Test getBase, getHeight, and getArea:")
    print(f"Actual output:   Triangle thomas: base = {triangle_1.getBase()} height = {triangle_1.getHeight()} area = {triangle_1.getArea()}")
    print(f"Expected output: Triangle thomas: base = 3.0 height = 4.0 area = 6.0\n")
    print(f"Actual output:   Triangle teresa: base = {triangle_2.getBase()} height = {triangle_2.getHeight()} area = {triangle_2.getArea()}")
    print(f"Expected output: Triangle teresa: base = 1.25 height = 6 area = 3.75\n")

    print("Test __eq__")
    print(f"Testing triangle_1 == triangle_2: {triangle_1 == triangle_2}")
    print(f"Expected output: False (base/height and name are both different)")
    print(f"Testing triangle_2 == triangle_3 {triangle_2 == triangle_3}")
    print(f"Expected output: True (base/height and name are both the same)\n")

    print("Test setBase")
    new_base = 12
    expected_area_new_base = 0.5 * new_base * 4.0
    triangle_1.setBase(new_base)
    print(f"updated Triangle thomas: base = {new_base} area = {expected_area_new_base}")
    print(f"Test for triangle_1.getBase(): \nresult: {triangle_1.getBase()} expected: {new_base}")
    print(f"Test for triangle_1.getArea(): \nresult: {triangle_1.getArea()} expected: {expected_area_new_base}\n")

    print("Test setHeight")
    new_height = 4
    expected_area_new_height = 0.5 * 1.25 * new_height
    triangle_2.setHeight(new_height)
    print(f"updated Triangle teresa: height = {new_height} area = {expected_area_new_height}")
    print(f"Test for triangle_2.getHeight(): \nresult: {triangle_2.getHeight()} expected: {new_height}")
    print(f"Test for triangle_2.getArea(): \nresult: {triangle_2.getArea()} expected: {expected_area_new_height}")

if __name__ == "__main__":
    main()