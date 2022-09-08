import requests
import json


def enviar_telegram(foto, mensaje):
    files = foto
    r = requests.post(f'https://api.telegram.org/bot5162930037:AAGW9rOMXDzog_DtqShkgJwCAlCqLe1fDxM/sendPhoto?chat_id='
                      f'-1001789353905&caption={mensaje}', files=files)
    print(json.loads(r.content))
