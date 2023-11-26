from string import ascii_letters as letters, digits
from collections import defaultdict
from rest_framework.test import APITestCase
from utils import web_scraping as wbp
from django.urls import reverse
from pathlib import Path
import random
import json

class WebScrapingTest(APITestCase):

    def cookie(self):
        cookie = ""
        for _ in range(32):
            cookie += random.choice(letters + digits)

        return cookie

    def make_disciplines_request(self, path_name: str):
        current_path = Path(__file__).parents[1].absolute()
        infos_path = current_path / f"mock/infos.json"

        with open(infos_path) as json_file:
            data = json.load(json_file)

            year = data.get('year')
            period = data.get('period')
            department = data.get('department')

        url = reverse(f'utils:sigaa', kwargs={"path": path_name})
        args = [department, year, period, url, self.client, self.cookie()]
        disciplines = wbp.get_department_disciplines(*args)

        return disciplines

    def test_get_list_of_departments(self):
        response = self.client.get(reverse('utils:sigaa', kwargs={"path": "sigaa"}))

        departments = wbp.get_list_of_departments(response)
        self.assertEqual(type(list()), type(departments))
        if len(departments):
            self.assertEqual(type(str()), type(departments[0]))

    def test_get_list_of_departments_when_empty(self):
        response = self.client.get(reverse('utils:sigaa', kwargs={"path": "empty"}))

        departments = wbp.get_list_of_departments(response)
        self.assertIsNone(departments)

    def test_get_department_disciplines(self):
        disciplines = self.make_disciplines_request('sigaa')

        self.assertEqual(type(disciplines), type(defaultdict(str)))
        if len(disciplines):
            keys = list(disciplines.keys())
            class_discipline = disciplines.get(keys[0])[0]

            self.assertTrue('name' in class_discipline)
            self.assertTrue('class_code' in class_discipline)
            self.assertTrue('teachers' in class_discipline)
            self.assertTrue('schedule' in class_discipline)
            self.assertTrue('days' in class_discipline)

    def test_get_department_disciplines_when_empty(self):
        disciplines = self.make_disciplines_request('empty')

        self.assertFalse(len(disciplines))

    def test_get_department_disciplines_when_without_tr_html_tag(self):
        disciplines = self.make_disciplines_request('table')

        self.assertFalse(len(disciplines))
        