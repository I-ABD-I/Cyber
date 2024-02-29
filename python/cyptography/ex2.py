def encrypt1(message, key):
    return "".join([chr(ord(x) + int(key[0])) for x in message])


txt = "Wkh#dwwdfn#zloo#vwduw#dw#vxqvhw"
key = "309"


def decrypt(message, key):
    return "".join([chr(ord(x) - int(key[0])) for x in message])


print(decrypt(txt, key))
