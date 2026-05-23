import logging
from error_handling import handle_error

def parse_data(data):
    try:
        # parsing logic here
        pass
    except Exception as e:
        handle_error(e, "Error parsing data")

def main():
    # example usage
    data = "example data"
    parse_data(data)

if __name__ == "__main__":
    main()