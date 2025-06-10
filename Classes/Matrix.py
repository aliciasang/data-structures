'''
References:
- StackOverflow: Attempted to use the logic behind the questions other people were asking, in order to apply it to my code
- ChatGPT: Used for debugging an issue with variable reference in __slots__. 
    Prompt: "Can you help me figure out why my code is giving me this error message?"
'''

from __future__ import annotations # so we can use Matrix as a type hint

class Matrix:
    __slots__ = ("_num_rows", "_num_cols", "_data")
    def __init__(self, num_rows: int = 0, num_cols: int = 0, data: list[int] = None, *, filename: str = None) -> None:
        '''Initializes a Matrix instance in class Matrix. Can be initialized in one of two ways: 
            - If keyword argument filename is provided, the Matrix data is loaded from the specified file
            - Else, the Matrix data is referred to using the num_rows, num_cols, and data lists specified in each instance in the main() function
            
            Parameters:
                self(Matrix): specifies Matrix instance
                num_rows(int): number of rows in the Matrix instance
                num_cols(int): number of columns in the Matrix instance
                data(list[int]): the data at each index in the matrix flattened into row-major order

            Notes: 
                - if keyword argument filename is provided; num_rows, num_cols, and data are passed
        '''
        if filename is not None: 
            self._init_from_file(filename)
        elif num_rows > 0 and num_cols > 0 and data is not None:
            self._init_from_data(num_rows, num_cols, data)
        else:
            raise ValueError("Matrix.__init__() requires either (num_rows, num_cols, data) or filename")

    def _init_from_data(self, num_rows: int, num_cols: int, data: list[int]) -> None:
        '''initializes matrices from data hard coded into tests in the main function
            Parameters:
                num_rows(int): number of rows in the matrix instance
                num_cols(int): number of columns in the matrix instance
                data(list[int]): the datapoints stored in each location within the matrix instance
            Raises:
                ValueError: if dimensions do not align with amount of data, or if a part of the matrix is empty
        '''
        if len(data) != num_rows * num_cols:
            raise ValueError("ValueError: dimensions do not match the amount of data given")

        self._num_rows = num_rows
        self._num_cols = num_cols
        self._data = [] ## loops through data twice
        for row in range(num_rows):
            row_data = [] 
            for col in range(num_cols):
                index = (row * num_cols) + col # build matrix one row at a time
                row_data.append( data[index] )
            self._data.append(row_data)
    
    def _init_from_file(self, filename: str) -> None:
        '''initializes matrices from file
            Parameters: 
                filename(str): variable which contains the name of the file with matrices in it
            Raises: 
                Value Error: if row lengths are inconsistent or if file is not in proper format
        '''
        all_rows = []

        with open (filename, 'r') as file:
            for row in file:
                row_data = []
                for data_point in row.split():
                    row_data.append(int(data_point))
                all_rows.append(row_data)
            
        if not all_rows: 
            raise ValueError("ValueError: file is empty or improperly formatted")
        
        self._num_rows = len(all_rows)
        self._num_cols = len(all_rows[0])
        self._data = all_rows

    def getNumRows(self) -> int:
        '''Getter method: Gets the number of rows in the matrix
            Parameters: 
                self (Matrix): matrix instance
            Returns: 
                int: number of rows in the matrix
        '''
        return self._num_rows

    def getNumCols(self) -> int:
        '''Getter method: Gets the number of columns in the matrix
            Parameters:
                self(Matrix): matrix instance
            Returns:
                int: number of columns in the matrix
        '''
        return self._num_cols

    def __str__(self) -> str:
        '''Converts the matrix into a formatted string for printing

        Parameters:
            self (Matrix): The matrix instance.

        Returns:
            str: A string representation of the matrix with proper formatting.

        Formatting:
            - Each row starts with "| " and ends with " |"
            - values are right-justified based on the longest number's width
            - Each value is separated by two spaces
            - No newline after the last row
        '''

        # find the width of the longest datapoint in the matrix
        if self._data:
            sigfigs = 0
            for row in self._data:
                for data_point in row:
                    sigfigs = max(sigfigs, len(str(data_point)))

        printing_format = []
        for row in self._data:
            formatted_row = []
            for data_point in row:
                formatted_row.append(f'{data_point:>{sigfigs}}')  # right-justify each number
            printing_format.append('|  ' + '  '.join(formatted_row) + '  |')  

        return '\n'.join(printing_format)

    def __getitem__(self, row_col: tuple) -> int:
        '''Gets a value from the matrix at the specified location
            Parameters:
                row_col (tuple[int,int]): tuple containing row and column information
            Returns: 
                int: datapoint stored at the given row and column index in the matrix instance
            Raises: 
                IndexError: if indices are outside of the range of the matrix 
        '''
        if not isinstance(row_col, tuple) or len(row_col) != 2 :
            raise TypeError("TypeError: index must be a tuple of two integers")

        row, col = row_col

        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError("TypeError: index must be a tuple of two integers")
        
        if row < 0:
            row += self._num_rows
        if col < 0:
            col += self._num_cols
                
        # raise IndexError to check if indices are within bounds
        if not (0 <= row < self._num_rows and 0 <= col < self._num_cols):
            raise IndexError("IndexError: indices out of range")

        return self._data[row][col]

    def __eq__(self, other: Matrix) -> bool:
        '''Tests equality of two matrices: number of rows, number of columns, and all datapoints must be equal to be marked True
            Parameters:
                self(Matrix): first Matrix to add
                other(Matrix): second Matrix to add
            Returns:
                Boolean: True or False depending on equality
            Raises: 
                TypeError: if trying to compare a matrix to a non-matrix object
        
        '''
        if type(other) is not Matrix:
            raise TypeError("TypeError: you are trying to compare a matrix to a non-matrix object")
        return (self._num_rows == other._num_rows and self._num_cols == other._num_cols and self._data == other._data)
        
    def __add__(self, other: Matrix) -> Matrix:
        '''adds two matrices together
            Parameters:
                self(Matrix): first matrix to add
                other(Matrix): second matrix to add
            Returns: 
                added together matrix
            Raises:
                TypeError: if trying to add an object which isn't a matrix
                ValueError: if the dimensions of self and other do not match
        '''

        if type(other) is not Matrix:
            raise TypeError("TypeError: trying to add a non-matrix object")
        if self._num_rows != other._num_rows or self._num_cols != other._num_cols:
            raise ValueError("ValueError: matrix dimensions need to match") 

        add_data = []
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                add_data.append(self._data[row][col] + other._data[row][col])
    
        return Matrix(self._num_rows, self._num_cols, add_data) 
       
    def transpose(self) -> Matrix:
        '''Swaps the rows and columns of the matrix
            Parameters: 
                self(Matrix): matrix instance
            Returns:
                Matrix, but with rows and columns swapped
        '''
        transposed_data = []
        for col in range (self._num_cols):
            for row in range (self._num_rows):
                transposed_data.append(self._data[row][col])

        return Matrix(self._num_cols, self._num_rows, transposed_data)

    def __mul__(self, other: Matrix) -> Matrix:
        '''Multiplies matrices
            Parameters: 
                self(Matrix): first matrix to multiply
                other(Matrix): second matrix to multiply
            Returns: 
                Multiplied matrix
            Raises:
                TypeError: if self or other is not a matrix
                ValueError: if the number of rows of one matrix do not equal the number of columns of the other        
        '''
        if self._num_cols != other._num_rows:
            raise ValueError("ValueError: rows of one matrix must equal columns of the other")
        if not isinstance(other, Matrix):
            raise TypeError("TypeError: trying to multiply a matrix by a non-matrix object")

        mul_data = []
        for i in range(self._num_rows):
            for j in range(other._num_cols):
                product = 0
                for k in range(self._num_cols):
                    product += self._data[i][k] * other._data[k][j]
                mul_data.append(product)
        return Matrix(self._num_rows, other._num_cols, mul_data) 

