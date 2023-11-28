import requests
from src.services.utils.faculties import Faculty
from src.services.urls import get_base_url

def create_session(username, password, faculty):
    faculty = Faculty.FEUP
    session = requests.Session()
    login_payload = {'p_user': username, 'p_pass': password}
    login_url = f"{get_base_url(faculty)}/vld_validacao.validacao"
    login_response = session.post(login_url, data=login_payload)
    print(login_response.status_code)
    print(login_response.cookies)
    return session

def create_session_from_previous(faculty, session):
    faculty = Faculty.FEUP
    http_session = session.cookies._cookies['sigarra.up.pt']['/']['HTTP_SESSION'].value
    session_cookie = session.cookies._cookies['sigarra.up.pt']['/']['SI_SESSION'].value
    security_cookie = session.cookies._cookies['sigarra.up.pt']['/']['SI_SECURITY'].value
    new_session = continue_session(http_session, session_cookie, security_cookie)
    login_url = f"{get_base_url(faculty)}/vld_validacao.validacao"
    login_response = new_session.post(login_url)
    print(login_response.status_code)
    print(login_response.cookies)
    return new_session

def continue_session(http_session, session_cookie, security_cookie):
    session = requests.Session()
    session.cookies.set('HTTP_SESSION', http_session, domain='sigarra.up.pt')
    session.cookies.set('SI_SESSION', session_cookie, domain='sigarra.up.pt')
    session.cookies.set('SI_SECURITY', security_cookie, domain='sigarra.up.pt')
    # login_url = f"https://sigarra.up.pt/feup/pt/vld_validacao.validacao"
    # login_payload = {
    #     "p_user": "up201906681"
    # }
    # login_response = session.post(login_url, data=login_payload)
    # print(login_response.status_code)
    # print(login_response.cookies)
    return session
def login_credentials(username, password, faculty):
    faculty = Faculty.FEUP
    url = get_base_url(faculty)

    body = {
        'p_user': username,
        'p_pass': password
    }
    auth_url = f"{url}/vld_validacao.validacao"

    r = requests.post(url, data=body)
    session_cookie = r.cookies._cookies['sigarra.up.pt']['/']['HTTP_SESSION'].value
    si_session_cookie = r.cookies._cookies['sigarra.up.pt']['/']['SI_SESSION'].value
    si_security_cookie = r.cookies._cookies['sigarra.up.pt']['/']['SI_SECURITY'].value
    print(r.status_code)
    print(session_cookie)
    return [session_cookie, si_session_cookie, si_security_cookie]
