// Shared data rules: browser rendering and Node regression tests use the same logic.
export const teamOf=(g,code)=>Object.values(g.teams).find(t=>t.code===code);
export function resultOf(g,code){
 const t=teamOf(g,code);if(!t)return null;
 const other=Object.values(g.teams).find(x=>x.code!==code);
 return t.runs===other.runs?'tie':t.runs>other.runs?'win':'loss';
}
export function selectGames(games,{year='all',series='all',team='all',result='all',query=''}={}){
 const q=query.trim().toLowerCase();
 return games.filter(g=>(year==='all'||String(g.season)===String(year))&&(series==='all'||g.seriesId===series)&&(team==='all'||!!teamOf(g,team))&&(result==='all'||(team!=='all'&&resultOf(g,team)===result))&&
 [g.date,g.venue,g.seriesName,String(g.season),...Object.values(g.teams).flatMap(t=>[t.name,t.code,...t.batters.map(p=>p.name),...t.pitchers.map(p=>p.name)])].join(' ').toLowerCase().includes(q))
 .sort((a,b)=>b.date.localeCompare(a.date)||a.gamePk-b.gamePk);
}
export function teamStats(games){
 const map=new Map();
 for(const g of games)for(const t of Object.values(g.teams)){
  if(!map.has(t.code))map.set(t.code,{code:t.code,name:t.name,games:0,wins:0,losses:0,ties:0,runs:0,hits:0,errors:0});
  const s=map.get(t.code);s.games++;s[resultOf(g,t.code)==='win'?'wins':resultOf(g,t.code)==='loss'?'losses':'ties']++;
  for(const k of ['runs','hits','errors'])s[k]+=t[k];
 }
 return [...map.values()].sort((a,b)=>b.wins-a.wins||a.code.localeCompare(b.code)).map(s=>({...s,winRate:s.games?(s.wins/s.games*100).toFixed(1)+'%':'—'}));
}
