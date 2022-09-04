import requests
from config import RECAPTCHA_SECRET

############################
# Recaptcha Handler
############################


def verify_recaptcha(token: str) -> bool:
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                      data={
                          "secret": RECAPTCHA_SECRET,
                          "response": token
                      }
                      )

    if(r.ok):
        res = r.json()
        print(res)
        if(res["success"]):
            return True
    return False
