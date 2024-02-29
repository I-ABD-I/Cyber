def decrypt_char(char: str, shift) -> str:
    if char.isalpha():
        if char.islower():
            return chr(((ord(char) - ord("a") - shift) % 26) + ord("a"))
        else:
            return chr(((ord(char) - ord("A") - shift) % 26) + ord("A"))
    else:
        return char


def decrypt_string(string: str, shift):
    return "".join([decrypt_char(char, shift) for char in string])


with open("ciphertext.txt") as f:
    txt = f.read()
    print(decrypt_string(txt, ord("S") - ord("E")))
