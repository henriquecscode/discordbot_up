
from datetime import datetime
from lxml import html
import urllib.parse

def get_office(session, number: int, date: datetime, start_time: float, duration:float, motivation="", observation="", name="") -> (bool, int | str | None):
    URL = "https://sigarra.up.pt/feup/pt/res_recursos_geral.pedidos_valida"

    
    date_format = "%Y-%m-%d"
    p_data_inicio_string = date.strftime(date_format)
    
    p_hora_inicio = str(start_time).replace(".", ",")
    p_duracao = str(duration).replace(".", ",")
    form = {
        "pi_avancada": 0,
        "pct_pedido_id": "",
        "pct_grupo_id": 7,
        "p_quantidade": 1,
        "p_data_fim": "",
        "p_tp_periodo": "",
        "p_periodo": "",
        "pi_exc_feriados": "",
        "p_data_inicio":p_data_inicio_string,
        "p_hora_inicio": p_hora_inicio,
        "p_duracao": p_duracao,
        "p_beneficiario": number,
        "p_beneficiario_nome": name,
        "p_automatica": "S"
    }
    # content type application/x-www-form-urlencoded
    headers = { "Content-Type": "application/x-www-form-urlencoded"}

    # Make form like pi_avancada=0&pct_pedido_id=&pct_grupo_id=7&p_quantidade=1&p_data_fim=&p_tp_periodo=&p_periodo=&pi_exc_feriados=&p_data_inicio=2023-12-29&p_hora_inicio=1%2C5&p_duracao=1%2C5&p_beneficiario=201906681&p_beneficiario_nome=Henrique+Costa+Sousa&p_automatica=S

    
    # response = session.post(url, data=form)
    response = session.post(URL, params=form, headers=headers)
    page_text = response.text

    tree = html.fromstring(page_text)

    redirect_meta_list = tree.xpath('//head/meta[@name="ROBOTS"]')
    if len(redirect_meta_list) > 0:
        redirect_meta = redirect_meta_list[0]
        # We got a good schedule
        a = redirect_meta.xpath('//a')[0]
        url = a.attrib['href']
        params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        office_request_id = int(params['pct_session_id'][0])
        response = session.get(url)
        
        new_form = params
        form['p_motivo'] = motivation
        form['p_obs'] = observation
        form['pi_confirmacao'] = 1
        form['pct_session_id'] = office_request_id
        form['pi_exc_feriados'] = 0
        del form['p_beneficiario_nome']

        plain_url = urllib.parse.urlparse(URL).scheme + "://" + urllib.parse.urlparse(url).netloc + urllib.parse.urlparse(url).path
        response = session.post(URL, params=form, headers=headers)

        page_text = response.text

        tree = html.fromstring(page_text)

        redirect_meta_list = tree.xpath('//head/meta[@name="ROBOTS"]')
        if len(redirect_meta_list) > 0:
            redirect_meta = redirect_meta_list[0]
            a = redirect_meta.xpath('//a')[0]
            url = a.attrib['href']
            return True, office_request_id
        else:
             # div with id involucro
            involucro_div = tree.xpath('//div[@id="involucro"]')[0]
            # div with id envolvente
            envolvente_div = involucro_div.xpath('//div[@id="envolvente"]')[0]
            #   div with id conteudo
            conteudo_div = envolvente_div.xpath('//div[@id="conteudo"]')[0]
            #     div with id conteudoinner
            conteudoinner_div = conteudo_div.xpath('//div[@id="conteudoinner"]')[0]
            lines = conteudoinner_div.text_content().split('\n')
            for i, line in enumerate(lines):
                if line.startswith("Este pedido não pode ser aceite porque tem pelo menos a seguinte falha:"):
                    if len(lines) > i+1:
                        return False, lines[i+1]
                    else:
                        return False, "Unknown error"
            return False, "Unknown error"
    else:
        involucro_div = tree.xpath('//div[@id="involucro"]')[0]
        # div with id envolvente
        envolvente_div = involucro_div.xpath('//div[@id="envolvente"]')[0]
        #   div with id conteudo
        conteudo_div = envolvente_div.xpath('//div[@id="conteudo"]')[0]
        #     div with id conteudoinner
        conteudoinner_div = conteudo_div.xpath('//div[@id="conteudoinner"]')[0]
        lines = conteudoinner_div.text_content().split('\n')
        lines = [line.strip() for line in lines if line.strip() != ""]
        return False, lines[1]

def cancel_office(session, request_id: int):
    URL = "https://sigarra.up.pt/feup/pt/res_recursos_geral.pedidos_cancelar"
    VIEW_URL = "https://sigarra.up.pt/feup/pt/res_recursos_geral.pedidos_view"

    form = {
        "pct_pedido_id": request_id,
    }

    # content type application/x-www-form-urlencoded
    headers = { "Content-Type": "application/x-www-form-urlencoded"}
    response = session.post(URL, params=form, headers=headers)
    page_text = response.text
    tree = html.fromstring(page_text)

    redirect_meta_list = tree.xpath('//head/meta[@name="ROBOTS"]')
    if len(redirect_meta_list) > 0:
        redirect_meta = redirect_meta_list[0]
        a = redirect_meta.xpath('//a')[0]
        url = a.attrib['href']

        if url == f"{VIEW_URL}?pct_pedido_id={request_id}":
            # response = session.get(url)
            return True, "Sucessfully canceled reservation"

    return False, "Could not cancel reservation"
