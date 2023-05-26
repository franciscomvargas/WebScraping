import json
import pandas as pd
with open('scores.json', 'r') as f:
    jsondata = json.load(f)


res = []
print(len(jsondata['events']))
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


