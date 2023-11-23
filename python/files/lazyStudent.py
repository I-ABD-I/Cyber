import sys

try:
    HOMEWORK_FILE = sys.argv[1]
except IndexError:
    print("No Homework file specified, Exiting...")
    exit()

try:
    SOLUTION_FILE = sys.argv[2]
except IndexError:
    print("No Solution file specified, Exiting...")
    exit()


def solve_expression(expression: str) -> str:
    try:
        return eval(expression)
    except:
        return "ERROR"


def main():
    """
    Reads a homework file and generates a solution file.
    """
    try:
        with open(HOMEWORK_FILE, "r") as homework_file, open(
            SOLUTION_FILE, "w"
        ) as solution_file:
            for exercise in homework_file:
                exercise = exercise.rstrip("\n")
                solution_file.write(f"{exercise} = {solve_expression(exercise)}\n")
        print("Solution was written to " + SOLUTION_FILE)
    except FileNotFoundError:
        print("Homework File not found, Exiting...")
        exit()


if __name__ == "__main__":
    main()
