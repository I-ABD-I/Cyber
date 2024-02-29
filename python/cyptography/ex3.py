txt = "c0xCVlFTFl5BGFVbXUtTF19ZXVISS0NFVxhCWBJaUxdAXVdTSw=="

import base64 as b64


to_decode = b64.b64decode(txt).decode()


def encrypt(message, key):
    return "".join(
        [chr(ord(message[i]) ^ ord(key[i % len(key)])) for i in range(len(message))]
    )


def decrypt(message, key):
    return encrypt(message, key)


import enchant

usdict = enchant.Dict("en_us")

for l1 in range(10):
    for l2 in range(10):
        for l3 in range(10):
            for l4 in range(10):
                key = f"{l1}{l2}{l3}{l4}"
                if all(
                    [usdict.check(word) for word in decrypt(to_decode, key).split(" ")]
                ):
                    print(key, decrypt(to_decode, key))

# key 2867: Attack is close make sure to be ready
