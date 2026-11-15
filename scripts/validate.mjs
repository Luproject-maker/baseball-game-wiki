import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {teamStats} from '../assets/data.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file=process.argv[2]||path.join(root,'data/games.json');
const db=JSON.parse(fs.readFileSync(file,'utf8'));
const ids=new Set(),pks=new Set(),series=new Map(),seriesNumbers=new Set();let checks=0;
function ok(v,m){assert.ok(v,m);checks++}
for(const g of db.games){
 ok(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(g.id),'id format');ok(!ids.has(g.id),'duplicate id');ids.add(g.id);ok(!pks.has(g.gamePk),'duplicate gamePk');pks.add(g.gamePk);
 ok(g.status==='Final','only final games');ok(/^\d{4}-\d{2}-\d{2}$/.test(g.date),'date format');ok(g.venue&&g.summary,'required text');ok(g.source.startsWith('https://statsapi.mlb.com/'),'official source');ok(g.sourcePage.startsWith('https://www.mlb.com/'),'official page');
 ok(Number.isInteger(g.season)&&g.season>=1876,'season');ok(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(g.seriesId),'seriesId');ok(typeof g.seriesName==='string'&&g.seriesName.trim().length>0,'seriesName');ok(Number.isInteger(g.number)&&g.number>0,'game number');
 const seriesKey=JSON.stringify([g.season,g.seriesName]);ok(!series.has(g.seriesId)||series.get(g.seriesId)===seriesKey,'series metadata consistent');series.set(g.seriesId,seriesKey);
 const gameKey=JSON.stringify([g.seriesId,g.number]);ok(!seriesNumbers.has(gameKey),'unique series game number');seriesNumbers.add(gameKey);
 const raw=JSON.parse(fs.readFileSync(path.join(root,'sources',g.gamePk+'.json'),'utf8'));
 ok(g.season===Number(raw.gameData.game.season),'official season');ok(g.date===raw.gameData.datetime.officialDate,'official date');
 for(const side of ['away','home']){const t=g.teams[side],official=raw.liveData.linescore.teams[side];ok(t.code===raw.gameData.teams[side].abbreviation,'official team');ok(t.innings.length>0,'innings count');ok(t.innings.reduce((a,b)=>a+(b??0),0)===t.runs,'inning sum');
 for(const k of ['runs','hits','errors']){ok(Number.isInteger(t[k])&&t[k]>=0,k);ok(t[k]===official[k],'official '+k)}
 ok(JSON.stringify(t.innings)===JSON.stringify(raw.liveData.linescore.innings.map(i=>i[side]?.runs??null)),'official innings');
 for(const p of t.batters){ok(p.hits<=p.atBats,'hits <= AB');for(const k of ['atBats','runs','hits','rbi','baseOnBalls','strikeOuts','homeRuns'])ok(p[k]===null||(Number.isInteger(p[k])&&p[k]>=0),'batter '+k)}
 for(const p of t.pitchers)ok(/^\d+\.[012]$/.test(p.inningsPitched),'baseball IP');
 }
 const last=g.scoring.at(-1);ok(last?last.awayScore===g.teams.away.runs&&last.homeScore===g.teams.home.runs:g.teams.away.runs===0&&g.teams.home.runs===0,'last scoring event');
}
const stats=teamStats(db.games);
console.log(JSON.stringify({passed:true,checks,games:db.games.length,stats},null,2));
