def getipwithno0(ip: str):
    return ".".join([str(int(i)) for i in ip.split(".")])


if __name__ == "__main__":
    print(getipwithno0("255.024.101.001"))
