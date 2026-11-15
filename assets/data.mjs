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

export const teamColor=code=>({LAD:'#2879d0',NYY:'#283c5b',TEX:'#bd3544',AZ:'#087f82',ARI:'#087f82',TOR:'#245db6',MIL:'#896a27',TB:'#244b62',TBR:'#244b62'}[code]||'#527b65');
export function scoreProgress(g){
 const n=Math.max(g.teams.away.innings.length,g.teams.home.innings.length),points=[{inning:0,away:0,home:0,homePlayed:true}];let away=0,home=0;
 for(let i=0;i<n;i++){away+=g.teams.away.innings[i]??0;home+=g.teams.home.innings[i]??0;points.push({inning:i+1,away,home,homePlayed:g.teams.home.innings[i]!==null&&g.teams.home.innings[i]!==undefined})}return points;
}
export function scoringMoments(g){
 let previous={away:0,home:0};
 const actions={single:'擊出一壘安打',double:'擊出二壘安打',triple:'擊出三壘安打',home_run:'擊出全壘打',sac_fly:'擊出高飛犧牲打',field_out:'擊球出局',force_out:'造成封殺出局',fielders_choice:'靠野手選擇上壘',walk:'獲得四壞保送',hit_by_pitch:'獲得觸身球保送',field_error:'因守備失誤上壘'};
 return g.scoring.map((s,i)=>{const side=s.half==='top'?'away':'home',other=side==='away'?'home':'away',score={away:s.awayScore,home:s.homeScore},delta=score[side]-previous[side],before=previous[side]-previous[other],after=score[side]-score[other];
  const walkoff=side==='home'&&s.inning>=9&&i===g.scoring.length-1&&after>0&&before<=0&&score.home===g.teams.home.runs&&score.away===g.teams.away.runs;
  const label=walkoff?'再見得分':after===0?'追平比分':before<=0&&after>0?'超前比分':after>0?'擴大領先':'追近比分';
  const action=s.eventType==='home_run'&&delta===4&&s.rbi===4?'擊出滿貫全壘打':actions[s.eventType]||'完成得分打席';
  const text=`${s.batter||'進攻方'} ${action}，${g.teams[side].name}在這次進攻增加 ${delta} 分${Number.isInteger(s.rbi)?`（打者記 ${s.rbi} 打點）`:''}。`;
  previous=score;return {...s,label,text,delta,walkoff,side};
 });
}
export function playerHighlights(g){
 const both=Object.values(g.teams),batters=both.flatMap(t=>t.batters.map(p=>({...p,team:t.code}))),pitchers=both.flatMap(t=>t.pitchers.map(p=>({...p,team:t.code})));
 return [{key:'rbi',title:'打點焦點',unit:'RBI',pool:batters,note:'兩隊打者單場最多打點'},{key:'homeRuns',title:'長打火力',unit:'HR',pool:batters,note:'兩隊打者單場最多全壘打'},{key:'strikeOuts',title:'三振焦點',unit:'K',pool:pitchers,note:'兩隊投手單場最多三振'}].map(({pool,...item})=>{const eligible=pool.filter(p=>Number.isFinite(p[item.key])),max=Math.max(0,...eligible.map(p=>p[item.key]));return {...item,value:max,players:max>0?eligible.filter(p=>p[item.key]===max):[]}});
}
export function featuredGame(games){return [...games].sort((a,b)=>rank(b)-rank(a)||b.date.localeCompare(a.date))[0]||null;function rank(g){const moments=scoringMoments(g),last=moments.at(-1);return (last?.walkoff?100:0)+(last?.walkoff&&last.eventType==='home_run'&&last.rbi===4?100:0)+Math.max(0,g.teams.away.innings.length-9)*10}}
export function seriesSummary(games){
 const groups=new Map();for(const g of games){if(!groups.has(g.seriesId))groups.set(g.seriesId,{id:g.seriesId,name:g.seriesName,season:g.season,games:[]});groups.get(g.seriesId).games.push(g)}
 return [...groups.values()].sort((a,b)=>b.season-a.season).map(s=>({...s,games:s.games.sort((a,b)=>a.number-b.number),teams:teamStats(s.games)}));
}
