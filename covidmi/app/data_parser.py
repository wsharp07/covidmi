class DataParser:

    def is_valid(self, county):
        if (county == 'Other*'):
            return False
        if (county == 'Out of State'):
            return False
        if (county == 'Unknown'):
            return False
        if (county == 'Total'):
            return False
        if (county == 'County'):
            return False

        return True

    def parse_county(self, table_data):
        return table_data[0].text.strip()

    def parse_deaths(self, table_data):
        deaths = table_data[2].text.strip()
        if (deaths == ''):
            return 0
        return deaths

    def parse_cases(self, table_data):
        return table_data[1].text.strip()
