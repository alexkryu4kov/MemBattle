import requests


class Parser:
    def __init__(self, api_version, method='https://api.vk.com/method/wall.get', **params):
        self.domains = self.get_domains('data/domains.txt')
        self.api_version = api_version
        self.params = params
        self.method = method

    @staticmethod
    def get_domains(filename):
        with open(filename, 'r') as f:
            domains = f.read()
        return domains.split('\n')

    def make_request(self):
        return requests.get(self.method, self.params).json()

    def parse_response(self):
        return self.parse_response()['response']['items']

    def to_sql(self):
        pass
