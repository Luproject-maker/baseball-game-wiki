import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file=process.argv[2]||path.join(root,'data/games.json');
const db=JSON.parse(fs.readFileSync(file,'utf8'));
const ids=new Set(),pks=new Set();let checks=0;
function ok(v,m){assert.ok(v,m);checks++}
for(const g of db.games){
 ok(/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(g.id),'id format');ok(!ids.has(g.id),'duplicate id');ids.add(g.id);ok(!pks.has(g.gamePk),'duplicate gamePk');pks.add(g.gamePk);
 ok(g.status==='Final','only final games');ok(/^\d{4}-\d{2}-\d{2}$/.test(g.date),'date format');ok(g.venue&&g.summary,'required text');ok(g.source.startsWith('https://statsapi.mlb.com/'),'official source');ok(g.sourcePage.startsWith('https://www.mlb.com/'),'official page');
 const raw=JSON.parse(fs.readFileSync(path.join(root,'sources',g.gamePk+'.json'),'utf8'));
 for(const side of ['away','home']){const t=g.teams[side],official=raw.liveData.linescore.teams[side];ok(t.innings.length>=9,'innings count');ok(t.innings.reduce((a,b)=>a+(b??0),0)===t.runs,'inning sum');
 for(const k of ['runs','hits','errors']){ok(Number.isInteger(t[k])&&t[k]>=0,k);ok(t[k]===official[k],'official '+k)}
 ok(JSON.stringify(t.innings)===JSON.stringify(raw.liveData.linescore.innings.map(i=>i[side]?.runs??null)),'official innings');
 for(const p of t.batters){ok(p.hits<=p.atBats,'hits <= AB');for(const k of ['atBats','runs','hits','rbi','baseOnBalls','strikeOuts','homeRuns'])ok(p[k]===null||(Number.isInteger(p[k])&&p[k]>=0),'batter '+k)}
 for(const p of t.pitchers)ok(/^\d+\.[012]$/.test(p.inningsPitched),'baseball IP');
 }
 const last=g.scoring.at(-1);ok(last.awayScore===g.teams.away.runs&&last.homeScore===g.teams.home.runs,'last scoring event');
}
const stats=Object.fromEntries(['LAD','NYY'].map(code=>{const teams=db.games.map(g=>Object.values(g.teams).find(t=>t.code===code));const wins=db.games.filter(g=>{const ts=Object.values(g.teams);return ts.find(t=>t.code===code).runs>ts.find(t=>t.code!==code).runs}).length;return [code,{wins,losses:db.games.length-wins,runs:teams.reduce((n,t)=>n+t.runs,0),hits:teams.reduce((n,t)=>n+t.hits,0),errors:teams.reduce((n,t)=>n+t.errors,0)}]}));
console.log(JSON.stringify({passed:true,checks,games:db.games.length,stats},null,2));
