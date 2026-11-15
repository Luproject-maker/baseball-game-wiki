"""Import immutable official MLB game snapshots, then derive the site dataset."""
import json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'sources'
RAW.mkdir(exist_ok=True)
(ROOT/'data').mkdir(exist_ok=True)
IDS = [775300, 775294, 775298, 775297, 775296]
NAMES = {'LAD':'洛杉磯道奇','NYY':'紐約洋基'}
def get(url, path):
    if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    with urllib.request.urlopen(url, timeout=45) as r: data=json.load(r)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data
games=[]
for n,pk in enumerate(IDS,1):
    url=f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live'
    d=get(url,RAW/f'{pk}.json'); live=d['liveData']; gd=d['gameData']; line=live['linescore']; box=live['boxscore']
    teams={}
    for side in ['away','home']:
        t=gd['teams'][side]; b=box['teams'][side]; total=line['teams'][side]
        batters=[]; pitchers=[]
        for pid in b['batters']:
            p=b['players'][f'ID{pid}']; s=p['stats'].get('batting',{})
            if not s: continue
            batters.append(dict(name=p['person']['fullName'],position=p['position']['abbreviation'],**{k:s.get(k) for k in ['atBats','runs','hits','rbi','baseOnBalls','strikeOuts','homeRuns']}))
        for pid in b['pitchers']:
            p=b['players'][f'ID{pid}']; s=p['stats']['pitching']
            pitchers.append(dict(name=p['person']['fullName'],**{k:s.get(k) for k in ['inningsPitched','hits','runs','earnedRuns','baseOnBalls','strikeOuts','numberOfPitches']}))
        ab=t['abbreviation']
        teams[side]=dict(code=ab,name=NAMES.get(ab,t['name']),runs=total['runs'],hits=total['hits'],errors=total['errors'],innings=[i.get(side,{}).get('runs') for i in line['innings']],batters=batters,pitchers=pitchers)
    scoring=[]
    plays=live['plays']['allPlays']
    for i in live['plays']['scoringPlays']:
        p=plays[i]; scoring.append(dict(inning=p['about']['inning'],half=p['about']['halfInning'],description=p['result']['description'],awayScore=p['result']['awayScore'],homeScore=p['result']['homeScore']))
    winner='home' if teams['home']['runs']>teams['away']['runs'] else 'away'
    g=dict(id=f'ws-2024-g{n}',gamePk=pk,number=n,date=gd['datetime']['officialDate'],venue=gd['venue']['name'],status=gd['status']['abstractGameState'],teams=teams,scoring=scoring,source=url,sourcePage=f'https://www.mlb.com/gameday/{pk}/final/box',retrieved='2026-11-15',summary=f"{teams[winner]['name']}以 {teams[winner]['runs']} 比 {teams['away' if winner=='home' else 'home']['runs']}獲勝；全場共進行 {len(line['innings'])} 局。",reflection=None)
    games.append(g)
out=dict(title='2024 世界大賽',scope='2024 世界大賽全部五場；日期採球場當地官方賽事日期。',games=games)
(ROOT/'data/games.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Imported',len(games),'official MLB games')
