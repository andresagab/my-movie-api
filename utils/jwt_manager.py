from jwt import encode, decode

# create a token
def create_token(data: dict):
    token: str = encode(payload = data, key = "my_secrete_key", algorithm = "HS256")
    return token

# valid a generated token
def valid_token(token: str) -> dict:
    data: dict = decode(token, key="my_secrete_key", algorithms = ["HS256"])
    return data