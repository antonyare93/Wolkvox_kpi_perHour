import requests
import vars
import json

init_vars = vars.credentials


def skill4(fecha):

    for variable in init_vars:
        server_num = variable[0]
        url = f'https://wv{server_num}.wolkvox.com/api/v2/reports_manager.php?api=skill_4&skill_id=all&date_ini=' \
              f'{fecha[:8]}000000&date_end={fecha}5959'

        token_num = variable[1]

        payload = {}
        headers = {'wolkvox-token': f"{token_num}"}

        r = requests.get(url, headers=headers, data=payload, timeout=300)
        j_resultado = json.loads(r.content)
        print(url)
        return j_resultado


def skill5(fecha):
    for variable in init_vars:
        server_num = variable[0]
        url = f'https://wv{server_num}.wolkvox.com/api/v2/reports_manager.php?api=skill_5&skill_id=all&date_ini=' \
              f'{fecha[:8]}000000&date_end={fecha}5959'

        token_num = variable[1]

        payload = {}
        headers = {'wolkvox-token': f"{token_num}"}

        r = requests.get(url, headers=headers, data=payload, timeout=300)
        j_resultado = json.loads(r.content)
        print(url)
        return j_resultado


def agent6(fecha):
    for variable in init_vars:
        server_num = variable[0]
        url = f'https://wv{server_num}.wolkvox.com/api/v2/reports_manager.php?api=agent_6&date_ini={fecha[:8]}000000&' \
              f'date_end={fecha}5959'

        token_num = variable[1]

        payload = {}
        headers = {'wolkvox-token': f"{token_num}"}

        r = requests.get(url, headers=headers, data=payload, timeout=300)
        j_resultado = json.loads(r.content)
        print(url)
        return j_resultado
