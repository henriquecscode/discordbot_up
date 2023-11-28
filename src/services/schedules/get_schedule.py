import requests

def get_schedule_from_session(session):
    url = "https://sigarra.up.pt/feup/pt/hor_geral.estudantes_view?pv_fest_id=1313647&pv_ano_lectivo=2023&pv_periodos=1"
    response = session.get(url)
    status_code = response.status_code
    # print(response.text.encode('utf8'))
    print(status_code)
    
def get_schedule_from_cookie(session_cookie):
    url = "https://sigarra.up.pt/feup/pt/hor_geral.estudantes_view?pv_fest_id=1313647&pv_ano_lectivo=2023&pv_periodos=1"

    payload={}
    cookies = {
        "HTTP_SESSION":283917821,
        "SI_SESSION":181766769,
        "SI_SECURITY":"LXN1XFQ6aXguOi1ddyVeJGJvRD41Y2FfYXg2Sm4mY2J1I1VcWCcyNUk4c3sxeTJicFZRWT86KW9tLShDzzHPzRes02Hw8YgxSpOOumGhWPO3Y9kABvLG1+/ay9IZGtE2TzwWVwTZWPGXrWKxdww3DEkq8TlOyeu1"
    }
    cookie_header = ';'.join([f'{name}, {value}' for name, value in cookies.items()])
    headers = {
        'Cookie': cookie_header
        }
    print(headers)
    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    # print(response.text.encode('utf8'))

