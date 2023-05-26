import requests
import json
import pandas as pd

url = "https://api.sofascore.com/api/v1/sport/football/events/live"

headers = {
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "if-none-match": "W/^\^29c8426ecb^^",
    "origin": "https://www.sofascore.com",
    "referer": "https://www.sofascore.com/",
    "sec-ch-ua": "^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

jsondata = json.loads(requests.request("GET", url, headers=headers).text)
print(len(jsondata['events']))

res = []
for event in jsondata['events']:
    try:
        sport = event['tournament']['category']['sport']['name']
        league = event['tournament']['name']
        country = event['tournament']['category']['name']
        homeTeam = event['homeTeam']['name']
        awayTeam = event['awayTeam']['name']
        homeScore = event['homeScore']['current']
        awayScore = event['awayScore']['current']

        #print(sport, league, country, homeTeam, awayTeam, homeScore, awayScore)
        res.append([sport, league, country, homeTeam, awayTeam, homeScore, awayScore])
    except:
        continue
df = pd.DataFrame(res, columns=['Sport', 'League', 'Country', 'Home Team', 'Away Team', 'Home Score', 'Away Score'])

df.to_excel('firstres.xlsx')