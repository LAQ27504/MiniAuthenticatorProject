import base64
import time
import hmac
import hashlib
import secrets
from math import floor
import pyotp
VALID_DURATION = 30
TOKEN_LENGTH = 6
def generate_counter_value():
    """ Generated the counter avlue for the TOTP algorithm's hash generator."""
    timestamp = floor(time.time())
    counter_value = floor(timestamp / VALID_DURATION)

    return counter_value

def generate_hash(K: str, C: int):
    """
    Generates a TOTP compatible HMAC hash based on the shared secret (K) and 
    the current time window/ counter value C.
    """

    key_bytes = base64.b32decode(K)
    counter_bytes = C.to_bytes(8, byteorder = 'big')
    hash = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)
    return hash

def truncate_dynamically(hash: bytes):
    offset = hash[-1] & 0x0F
    truncated = hash[offset:offset+4]

    code_number = int.from_bytes(truncated, byteorder= 'big')
    return code_number & 0x7FFFFFFF

def truncated_hash_to_token(code: int, digits: int = TOKEN_LENGTH):
    code = code % 10 ** digits
    code = str(code)
    if len(code) < digits:
        code = code.rjust(digits, "0")
    return code

VALID_START = -2 
VALID_END = 2 

def generate_totp_tokens (
    key: str,
    timestep_start = VALID_START,
    timestep_end = VALID_END
):
    tokens: list[str] = []
    counter_value = generate_counter_value()

    hm = generate_hash(key, counter_value + 0)
    code = truncate_dynamically(hm)
    valid_token = truncated_hash_to_token(code)
    tokens.append(valid_token)

    return tokens

def generate_secret_key():
    random_bytes = secrets.token_bytes(20)
    return base64.b32encode(random_bytes).decode('utf-8')

if __name__ == "__main__":
<<<<<<< HEAD
    secret = "CLAH6OEOV52XVYTKHGKBERP42IUZHY4T"
    totp = pyotp.TOTP(secret)
    #client_token = input("Enter TOTP code from device: ")
=======
    secret = generate_secret_key()
    print(f"Generated secret key: {secret}")
    client_token = input("Enter TOTP code from device: ")
>>>>>>> a03d819a14c7983c6b0ecf99dac58fe7f5288505
    valid_tokens = generate_totp_tokens(secret)
    print(valid_tokens)
    print(totp.now())
    # if client_token in valid_tokens:
    #     print("Token is valid!")
    # else:
    #     print("Invalid token!")

