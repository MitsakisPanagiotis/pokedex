import requests

from .api_config import ENDPOINTS


class PokeAPI:
    def get(self, resource):
        return requests.get(ENDPOINTS[resource], timeout=5).json()

    def get_image(self, url):
        return requests.get(url).content

    def get_json(self, url):
        return requests.get(url).json()
