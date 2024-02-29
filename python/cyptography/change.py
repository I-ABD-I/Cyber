def encrypt(message, key):
    return "".join(
        [chr(ord(message[i]) ^ ord(key[i % len(key)])) for i in range(len(message))]
    )


def decrypt(message, key):
    return encrypt(message, key)


import base64 as b64

txt = "c0xCVlFTFl5BGFVbXUtTF19ZXVISS0NFVxhCWBJaUxdAXVdTSw=="
to_decode = b64.b64decode(txt).decode()

print(decrypt(to_decode, f"2867"))
print(decrypt(to_decode, f"2000")[::4])
