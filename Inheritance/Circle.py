'''Import shape class from Shape.py file'''
from Shape import Shape # type: ignore

class Circle(Shape):
    '''Represents a Circle, a subclass of Shape

    Attributes:
        _radius (float): The radius of the circle
    '''
    __slots__ = ("_radius",)

    def __init__(self, name: str, radius: float) -> None:
        '''Initializes a Circle instance with a name and radius
        Parameters:
            name (str): The name of the circle
            radius (float): The radius of the circle
        Attributes:
            _radius (float): Stores radius of the circle
            _area (float): Stores computed area of the circle
        '''

        super().__init__(name)
        self._radius = radius
        self._area = 3.1415926 * radius**2

    def getRadius(self) -> float:
        '''Returns the radius of the Circle'''
        return self._radius
    
    def setRadius(self, radius: float) -> None:
        '''Changes the radius to a new value'''
        self._radius = radius
        self._area = 3.1415926 * (self._radius ** 2)
        
    def getPerimeter(self) -> float:
        '''Calculates and returns the perimeter of the Circle'''
        return 2 * 3.1415926 * self._radius
    
    def __str__(self) -> str:
        '''Returns a string representation of the Circle, including its name, radius, and area

        Returns:
            str: A formatted string in the form "Circle {name}: radius = {radius} area = {area}".
        '''
        return f"Circle {self._name}: radius = {self._radius} area = {self._area}"

def main() -> None:
    print(f"Defining circles to test:")
    circle_1 = Circle("samantha", 2.0)
    circle_2 = Circle("samuel", 3.7)
    circle_3 = Circle("samuel", 3.7)
    print(f"Circle 1: r = 2.0")
    print(f"Circle 2: r = 3.7")
    print(f"Circle 3: r = 5.0\n")

    print(f"Test __str__")
    print(f"Actual output:   {circle_1.__str__()}")
    print(f"Expected output: Circle samantha: radius = 2.0 area = 12.5663704")
    print(f"Actual output:   {circle_2.__str__()}")
    print(f"Expected output: Circle samuel: radius = 3.7 area = 43.008402694000004\n")

    print(f"Test getRadius, getArea, and getPerimeter:")
    print(f"Actual output:   Circle samantha: radius = {circle_1.getRadius()} area = {circle_1.getArea()} perimeter = {circle_1.getPerimeter()}")
    print(f"Expected output: Circle samantha: radius = 2.0 area = 12.5663704 perimeter = 12.5663704\n")
    print(f"Actual output:   Circle samuel: radius = {circle_2.getRadius()} area = {circle_2.getArea()} perimeter = {circle_2.getPerimeter()}")
    print(f"Expected output: Circle samuel: radius = 3.7 area = 43.008402694000004 perimeter = 23.247785240000002\n")

    print("Test __eq__")
    print(f"Testing circle_1 == circle_2: {circle_1 == circle_2}")
    print(f"Expected output: False (radius and name are both different)")
    print(f"Testing circle_2 == circle_3 {circle_2 == circle_3}")
    print(f"Expected output: True (radius and name are both the same)\n")

    print("Test setRadius")
    new_radius = 4
    expected_area = 3.1415926 * new_radius **2
    expected_perimeter = 2 * 3.1415926 * new_radius
    circle_1.setRadius(new_radius)
    print(f"updated Circle samantha: radius = {new_radius} area = {expected_area} perimeter = {expected_perimeter}")
    print(f"Test for circle_1.getRadius(): \nresult: {circle_1.getRadius()} expected: {new_radius}")
    print(f"Test for circle_1.getArea(): \nresult: {circle_1.getArea()} expected: {expected_area}")
    print(f"Test for circle_1.getPerimeter()\nresult: {circle_1.getPerimeter()} expected: {expected_perimeter}")

if __name__ == "__main__":
    main()