def main() -> None:
    '''main function for testing of Matrix class'''

    print("Define test matrices:")   
    print("Matrix 1:") 
    matrix_1 = Matrix(2, 3, [1, 23, 9854, 234, 17, 34587])
    print(matrix_1)

    print("\nMatrix 2:")
    matrix_2 = Matrix(2, 3, [4, 2, 3, 7, 1, 6])
    print(matrix_2)

    print("\nMatrix 3:")
    matrix_3 = Matrix(3, 4, [5, 2, 3, 5, 5, 7, 3, 6, 1, 9, 8, 4])
    print(matrix_3)

    print("\nMatrix 4:")
    matrix_4 = Matrix(3, 4, [5, 2, 3, 5, 5, 7, 3, 6, 1, 9, 8, 4])
    print(matrix_4)
    
    print("\ngetNumRows Test")
    print("Expected Output: 2")
    try:
        print(f"Actual Output: {matrix_1.getNumRows()}")
    except TypeError:
        print("TypeError: object is not a matrix")

    print("\ngetNumCols Test")
    print("Expected Output: 4")
    try:
        print(f"Actual Output: {matrix_3.getNumCols()}")
    except TypeError:
        print("TypeError: object is not a matrix")

    print("\ngetItem Test:")
    try:
        print(f"Expected Output: 34587\nActual Output: {matrix_1[1, 2]}")
        print(f"Expected Output: 4\nActual Output:{matrix_3[2, 3]}")
        print("Expected IndexError")
        print(f"{matrix_1[5, 5]}") # invalid indices exception handling
    except IndexError:
        print("IndexError: Indices outside of range")
        
    print("\nMatrix Equality Test:")
    try:
        print("Actual Output:", matrix_1 == matrix_2)
        print(f'Expected Output: False')

        print("Actual Output:", matrix_3 == matrix_4)
        print(f'Expected Output: True')

        print(f'Expected TypeError')
        print("\nActual Output:", matrix_3 == matrix_1[1,2])
     
    except TypeError:
        print("TypeError: attempting to compare matrix to a non-matrix object")
        
    print("\nMatrix Addition Test")
    try:
        print("Matrix 1 + Matrix 2")
        print(matrix_1 + matrix_2)
        print("\nMatrix 3 + Matrix 4")
        print(matrix_3 + matrix_4)
        print("\nExpected: ValueError") # ValueError exception handling
        print(matrix_1 + matrix_3)
    except ValueError:
        print("ValueError: You cannot add two matrices that do not have the same dimensions")

    print("\nMatrix Transposition Test")
    print("\nTransposed Matrix 1")
    print(f"Input: \n{matrix_1}")
    print(f"Output: \n{matrix_1.transpose()}")

    print("\nTransposed Matrix 2")
    print(f"Input: \n{matrix_2}")
    print(f"Output: \n{matrix_2.transpose()}")

    print("\nTransposed Matrix 3")
    print(f"Input: \n{matrix_3}")
    print(f"Output: \n{matrix_3.transpose()}")

    print("\nMatrix Multiplication Test")
    try:
        print(f"Input:\n{matrix_1}\n{matrix_3}")
        print("Output:")
        print(matrix_1 * matrix_3)
        
        print(f"\nInput:\n{matrix_2}\n{matrix_3}")
        print("Output:")
        print(matrix_2 * matrix_3)

        print("\nExpected: Value Error")  # ValueError exception handling test
        print("Output:")
        print(matrix_2 * matrix_1)
    except ValueError:
        print("ValueError: rows of one matrix must equal columns of the other")
    
    print("\nRead From File Test")
    try:
        matrix_from_file = Matrix(filename="test_matrix.txt")
        print("Matrix successfully loaded from file:")
        print(matrix_from_file)
    except FileNotFoundError:
        print("Error: File 'test_matrix.txt' not found")

    print("\nMatrix Addition With Matrix From File:")
    try:
        matrix_sum = matrix_from_file + matrix_from_file # adding the same matrix twice so they have the same dimensions
        print(matrix_sum)
    except ValueError:
        print("\nMatrix Addition Error: Matrices have different dimensions and cannot be added.")
  
if __name__ == "__main__":
    main()