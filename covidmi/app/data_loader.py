import requests
from bs4 import BeautifulSoup


class DataLoader:
    def __init__(self, parser):
        self.parser = parser
        self.url = \
            'https://www.michigan.gov/coronavirus/' \
            + '0,9753,7-406-98163-520743--,00.html'
        self.response = requests.get(self.url)
        self.data = []

    def get_table_rows(self):
        soup = BeautifulSoup(self.response.text, "html.parser")
        table = soup.find('table')
        return table.findAll('tr')

    def load_data(self):

        table_rows = self.get_table_rows()
        for row in table_rows:
            table_data = row.findAll('td')

            if len(table_data) <= 0:
                continue

            county = self.parser.parse_county(table_data)
            cases = self.parser.parse_cases(table_data)
            deaths = self.parser.parse_deaths(table_data)

            if (self.parser.is_valid(county) is False):
                continue

            self.data.append({
                'county': county,
                'cases': cases,
                'deaths': deaths})

        return self.data
