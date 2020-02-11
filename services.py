import requests
import yaml


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

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        

class BeerService():
    """Brewerydb service"""
    @staticmethod
    def style_by_id(id):
        return style_db.get(id)
    
    @staticmethod
    def id_by_style(style):
        return list(style_db.keys())[list(style_db.values()).index(style)]
    
    @staticmethod
    def get_random_beer(is_organic, has_label, style):
        url = "https://sandbox-api.brewerydb.com/v2/beer/random"
        params = {
            "key": brew_token,
            "style": BeerService.id_by_style(style),
            "isOrganic": 'Y' if is_organic else 'N',
            "hasLabels": 'Y' if has_label else 'N'
        }
        response = requests.get(url=url,params=params).json()
        result_beer = Beer(response['data']['name'], response['data']['style']['description'])

        return result_beer


class ChuckService():
    """chucknorris.io service"""
    @staticmethod
    def get_fact():
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url=url)
        chuck_joke = response.json()['value']
        return chuck_joke
