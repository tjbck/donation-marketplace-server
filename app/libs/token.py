from typing import Union
import jwt
import config
SECRET_KEY = config.SECRET_KEY

############################
# Token Decoder
############################


def decodeToken(token: str) -> Union[None, dict]:
    try:
        decoded = jwt.decode(token,
                             SECRET_KEY,
                             options={"verify_signature": False})
        return decoded
    except Exception as e:
        return None
