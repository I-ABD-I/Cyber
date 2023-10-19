_author_ = "Aylon"


def printNumber(num):
    print(num)


def printDigits(num: int):
    for i in str(num):
        print(i)


def printSum(num: int):
    sum = 0
    for i in str(num):
        sum += int(num)
    print(sum)


def fibto10k():
    n1 = 0
    n2 = 1
    while True:
        print(n1)
        n1, n2 = n2, n1 + n2
        if n1 > 10000:
            break


def subDirDomain(domain: str):
    return domain.split("/")

def main():
    num: int = int(input("Please enter a number with 5 digits: "))
    printNumber(num)
    printDigits(num)
    printSum(num)


if __name__ == "__main__":
    fibto10k()
