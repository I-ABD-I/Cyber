def fizz(num: int) -> str:
    return "Fizz" if num % 3 == 0 else ""


def buzz(num: int) -> str:
    return "Buzz" if num % 5 == 0 else ""


def fizzbuzz(num: int) -> str:
    fizzbuzz = fizz(num) + buzz(num)
    return fizzbuzz if fizzbuzz else str(num)


# for i in range(1, 100):
#     print(fizzbuzz(i))


for i in range(1, 100):
    print("Fizz" * (not i % 3) + "Buzz" * (not i % 5) or i)
