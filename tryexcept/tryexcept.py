import operator


def div(n1, n2):
    try:
        return n1 / n2
    except:
        print("Error")


def get(arg):
    try:
        arg.get()
    except TypeError:
        pass
    except:
        print("Error get dosent exist")


def clac(n1: str, opr: str, n2: str):
    dict = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    try:
        num1 = float(n1)
        num2 = float(n2)

        func = dict[opr]
        return func(num1, num2)

    except KeyError:
        print("Wrong input for operator")
    except:
        print("Wrong input for numbers")


if __name__ == "__main__":
    div(1, 2)
    get(["hi", "bye"])
    clac(input("Enter a number: "), input("Enter a operator: "), input("Enter a number:"))
