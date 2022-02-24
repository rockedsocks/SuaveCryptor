from cryptography.fernet import Fernet

# input: the string to encode/decode
# return: the encoded/decoded string, key (utf-8)
def encrypt(s, key=""):
    print(key)
    if key != "":
        key = bytes(key, encoding="utf-8")
        fernet = Fernet(key)
    else:
        key = Fernet.generate_key()
        fernet = Fernet(key)
    return [key.decode("utf-8"), fernet.encrypt(bytes(s, encoding="utf-8")).decode("utf-8")]


def decrypt(s, key): # s and key must be plain text
    print(key)
    fernet = Fernet(bytes(key, encoding="utf-8"))
    return fernet.decrypt(bytes(s, encoding="utf-8")).decode("utf-8")

def test(): # basic test of encryption and decryption
    encrypts = encrypt("test")
    print(encrypts[0] + "\n" + encrypts[1])
    print(decrypt(encrypts[1], encrypts[0]))
