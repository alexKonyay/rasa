import requests
import yaml
from typing import Any, Dict, List, Text

style_db = {
    3: "Bitter",
    32: "Amber",
    36: "Blonde",
    44: "Stout"
}

brew_token = ''
with open('config.yml') as config_file:
    brew_token = yaml.load(config_file)['brew_token']


class Beer():
    """Beer"""

    def __init__(self, name: Text, desc: Text):
        self.name = name
        self.desc = desc


class BeerService():
    """Brewerydb service"""

    @staticmethod
    def style_by_id(id: int) -> Text:
        return style_db.get(id)

    @staticmethod
    def id_by_style(style: Text) -> int:
        return list(style_db.keys())[list(style_db.values()).index(style)]

    @staticmethod
    def get_random_beer(is_organic: bool, has_label: bool, style: Text) -> Beer:
        url = "https://sandbox-api.brewerydb.com/v2/beer/random"
        params = {
            "key": brew_token,
            "style": BeerService.id_by_style(style),
            "isOrganic": 'Y' if is_organic else 'N',
            "hasLabels": 'Y' if has_label else 'N'
        }
        response = requests.get(url=url, params=params).json()
        result_beer = Beer(response['data']['name'],
                           response['data']['style']['description'])

        return result_beer


class ChuckService():
    """chucknorris.io service"""

    @staticmethod
    def get_fact() -> Text:
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url=url)
        chuck_joke = response.json()['value']
        return chuck_joke
