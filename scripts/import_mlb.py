"""Import immutable official MLB game snapshots, then derive the site dataset."""
import argparse, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'sources'
RAW.mkdir(exist_ok=True)
(ROOT/'data').mkdir(exist_ok=True)
IDS = [775300, 775294, 775298, 775297, 775296]
NAMES = {'LAD':'洛杉磯道奇','NYY':'紐約洋基','TEX':'德州遊騎兵','AZ':'亞利桑那響尾蛇','ARI':'亞利桑那響尾蛇'}
def get(url, path):
    if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    with urllib.request.urlopen(url, timeout=45) as r: data=json.load(r)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data
def convert_game(pk,season,series_id,series_name,n):
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
        p=plays[i]; scoring.append(dict(inning=p['about']['inning'],half=p['about']['halfInning'],description=p['result']['description'],awayScore=p['result']['awayScore'],homeScore=p['result']['homeScore'],eventType=p['result']['eventType'],batter=p['matchup']['batter']['fullName'],rbi=p['result'].get('rbi')))
    if gd['status']['abstractGameState']!='Final': raise ValueError('Only completed games can be imported')
    if int(gd['game']['season'])!=season: raise ValueError('Season does not match official game')
    a,h=teams['away'],teams['home'];winner='home' if h['runs']>a['runs'] else 'away'
    summary=(f"{teams[winner]['name']}以 {teams[winner]['runs']} 比 {teams['away' if winner=='home' else 'home']['runs']} 獲勝" if a['runs']!=h['runs'] else f"兩隊以 {a['runs']} 比 {h['runs']} 和局")+f"；全場共進行 {len(line['innings'])} 局。"
    # Keep historical URLs stable for the original five games.
    game_id=f'ws-2024-g{n}' if series_id=='mlb-2024-world-series' else f'mlb-{pk}'
    return dict(id=game_id,gamePk=pk,season=season,seriesId=series_id,seriesName=series_name,number=n,date=gd['datetime']['officialDate'],venue=gd['venue']['name'],status=gd['status']['abstractGameState'],teams=teams,scoring=scoring,source=url,sourcePage=f'https://www.mlb.com/gameday/{pk}/final/box',retrieved='2026-11-15',summary=summary,reflection=None)

def main():
    parser=argparse.ArgumentParser(description='Append an official MLB game without overwriting existing records.')
    parser.add_argument('--game-pk',type=int);parser.add_argument('--season',type=int)
    parser.add_argument('--series-id');parser.add_argument('--series-name');parser.add_argument('--number',type=int)
    args=parser.parse_args();dest=ROOT/'data/games.json'
    db=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else dict(title='棒球逐場賽事紀錄站',scope='依年度與系列賽持續收錄 MLB 已結束賽事；日期採球場當地官方日期。',games=[])
    if args.game_pk:
        if not all([args.season,args.series_id,args.series_name,args.number]):parser.error('game-pk requires season, series-id, series-name and number')
        import re
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.series_id) or args.number<1:parser.error('Invalid series-id or number')
        if any(g['gamePk']==args.game_pk for g in db['games']):parser.error('This gamePk already exists; no data was changed')
        same=[g for g in db['games'] if g['seriesId']==args.series_id]
        if any(g['season']!=args.season or g['seriesName']!=args.series_name or g['number']==args.number for g in same):parser.error('Series metadata or game number conflict')
        new=[convert_game(args.game_pk,args.season,args.series_id,args.series_name,args.number)]
    else:
        existing={g['gamePk'] for g in db['games']}
        new=[convert_game(pk,2024,'mlb-2024-world-series','2024 世界大賽',n) for n,pk in enumerate(IDS,1) if pk not in existing]
    if any(g['id'] in {x['id'] for x in db['games']} for g in new):raise ValueError('Duplicate game id')
    db['games'].extend(new);db['games'].sort(key=lambda g:(g['date'],g['gamePk']))
    temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(dest)
    print('Added',len(new),'games; total',len(db['games']))
if __name__=='__main__': main()
