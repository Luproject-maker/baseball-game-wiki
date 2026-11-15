import fs from 'node:fs';
import assert from 'node:assert/strict';
import {selectGames,teamStats,seriesSummary,scoreProgress,scoringMoments} from '../assets/data.mjs';
const {games}=JSON.parse(fs.readFileSync(new URL('../data/games.json',import.meta.url),'utf8'));
for(const [year,expected] of [[2025,7],[2026,5]]){
 const schedule=JSON.parse(fs.readFileSync(new URL(`../sources/schedule-${year}-world-series.json`,import.meta.url),'utf8'));
 const official=schedule.dates.flatMap(d=>d.games).filter(g=>g.gameType==='W'&&g.status.abstractGameState==='Final');
 const selected=selectGames(games,{year:String(year),series:`mlb-${year}-world-series`});assert.equal(selected.length,expected);assert.equal(official.length,expected);
 for(const o of official){const g=selected.find(x=>x.gamePk===o.gamePk);assert.ok(g);assert.equal(g.number,o.seriesGameNumber);assert.equal(g.date,o.officialDate);assert.equal(g.teams.away.runs,o.teams.away.score);assert.equal(g.teams.home.runs,o.teams.home.score);const p=scoreProgress(g).at(-1);assert.equal(p.away,g.teams.away.runs);assert.equal(p.home,g.teams.home.runs);assert.ok(scoringMoments(g).every(s=>s.delta>0))}
 assert.equal(teamStats(selected).reduce((n,t)=>n+t.games,0),expected*2);
}
assert.equal(games.length,18);assert.equal(seriesSummary(games).length,4);
assert.equal(teamStats(selectGames(games,{year:'2025'})).find(t=>t.code==='LAD').wins,4);
assert.equal(teamStats(selectGames(games,{year:'2026'})).find(t=>t.code==='MIL').wins,4);
assert.equal(selectGames(games,{year:'2026',team:'LAD'}).length,0);
assert.equal(games.find(g=>g.gamePk===813032).teams.away.innings.length,18);
console.log('2025/2026 season checks passed: all official game IDs, series numbers, final scores, 18-inning game, scoped records.');
