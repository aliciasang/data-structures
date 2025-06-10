import random

def randomPermutation(word: str) -> str:
    '''
    define function to scramble the letters in a word using random.randint()
    Parameters: 
        word: the given word to be scrambled
    Returns: 
        scrambledWord: permuted version of word
    '''
  
    length = len(word)
    scrambledWord = ""
    
    # use a set to store available indices
    availableIndices = set(range(length))

    while availableIndices:
        # select a random index from the set
        selectedIndex = random.choice(tuple(availableIndices))  # convert temporarily to a tuple
        scrambledWord += word[selectedIndex] # append corresponding character
        availableIndices.remove(selectedIndex) # remove used index
    return scrambledWord

def readWords(filename: str) -> str:
    '''
    define function to read all words in a given file, convert to lowercase, and return a list of all words
    Parameters: 
        filename: name of the file which will be read
    Returns: 
        a list of all words in filename, converted to lowercase 
    '''
    words = []
    with open(filename, 'r') as file:
        line = file.readline()
        # reads next line while there is a line
        while line:
            lowercaseLine = line.lower() # convert to lowercase
            listOfWords = lowercaseLine.split() # split each line into individual words
                
            # loop through listOfWords and append each word
            for word in listOfWords:
                words.append(word)
            line = file.readline() # moves to next line, if empty, appends "" and exits while loop
    return words

def writePermutedWords(filename: str, words: str) -> list:
    '''
    define function to write a list of randomly permuted words to a file.
    Parameters: 
        filename: name of the file which will be written on
        words: list of words
    Returns:
        fullPath: file path where the file is created and saved to
    '''

    # define path
    folder = "/Users/aliciasang/Desktop/DCS229/"
    fullPath = folder + filename # concatenate full file path

    # locate directory where the file will be made
    with open(fullPath, 'w') as file:
        permutedWords = []
        for i in words:
            individualWord = randomPermutation(i)
            permutedWords.append(individualWord)
        
        # write the permuted words to the file, one word per line
        fileContent = "\n".join(permutedWords) + "\n"
        file.write(fileContent)

    print(f"File Path: {fullPath}")
    return fullPath

# one main function to run all tests on all three functions
def main():
    random.seed(2098543) # set seed so a specific random selection is made for testing

    # test randomPermutation
    print("randomPermutation test on (\"string\") with initial seed 2098543:")
    test1 = randomPermutation("string")
    print("Actual Output:", test1)
    print("Expected Output: rtnsgi\n")

    print("randomPermutation test on (\"jenny\") with initial seed 2098543:")
    test2 = randomPermutation("jenny")
    print("Actual Output:", test2)
    print("Expected Output: yenjn\n")

    print("randomPermutation test on (\"algorithms\") with initial seed 2098543:")
    test3 = randomPermutation("algorithms")
    print("Actual Output:", test3)
    print("Expected Output: oaimtshlgr\n")

    # testing readWords
    filePath = "/Users/aliciasang/Desktop/DCS229/"
    file1 = filePath + "testfile.txt"
    file2 = filePath + "testfile2.txt"

    print(f"readWords test on {file1}")
    result1 = readWords(file1)
    print("Actual Output:", result1)
    print("Expected Output: ['hello', 'python', 'can', 'you', 'read', 'this', 'file?']\n")

    print(f"readWords test on {file2}")
    result2 = readWords(file2)
    print("Actual Output:", result2)
    print("Expected Output: ['two', 'roads', 'diverged', 'in', 'a', 'yellow', 'wood,', 'and', 'sorry', 'i', 'could', 'not', 'travel', 'both', 'and', 'be', 'one', 'traveler,', 'long', 'i', 'stood', 'and', 'looked', 'down', 'one', 'as', 'far', 'as', 'i', 'could', 'to', 'where', 'it', 'bent', 'in', 'the', 'undergrowth;', 'then', 'took', 'the', 'other,', 'as', 'just', 'as', 'fair,', 'and', 'having', 'perhaps', 'the', 'better', 'claim,', 'because', 'it', 'was', 'grassy', 'and', 'wanted', 'wear;']\n")

    # testing writePermutedWords
    random.seed(1985034)  # set seed so a specific random selection is made for testing

    wordsToPermute1 = ["python", "viper", "boa", "garter"]
    writePermutedWords("permutedWords1.txt", wordsToPermute1)
    print("Permuted list is saved to file permutedWords1.txt")

    wordsToPermute2 = ["variables", "at", "the", "left", "margin", "exist", "in", "the", "global", "scope"]
    writePermutedWords("permutedWords2.txt", wordsToPermute2)
    print("Permuted list is saved to file permutedWords2.txt")

    wordsToPermute3 = ["python", "dedicates", "a", "separate", "location", "in", "memory", "to", "store", "parameters", "and", "variables"]
    writePermutedWords("permutedWords3.txt", wordsToPermute3)
    print("Permuted list is saved to file permutedWords3.txt")

main()