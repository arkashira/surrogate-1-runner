from parser import Parser

def main():
    parser = Parser()
    try:
        parser.parse("some data")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()