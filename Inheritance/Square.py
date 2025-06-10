'''Import rectangle class from Rectangle.py file'''
from Rectangle import Rectangle # type: ignore

class Square(Rectangle):
    '''Represents a Square, a subclass of Rectangle, where width and height are always equal so we remove the height parameter
    Attributes:
        _width (float): The side length of the square.
    '''
    __slots__ = ("_width",)

    def __init__(self, name: str, width: float) -> None:
        '''Initializes a Square instance with a name and side length.
        Parameters:
            name (str): name of the square
            width (float): side length of the square.
        Attributes:
            _width (float): stores width of the square
        '''
        super().__init__(name, width, width) # overrides Rectangle to only expect 'width' attribute and not 'height'
        self._width = width

    def setWidth(self, width: float) -> None:
        '''Updates the side length of the Square.
        Parameters:
            width (float): new side length.
        '''
        self._width = width
        self._height = width # updates height to the same as width, so case will always be a square
        self._area = self._width ** 2

    def setHeight(self, height: float) -> None:
        '''Updates the side length of the Square to ensure width and height are the same'''
        self._width = height
        self.setWidth(height)
        self._area = self._width ** 2

    def __str__(self) -> str:
        '''Returns a string representation of Square, with its its name, width, area, and perimeter
        Returns:
            str: A formatted string in the form "Square {name}: width = {width} area = {area} perimeter = {perimeter}".
        '''
        return f"Square {self._name}: width = {self._width} area = {self.getArea()} perimeter = {self.getPerimeter()}"
    
def main() -> None:
    print(f"Defining squares to test:")
    square_1 = Square("sarah", 3.0)
    square_2 = Square("steven", 1.25)
    square_3 = Square("steven", 1.25)

    print(f"Square 1: b = 3.0  ")
    print(f"Square 2: b = 1.25 ")
    print(f"Square 3: b = 1.25  \n")

    print(f"Test __str__")
    print(f"Actual output:   {square_1.__str__()}")
    print(f"Expected output: Square sarah: width = 3.0 area = 9.0 perimeter = 12.0\n")
    print(f"Actual output:   {square_2.__str__()}")
    print(f"Expected output: Square steven: width = 1.25 area = 1.5625 perimeter = 5.0\n")

    print(f"Test getWidth, getHeight, and getArea:")
    print(f"Actual output:   Square sarah  width = {square_1.getWidth()} area = {square_1.getArea()} perimeter = {square_1.getPerimeter()}")
    print(f"Expected output: Square sarah  width = 3.0 area = 9.0 perimeter = 12.0\n")
    print(f"Actual output:   Square steven width = {square_2.getWidth()}  area = {square_2.getArea()} perimeter = {square_2.getPerimeter()}")
    print(f"Expected output: Square steven width = 1.25 area = 1.5625 perimeter 5.0\n")

    print("Test __eq__")
    print(f"Testing square_1 == square_2: {square_1 == square_2}")
    print(f"Expected output: False (width and name are both different)")
    print(f"Testing square_2 == square_3 {square_2 == square_3}")
    print(f"Expected output: True (width and name are both the same)\n")

    print("Test setWidth")
    new_width = 12
    expected_area_new_width = new_width**2
    expected_perimeter_new_width = (4 * new_width)
    square_1.setWidth(new_width)
    print(f"updated Square sarah: width = {new_width} area = {expected_area_new_width}")
    print(f"Test for square_1.getWidth(): \nresult: {square_1.getWidth()} expected: {new_width}")
    print(f"Test for square_1.getArea(): \nresult: {square_1.getArea()} expected: {expected_area_new_width}\n")
    print(f"Test for square_1.getPerimeter(): \nresult: {square_1.getPerimeter()} expected: {expected_perimeter_new_width}\n")

    print("Test setHeight")
    new_height = 4
    expected_area_new_height = new_height**2
    expected_perimeter_new_height = (4 * new_height)
    square_2.setHeight(new_height)
    print(f"updated Rectangle steven: height = {new_height} area = {expected_area_new_height}")
    print(f"Test for square_2.getHeight(): \nresult: {square_2.getHeight()} expected: {new_height}")
    print(f"Test for square_2.getArea(): \nresult: {square_2.getArea()} expected: {expected_area_new_height}")
    print(f"Test for square_2.getPerimeter(): \nresult: {square_2.getPerimeter()} expected: {expected_perimeter_new_height}\n")

if __name__ == "__main__":
    main()