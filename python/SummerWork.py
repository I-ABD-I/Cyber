def intInput(string: str) -> int:
    while True:
        try:
            return int(input(string))
        except ValueError:
            print("Invalid input")


def digits() -> None:
    """
    This function takes a 5-digit number as input, extracts its digits, calculates their sum, and prints
    the original number, its digits, and the sum of its digits.
    """
    num: int = intInput("Please enter a number with 5 digits: ")
    ncpy: int = num
    digits: str = ""
    sumDigits: int = 0

    while num > 0:
        digits += str(num % 10)
        sumDigits += num % 10
        num //= 10

    print(
        f"Your number is: {ncpy},\
        \nhis Digits are: {', '.join(digits[::-1])},\
        \nThe sum of the digits is: {sumDigits}"
    )


def anti_vowel(string: str) -> str:
    """
    The function removes all vowels from a given string and returns the modified string.

    string
      The input string that the function will remove vowels from
    """
    vowels: set[str] = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    for char in vowels:
        string = string.replace(char, "")

    return string
    # yohanan's function works perfectly fine but when he calls the function he dosent print the returned string


def password(string: str) -> bool:
    """
    The function returns true if the given string is a valid password by these conditions:
      1. the lenght is greater than 8
      2. starts with an english letter a-z, A-Z
      3. at least 2 digits
      4. at least 2 letters a-z, A-Z
      5. no sapcial characters except '_', '.'
      6. no spaces

    string
      the password to test
    """
    PASSSWORD_LENGTH: int = 8
    if len(string) < PASSSWORD_LENGTH:
        return False
    if not (0x41 <= ord(string[0]) <= 0x5A or 0x61 <= ord(string[0]) <= 0x7A):
        return False

    charNum: list[int] = [0, 0]
    for char in string:
        if char.isdigit():
            charNum[1] += 1
        elif 0x41 <= ord(char) <= 0x5A or 0x61 <= ord(char) <= 0x7A:
            charNum[0] += 1
        elif char != "." and char != "_":
            return False

    if charNum[0] < 2 or charNum[1] < 2:
        return False

    return True


def monthly_rain(monthly_rain: list[list[int]]) -> None:
    """
    This function takes a list of lists representing daily rainfall for a month and calculates the day
    with the most rain, the average rainfall, and the number of days without rain.

    monthly_rain
      A list of lists, where each inner list contains two integers representing the
      day of the month and the amount of rain (in millimeters) that fell on that day.
    """
    maxDay: int = 0
    maxRain: int = monthly_rain[0][1]

    totalRain: float = 0

    totalNoRain: int = 0
    for day in monthly_rain:
        if day[1] > maxRain:
            maxDay = day[0]
            maxRain = day[1]
        elif day[1] <= 0:
            totalNoRain += 1
        totalRain += day[1]

    print(
        f"The Day With the Most Rain Was: {maxDay},\
        \nThe avg Rain was: {totalRain/10},\
        \nThe Numer Of Days Without Rain is: {totalNoRain}"
    )


if __name__ == "__main__":
    print("\033[1mEx1: number with 5 digits\033[0m")
    digits()

    input("\nPlease press enter to continue\n")

    print("\033[1mEx2: A no Vowel String\033[0m")
    print(anti_vowel(input("Please enter a string: ")))

    input("\nPlease press enter to continue\n")

    print("\033[1mEx3: Passwords\033[0m")
    passwords: dict[str, bool | None] = {
        "hello": None,
        "HAI__..2333": None,
        "VERYSTRNOGPASSWORD123": None,
        "123Hello": None,
        "TEST!@#$!#@": None,
        "iLovePasswords6622": None,
    }
    passwords[input("Please enter a Password: ")] = None

    for pw in passwords:
        passwords[pw] = password(pw)
        print(pw + " -> " + str(passwords[pw]))

    input("\nPlease press enter to continue\n")

    print("\033[1mEx4: Monthly Rain\033[0m")
    monthly_rain([[1, 22], [2, 5], [3, 0], [4, 0], [5, 30]])
