import base64


class EncryptorService:

    def encode(self, string):
        return base64.b64encode(bytes(string, "utf-8"))

    def decode(self, string):
        return base64.b64decode(string).decode("utf-8", "ignore")


if __name__ == '__main__':
    es = EncryptorService()
    print(es.encode("hello"))
    print(es.decode(es.encode("hello")))