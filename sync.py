import requests
from config import (U_NAME, U_PASSWD)

s = requests.session()
url_login = "http://127.0.0.1:3030/login"
url_sync = "http://127.0.0.1:3030/sync"

payload = {
    "username": U_NAME,
    "password": U_PASSWD
}

req1 = s.post(url_login, data=payload)

req2 = s.get(url_sync)
