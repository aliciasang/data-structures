'''citations: used stack overflow to review newline debugging issue'''

import sys
from Stack import Stack

def readFile(filename: str) -> str:
    ''' 
    Function to open and read a file whose name is provided as the argument.

    Args:
        filename (str): The name of the file to be read.

    Returns:
        str: The content of the file as a string with trailing newlines removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    '''
    try:
        with open(filename, 'r') as file:
            return file.read().rstrip("\n")  # keeps whitespace but removes trailing newlines
    except FileNotFoundError:
        raise FileNotFoundError(f'File {filename} does not exist')

def extract_tags(html: str) -> list:
    '''Extracts tags from an HTML string while ignoring comments'''
    tags = []
    i = 0
    while i < len(html):
        if html[i:i+4] == "<!--":  # detects comment start
            i += 4
            while i < len(html) and html[i:i+3] != "-->":
                i += 1
            i += 3  # skip past closing "-->"
            continue

        if html[i] == '<':
            j = i + 1
            while j < len(html) and html[j] != '>':
                j += 1
            if j < len(html):
                tag = html[i + 1:j].split()[0]
                tag = tag.rstrip('/')  # normalize self-closing tags
                tags.append(tag)  
            i = j  # moves i to correct position
        else:
            i += 1

    return tags

def parseHTML(entire_text: str) -> bool:
    '''
    Parses HTML text and determines if it has properly matched tags.

    Args:
        entire_text (str): The HTML content as a string.

    Returns:
        bool: True if all opening and closing tags are properly matched, False otherwise.

    Raises:
        None
    '''
    self_closing_tags = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    }
    
    tags = extract_tags(entire_text)
    stack = Stack()

    for tag in tags:
        if tag in self_closing_tags:
            continue  # ignore self-closing tags

        if not tag.startswith('/'):  # opening tag
            stack.push(tag)
        else:
            tag_name = tag[1:]  # closing tag, remove "/"
            if stack.isEmpty():
                print(f"unmatched </{tag_name}>")
                return False

            last_open = stack.pop()
            if last_open != tag_name:
                if last_open in stack._data:
                    print(f"mismatched <{last_open}> to </{tag_name}> --OR-- unmatched <{last_open}>")
                else:
                    print(f"mismatched <{last_open}> to </{tag_name}>")
                return False

    if not stack.isEmpty():
        unmatched_tags = ",".join(f"<{tag}>" for tag in stack._data)
        print(f"unmatched tags: {unmatched_tags}")
        return False

    return True

def main() -> None:
    try:
        if len(sys.argv) < 2:
            print('Usage: python dcs229_hw5.py <filename>')
            sys.exit(2)

        filename = sys.argv[1]
        html_text = readFile(filename)

        if parseHTML(html_text):
            print('HTML passes check')
        else:
            sys.exit(1)

    except FileNotFoundError:
        print(f'File {filename} does not exist')
        sys.exit(1)

    except IndexError:
        print('Incorrect number of command-line arguments')
        sys.exit(2)

if __name__ == "__main__":
    main()