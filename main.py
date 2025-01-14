# main.py
from src.argument_parser import parse_arguments


def main():
    args = parse_arguments()
    if args:
        print(f"Received arguments: {args}")
        # Logic triggered by each argument is handled inside argument_parser.py
    else:
        print("No arguments provided or invalid input.")


if __name__ == "__main__":
    main()
