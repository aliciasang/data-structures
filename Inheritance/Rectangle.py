from __future__ import annotations

'''Import shape class from Shape.py file'''
from Shape import Shape # type: ignore

class Rectangle(Shape):
    '''Represents a Rectangle, a subclass of Shape
    Attributes:
        _width (float): The width of the rectangle.
        _height (float): The height of the rectangle.
    '''
    __slots__ = ("_width", "_height")

    def __init__(self, name: str, width: float, height: float) -> None:
        '''Initializes a Rectangle instance with a name, width, and height
        Parameters:
            name (str): The name of rectangle
            width (float): The width of rectangle
            height (float): The height of rectangle
        Attributes:
            _width (float): Stores width of rectangle.
            _height (float): Stores height of rectangle.
        '''
        super().__init__(name)
        self._width = width
        self._height = height
        self._area = self._width * self._height

    def getWidth(self) -> float:
        '''Returns width of the Rectangle'''
        return self._width
    
    def getHeight(self) -> float: 
        '''Returns height of the Rectangle'''
        return self._height
    
    def setWidth(self, width: float) -> None:
        '''Updates width of the Rectangle
        Parameters:
            width (float): new width value.
        '''
        self._width = width
        self._area = self._width * self._height

    def setHeight(self, height: float) -> None:
        '''Updates height of the Rectangle.

        Parameters:
            height (float): new height value
        '''
        self._height = height
        self._area = self._width * self._height
    
    def getPerimeter(self) -> float:
        '''Calculates and returns perimeter of the Rectangle
        Returns:
            float: perimeter of rectangle, computed with formula A = (2 * width) + (2 * height)
        '''
        return (2 * self._width) + (2 * self._height)

    def __str__(self) -> str:
        '''Returns a string representation of the Rectangle, with its name, width, height, and area
        Returns:
            str: A formatted string in the form "Rectangle {name}: width = {width} height = {height} area = {area}"
        '''
        return f"Rectangle {self._name}: width = {self._width} height = {self._height} area = {self.getArea()}"
    
    def __eq__(self, other: Rectangle) -> bool:
        '''Checks if two Rectangle instances are equal
        Parameters:
            other (object): object to compare with this Rectangle.
        Returns:
            boolean: True if the rectangles have the same name and the same width/height values (order-independent), otherwise False.
        '''
        if isinstance(other, Rectangle):
            return self._name == other._name and self._width == other._width and self._height == other._height
        return False
    
def main() -> None:
    print(f"Defining rectangles to test:")
    rectangle_1 = Rectangle("roberto", 3.0, 4.0)
    rectangle_2 = Rectangle("rachel", 1.25, 6)
    rectangle_3 = Rectangle("rachel", 6, 1.25)

    print(f"Rectangle 1: b = 3.0  h = 4.0")
    print(f"Rectangle 2: b = 1.25 h = 6")
    print(f"Rectangle 3: b = 6    h = 1.25\n")

    print(f"Test __str__")
    print(f"Actual output:   {rectangle_1.__str__()}")
    print(f"Expected output: Rectangle roberto: width = 3.0 height = 4.0 area = 12.0\n")
    print(f"Actual output:   {rectangle_2.__str__()}")
    print(f"Expected output: Rectangle rachel: width = 1.25 height = 6 area = 7.5\n")

    print(f"Test getWidth, getHeight, and getArea:")
    print(f"Actual output:   Rectangle roberto width = {rectangle_1.getWidth()} height = {rectangle_1.getHeight()} area = {rectangle_1.getArea()}")
    print(f"Expected output: Rectangle roberto width = 3.0 height = 4.0 area = 12.0\n")
    print(f"Actual output:   Rectangle rachel  width = {rectangle_2.getWidth()} height = {rectangle_2.getHeight()} area = {rectangle_2.getArea()}")
    print(f"Expected output: Rectangle rachel  width = 1.25 height = 6 area = 7.5\n")

    print("Test __eq__")
    print(f"Testing rectangle_1 == rectangle_2: {rectangle_1 == rectangle_2}")
    print(f"Expected output: False (width/height and name are both different)")
    print(f"Testing rectangle_2 == rectangle_3 {rectangle_2 == rectangle_3}")
    print(f"Expected output: True (width/height and name are both the same)\n")

    print("Test setWidth")
    new_width = 12
    expected_area_new_width = new_width * 4.0
    expected_perimeter_new_width = (2 * new_width) + (2 * 4.0)
    rectangle_1.setWidth(new_width)
    print(f"updated Rectangle roberto: width = {new_width} area = {expected_area_new_width}")
    print(f"Test for rectangle_1.getWidth(): \nresult: {rectangle_1.getWidth()} expected: {new_width}")
    print(f"Test for rectangle_1.getArea(): \nresult: {rectangle_1.getArea()} expected: {expected_area_new_width}\n")
    print(f"Test for rectangle_1.getPerimeter(): \nresult: {rectangle_1.getPerimeter()} expected: {expected_perimeter_new_width}\n")

    print("Test setHeight")
    new_height = 4
    expected_area_new_height = 1.25 * new_height
    expected_perimeter_new_height = (2 * 1.25) + (2 * new_height)
    rectangle_2.setHeight(new_height)
    print(f"updated Rectangle rachel: height = {new_height} area = {expected_area_new_height}")
    print(f"Test for rectangle_2.getHeight(): \nresult: {rectangle_2.getHeight()} expected: {new_height}")
    print(f"Test for rectangle_2.getArea(): \nresult: {rectangle_2.getArea()} expected: {expected_area_new_height}")
    print(f"Test for rectangle_2.getPerimeter(): \nresult: {rectangle_2.getPerimeter()} expected: {expected_perimeter_new_height}\n")

if __name__ == "__main__":
    main()