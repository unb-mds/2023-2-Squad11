from .sessions import URL, HEADERS, create_request_session, get_session_cookie, get_response
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import List, Optional
from re import findall
import requests.utils
import requests

'''
Modo de uso:

1. É necessário ter o código do departamento escolhido.
Logo, temos a função get_list_of_departments() que retorna uma lista com os códigos dos departamentos.
2. É necessário ter o ano e o período.
3. É necessário ter uma instância da classe DisciplineWebScraper.

- Exemplo:
    department = "650"
    year = "2023"
    period = "2"
    disciplines = DisciplineWebScraper(department, year, period)
    disciplines.get_disciplines() # Retorna um dicionário com as disciplinas
'''


def get_list_of_departments(response=get_response(create_request_session())) -> Optional[List]:
    """Obtem a lista de departamentos da UnB."""
    soup = BeautifulSoup(
        response.content, "html.parser")  # Create a BeautifulSoup object
    # Find the <select> tag with id "formTurma:inputDepto"
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"})

    if departments is None:
        return None

    # Find all <option> tags (It contains all departments)
    options_tag = departments.find_all("option")
    department_ids = []

    for option in options_tag:
        value = option["value"]

        if (value != "0"):
            department_ids.append(value)

    return department_ids


def get_department_disciplines(department_id: str, current_year: str, current_period: str, url=URL, session=None, cookie=None) -> defaultdict[str, List[dict]]:
    """Obtem as disciplinas de um departamento"""
    discipline_scraper = DisciplineWebScraper(department_id, current_year, current_period, url, session, cookie)
    disciplines = discipline_scraper.get_disciplines()

    return disciplines

class DisciplineWebScraper:
    # Classe que faz o web scraping das disciplinas
    def __init__(self, department: str, year: str, period: str, url=URL, session=None, cookie=None):
        self.disciplines: defaultdict[str, List[dict]] = defaultdict(
            list)  # A dictionary with the disciplines
        self.department = department  # The department code
        self.period = period  # 1 for first semester and 2 for second semester
        self.year = year
        self.url = url  # The url of the web page
        self.data = {  # This data is necessary to make the post request
            "formTurma": "formTurma",
            "formTurma:inputNivel":	"",
            "formTurma:inputDepto":	self.department,
            "formTurma:inputAno": self.year,
            "formTurma:inputPeriodo": self.period,
            "formTurma:j_id_jsp_1370969402_11":	"Buscar",
            "javax.faces.ViewState": "j_id1"
        }

        if session is None:
            self.session = create_request_session()  # Create a request session
        else:
            self.session = session

        if cookie is None:
            self.cookie = get_session_cookie(self.session)
        else:
            self.cookie = cookie

    def get_response_from_disciplines_post_request(self) -> requests.Response:
        # Faz uma requisição POST para obter a resposta das turmas disponíveis
        response = self.session.post(
            self.url,
            headers=HEADERS,
            cookies=self.cookie,
            data=self.data
        )

        return response
    
    def get_teachers(self, data: list) -> list:
        teachers = []
        
        for teacher in data:
            teacher = teacher.replace("\n", "").replace(
                "\r", "").replace("\t", "")
            content = teacher.split('(')

            if (len(content) < 2):
                continue

            teachers.append(content[0].strip())

        if len(teachers) == 0:
            teachers.append("A definir")
        
        return teachers

    def get_schedules(self, data: str) -> list:
        regex = "\d+[MTN]\d+"
        occurrences = findall(regex, data)
        
        return occurrences
    
    def get_special_dates(self, data: str) -> list:
        date_format = "\d{2}\/\d{2}\/\d{4}"
        regex = f"\(({date_format}\s\-\s{date_format})\)"
        occurrences = findall(regex, data)
        
        return occurrences
    
    def get_week_days(self, data: str) -> list:
        hours_format = "\d+\:\d+"
        regex = f"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}"
        occurrences = findall(regex, data)
        
        return occurrences
    
    def make_disciplines(self, rows: str) -> None:
        if rows is None or not len(rows):
            return None
        
        aux_title_and_code = ""
        
        for discipline in rows:
            if discipline.find("span", attrs={"class": "tituloDisciplina"}) is not None:
                title = discipline.find(
                    "span", attrs={"class": "tituloDisciplina"})
                aux_title_and_code = title.get_text().strip('-')

            elif "linhaPar" in discipline.get("class", []) or "linhaImpar" in discipline.get("class", []):
                code, name = aux_title_and_code.split(' - ', 1)
                tables_data = discipline.find_all("td")

                '''
                    Parâmetros a serem salvos para cada disciplina:

                    Chave: Código da disciplina (string)
                    Valor: Lista de dicionários com as seguintes chaves:
                    - name: Nome da disciplina (string)
                    - class: Turma (str)
                    - teachers: Nome dos professores (Lista de strings)
                    - schedule: Código do horário (string)
                    - days: Dias da semana com horário (Lista de strings)
                '''

                teachers_with_workload = discipline.find(
                    "td", attrs={"class": "nome"}).get_text().strip().strip().split(')')
                schedule_context = tables_data[3].get_text().strip()
                
                class_code = tables_data[0].get_text().strip()
                classroom = tables_data[7].get_text().strip()
                schedule = self.get_schedules(schedule_context)
                special_dates = self.get_special_dates(schedule_context) 
                days = self.get_week_days(schedule_context)
                teachers = self.get_teachers(teachers_with_workload)
                
                self.disciplines[code].append({
                    "name": name,
                    "class_code": class_code,
                    "teachers": teachers,
                    "classroom": classroom,
                    "schedule": " ".join(schedule),
                    "special_dates": special_dates,
                    "days": days
                })

    def make_web_scraping_of_disciplines(self, response) -> None:
        # Faz o web scraping das disciplinas
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the <table> tag with class "listagem"
        tables = soup.find("table", attrs={"class": "listagem"})

        if tables is None:
            return None

        table_rows = tables.find_all("tr")  # Find all <tr> tags

        self.make_disciplines(table_rows)

    def get_disciplines(self) -> defaultdict[str, List[dict]]:
        # Retorna um dicionário com as disciplinas
        response = self.get_response_from_disciplines_post_request()
        self.make_web_scraping_of_disciplines(response)

        return self.disciplines
