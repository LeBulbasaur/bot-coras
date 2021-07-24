import requests

# get champion data

URL = "http://ddragon.leagueoflegends.com/cdn/11.12.1/data/pl_PL/champion.json"
r = requests.get(url=URL)
response = r.json()


def getChampionName(id):
    all_champion = response
    for champ in all_champion["data"]:
        if int(all_champion["data"][champ]["key"]) == id:
            return champ
    else:
        return None
