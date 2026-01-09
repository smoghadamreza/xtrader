import random
import string

def generate_secure_token(code_length: int = 6) -> str:
    char_set = (
        string.ascii_lowercase + string.ascii_uppercase + string.digits
    )
    return ''.join(random.choice(char_set) for _ in range(code_length))
