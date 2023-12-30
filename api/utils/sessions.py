from requests import Session, Response, cookies
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from typing import List

"""Este módulo contém funções necessárias para realizar uma requsição ao SIGAA
corretamente.
"""

URL = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

"""Cria uma sessão de requisição e retorna um objeto Session."""
def create_request_session() -> Session:
    session = Session() # Create a persistent request session
    retry = Retry(connect=3, backoff_factor=0.5) # Create a retry object
    adapter = HTTPAdapter(max_retries=retry) # Try to make the request 3 times
    session.mount('https://', adapter) # Mount the adapter to the session

    return session

"""Obtem a resposta da requisição ao SIGAA e retorna um objeto Response."""
def get_response(session: Session) -> Response:
    response = session.get(url=URL, headers=HEADERS) # Make a get request to the url

    return response

"""Obtem o cookie da sessão de requisição necessário para acessar a pagina de turmas
e retorna um cookie jar."""
def get_session_cookie(session: Session) -> cookies.RequestsCookieJar: # pragma: no cover
    response = get_response(session) # Get the response from the request session
    cookie = response.cookies.get_dict() # Get the cookie from the response
    cookie_jar = cookies.RequestsCookieJar() # Create a cookie jar
    cookie_jar.update(cookie) # Update the cookie jar with the cookie

    return cookie_jar

"""Obtem o ano e o período atual e retorna uma lista com esses valores."""
def get_current_year_and_period(date: datetime | None = datetime.now()) -> List[str | str]:
    if date is None:
        date = datetime.now()
    
    current_year = date.year
    period = "1"

    # Se a data atual estiver entre 2 de maio e 1 de janeiro do próximo ano, o período é 2.
    if datetime(current_year, 5, 2) <= date <= datetime(current_year + 1, 1, 1):
        period = "2"

    return [str(current_year), period]

"""Obtem o ano e o período seguinte e retorna uma lista com esses valores."""
def get_next_period(date: datetime | None = None) -> List[str | str]:
    date = get_current_year_and_period(date)

    if date[1] == "1":
        date[1] = "2"
        return date

    date[0] = str(int(date[0]) + 1)
    date[1] = "1"

    return date

def get_previous_period(date: datetime | None = None) -> List[str | str]:
    date = get_current_year_and_period(date)

    if date[1] == "2":
        date[1] = "1"
        return date

    date[0] = str(int(date[0]) - 1)
    date[1] = "2"

    return date
