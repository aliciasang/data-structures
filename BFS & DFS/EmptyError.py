class EmptyError(Exception):
    ''' class extending Exception to better document stack/queue errors '''
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

def main() -> None:
    try:
        raise EmptyError("testing the exception")
    except EmptyError as error:
        print(f"Caught EmptyError: {error}")
    except Exception as error:
        print(f"caught different type of error: {type(error).__name__}")

if __name__ == "__main__":
    main()

