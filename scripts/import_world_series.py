"""Append completed World Series games using authoritative schedule game numbers."""
import argparse,json,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from import_mlb import ROOT,RAW,get,convert_game

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--years',type=int,nargs='+',required=True);args=parser.parse_args()
 dest=ROOT/'data/games.json';db=json.loads(dest.read_text(encoding='utf-8'));existing={g['gamePk'] for g in db['games']};planned=[]
 for year in args.years:
  url=f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={year}-10-01&endDate={year}-11-15&gameTypes=W'
  path=RAW/f'schedule-{year}-world-series.json'
  with urllib.request.urlopen(url,timeout=45) as response:schedule=json.load(response)
  path.write_text(json.dumps(schedule,ensure_ascii=False,indent=2),encoding='utf-8')
  games=[g for day in schedule.get('dates',[]) for g in day.get('games',[]) if g.get('gameType')=='W' and g['status']['abstractGameState']=='Final']
  if not games:raise ValueError(f'No completed official World Series games for {year}; no games changed')
  for g in games:
   if not isinstance(g.get('seriesGameNumber'),int):raise ValueError('Missing official series game number')
   if g['gamePk'] not in existing:
    if any(x['seriesId']==f'mlb-{year}-world-series' and x['number']==g['seriesGameNumber'] for x in db['games']):raise ValueError('Existing series game number conflict')
    planned.append((year,g));existing.add(g['gamePk'])
 def download(item):
  year,g=item;pk=g['gamePk'];get(f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live',RAW/f'{pk}.json');return item
 with ThreadPoolExecutor(max_workers=3) as pool:downloaded=list(pool.map(download,planned))
 new=[]
 for year,official in downloaded:
  g=convert_game(official['gamePk'],year,f'mlb-{year}-world-series',f'{year} 世界大賽',official['seriesGameNumber'])
  assert g['teams']['away']['runs']==official['teams']['away']['score'] and g['teams']['home']['runs']==official['teams']['home']['score']
  new.append(g)
 db['games'].extend(new);db['games'].sort(key=lambda g:(g['date'],g['gamePk']));temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(dest)
 print(json.dumps({'added':len(new),'total':len(db['games']),'seasons':sorted(set(g['season'] for g in db['games']))}))
if __name__=='__main__':main()
