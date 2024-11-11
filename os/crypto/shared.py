"""
Written By : Aylon
Date       : 4 / 11 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

import socket

import Crypto
import Crypto.Cipher
import Crypto.Cipher.AES
import Crypto.Cipher.PKCS1_OAEP
import Crypto.PublicKey
import Crypto.PublicKey.RSA
import Crypto.Random

BLOCK_SIZE = 2**4


class EncSocketWrapper:
    """A socket Wrapper to handle Encription"""

    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
        public_key = self.sock.recv(1024)
        rnd = Crypto.Random.new()

        self.cipher = Crypto.Cipher.AES.new(
            aes := rnd.read(BLOCK_SIZE), Crypto.Cipher.AES.MODE_ECB
        )

        rsa = Crypto.PublicKey.RSA.import_key(public_key)
        rsa_cipher = Crypto.Cipher.PKCS1_OAEP.new(rsa)

        self.sock.send(rsa_cipher.encrypt(aes))

    def bind(self, host, port):
        return self.sock.bind((host, port))

    def listen(self):
        return self.sock.listen()

    def accept(self):
        sock, addr = self.sock.accept()
        rsa = Crypto.PublicKey.RSA.generate(2048)

        sock.send(rsa.public_key().export_key())
        aes_key = sock.recv(1024)
        rsa_cipher = Crypto.Cipher.PKCS1_OAEP.new(rsa)
        aes = Crypto.Cipher.AES.new(
            rsa_cipher.decrypt(aes_key), Crypto.Cipher.AES.MODE_ECB
        )
        enc_sock = EncSocketWrapper(sock)
        enc_sock.cipher = aes  # type: ignore
        return (enc_sock, addr)

    def send(self, data: bytes):
        padding = (BLOCK_SIZE - len(data) & (BLOCK_SIZE - 1)) & (BLOCK_SIZE - 1)
        data += b"\x00" * padding
        return self.sock.send(self.cipher.encrypt(data))  # type: ignore

    def recv(self, bufsize):
        enc_data = self.sock.recv(bufsize)
        return self.cipher.decrypt(enc_data).rstrip(b"\x00")  # type: ignore
