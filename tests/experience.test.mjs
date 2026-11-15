import assert from 'node:assert/strict';
import fs from 'node:fs';
import {scoreProgress,scoringMoments,playerHighlights,featuredGame,seriesSummary} from '../assets/data.mjs';
const {games}=JSON.parse(fs.readFileSync(new URL('../data/games.json',import.meta.url),'utf8'));
const first=games.find(g=>g.id==='ws-2024-g1');
assert.equal(featuredGame(games).id,first.id);
const end=scoringMoments(first).at(-1);assert.equal(end.walkoff,true);assert.equal(end.delta,4);assert.match(end.text,/滿貫/);assert.equal(end.batter,'Freddie Freeman');
assert.equal(scoringMoments(first)[2].label,'追平比分');
assert.equal(scoreProgress(first).at(-1).away,3);assert.equal(scoreProgress(first).at(-1).home,6);
const h=playerHighlights(first).find(x=>x.key==='rbi');assert.equal(h.value,4);assert.equal(h.players[0].name,'Freddie Freeman');
for(const g of games){const p=scoreProgress(g).at(-1);assert.equal(p.away,g.teams.away.runs);assert.equal(p.home,g.teams.home.runs);assert.ok(scoringMoments(g).every(s=>s.delta>0));}
const groups=seriesSummary(games);assert.equal(groups.find(s=>s.season===2023).games.length,1);assert.equal(groups.find(s=>s.season===2024).games.length,5);
const tie=structuredClone(first);tie.teams.away.batters=[{name:'A',rbi:2,homeRuns:0}];tie.teams.home.batters=[{name:'B',rbi:2,homeRuns:0}];assert.equal(playerHighlights(tie)[0].players.length,2);assert.equal(playerHighlights(tie)[1].players.length,0);
const short=games.find(g=>g.teams.home.innings.at(-1)===null);if(short)assert.equal(scoreProgress(short).at(-1).homePlayed,false);
assert.equal(featuredGame([]),null);assert.deepEqual(seriesSummary([]),[]);
console.log('Experience checks passed: walk-off, translated summary, cumulative runs, tied leaders, incomplete series, unplayed innings.');
