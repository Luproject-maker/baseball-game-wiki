from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
doc=Document(); sec=doc.sections[0]
sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.5); sec.bottom_margin=Cm(1.5); sec.left_margin=Cm(2);sec.right_margin=Cm(2)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 s=doc.styles[name];s.font.name='Microsoft JhengHei';s._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei');s.font.color.rgb=RGBColor(0,0,0)
 s.paragraph_format.space_after=Pt(7)
doc.styles['Normal'].font.size=Pt(10.5);doc.styles['Normal'].paragraph_format.line_spacing=1.12
doc.styles['Title'].font.size=Pt(25);doc.styles['Heading 1'].font.size=Pt(16);doc.styles['Heading 2'].font.size=Pt(12)
header=sec.header.paragraphs[0];header.text='Homework 9   建立自己的 AGENTS.md';header.style='Caption'
doc.styles['Caption'].font.color.rgb=RGBColor(0,0,0)
f=sec.footer.paragraphs[0];f.alignment=2
f.add_run('棒球逐場賽事紀錄站   |   ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
def p(t):return doc.add_paragraph(t)
def h(t):doc.add_heading(t,1)
def picture(name,width=6.45):
 path=OUT/'screenshots'/name
 if path.exists():doc.add_picture(str(path),width=Inches(width))
def hyperlink(label,url):
 para=doc.add_paragraph();rel=para.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
 a=OxmlElement('w:hyperlink');a.set(qn('r:id'),rel);r=OxmlElement('w:r');props=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'174F45');props.append(color);r.append(props);t=OxmlElement('w:t');t.text=label;r.append(t);a.append(r);para._p.append(a)
def table(headers,rows):
 t=doc.add_table(rows=1, cols=len(headers));t.autofit=False
 if len(headers)==2:
  t.columns[0].width=Cm(3.3);t.columns[1].width=Cm(13.7)
 for c,s in zip(t.rows[0].cells,headers):c.text=s
 for row in rows:
  for c,s in zip(t.add_row().cells,row):c.text=str(s)
 for i,row in enumerate(t.rows):
  for j,c in enumerate(row.cells):
   pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for side in ['top','left','bottom','right']:
    z=OxmlElement('w:'+side);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'D9D9D9');b.append(z)
   pr.append(b);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E9EEEA' if i==0 else ('F7F8F7' if i%2==0 else 'FFFFFF'));pr.append(shade)
   if len(headers)==2:c.width=Cm(3.3 if j==0 else 13.7)
   for para in c.paragraphs:
    para.paragraph_format.space_after=Pt(3);para.paragraph_format.space_before=Pt(3)
    for r in para.runs:r.font.size=Pt(9);r.bold=i==0
 return t

doc.add_paragraph('棒球逐場賽事紀錄站',style='Title')
doc.add_paragraph('逐場數據與 AI 協作開發規則',style='Subtitle')
p('生成式 AI 課程 Homework 9 作業說明　｜　2026 年 11 月 15 日')
h('專案簡介')
p('本專案將棒球逐場比賽資料整理成可搜尋、可閱讀與持續擴充的網站，支援不同年度、系列賽與球隊。首批收錄 2024 世界大賽五場及 2023 世界大賽第五場，共六場官方比賽，提供逐局比分、球員投打數據與目前範圍的累計統計。2023 年僅收錄一場，不代表完整系列賽。')
p('本次作業的核心是先建立 AGENTS.md，明確定義資料與開發方式，再讓 AI 依規則完成網站。後續只要加入符合格式的賽事資料，共用程式就能產生新卡片、單場頁及統計，不必重做整個網站。')
h('專案與網站連結')
hyperlink('GitHub Repository  https://github.com/Luproject-maker/baseball-game-wiki','https://github.com/Luproject-maker/baseball-game-wiki')
hyperlink('公開網站  https://luproject-maker.github.io/baseball-game-wiki/','https://luproject-maker.github.io/baseball-game-wiki/')
hyperlink('開發規則  AGENTS.md','https://github.com/Luproject-maker/baseball-game-wiki/blob/main/AGENTS.md')
picture('home-v2.png')
p('圖一　首頁沿用球場深綠、米白與金黃，加入年度、系列賽、球隊與勝敗分類。')

doc.add_page_break();h('網站功能與資料來源')
table(['頁面','主要內容'],[['賽事紀錄','年度、系列賽、球隊、勝敗與搜尋取交集；分類自動產生。'],['單場數據','逐局記分板、投打成績、得分事件；標題使用所屬系列賽。'],['數據總覽','依目前篩選範圍計算各隊出賽場數、勝敗與得分資料。'],['關於本站','說明資料來源、數據記法及維護者新增比賽的方式。']])
p('資料來自 MLB 官方 Stats API，擷取日期為 2026 年 11 月 15 日。每場保留 gamePk、官方賽事頁、API 連結與 sources 原始 JSON 快照，供重現及核對。網頁日期採球場當地官方日期，不混用台灣跨日日期。')
hyperlink('來源範例  2023 世界大賽第五場官方 API','https://statsapi.mlb.com/api/v1.1/game/748534/feed/live')
table(['範圍','場次','客隊與比分','主隊'],[['2024 世界大賽','G1','洋基 3 : 6','道奇'],['2024 世界大賽','G2','洋基 2 : 4','道奇'],['2024 世界大賽','G3','道奇 4 : 2','洋基'],['2024 世界大賽','G4','道奇 4 : 11','洋基'],['2024 世界大賽','G5','道奇 7 : 6','洋基'],['2023 世界大賽','G5','遊騎兵 5 : 0','響尾蛇']])
picture('game-v2.png',6.1)
p('圖二　新增年度與不同球隊的單場頁沿用既有版型，無需為新球隊重寫網頁。')

doc.add_page_break();h('AGENTS.md 如何規範 AI')
p('AGENTS.md 放在專案根目錄，讓 AI 開始工作時先理解專案目的、內容界線與完成標準。規則採用具體欄位與操作流程，避免只要求「美觀」或「正確」而缺少可執行的方法。')
table(['規則面向','具體要求'],[['專案與結構','原生 HTML、CSS、JavaScript、JSON；data.mjs 共用篩選與統計邏輯。'],['視覺一致性','共用深綠、米白與金黃配色；共用頁首、卡片、表格；手機版單欄。'],['內容與分類','固定 season、seriesId、seriesName；id、gamePk 及系列賽場次不可重複。'],['數據可信度','核對官方來源；缺漏為 null；未進行半局顯示 X；5.2 局不可當十進位。'],['新增流程','命令追加資料，保留已有比賽；新年度、分類、球隊自動出現在選單。'],['統計與驗證','各隊分開計算場次，統計限目前篩選範圍；新增後執行資料與回歸檢查。']])
h('檔案如何分工')
p('index.html 是共用入口；assets/app.js 呈現頁面；assets/data.mjs 提供可測試的共用篩選與統計；assets/style.css 統一樣式；data/games.json 保存資料；sources 保存官方來源；scripts 與 tests 提供匯入、驗證及擴充紀錄。')
h('AI 協作與 LLM Wiki 的對應')
p('課堂的 LLM Wiki 與個人化 Wikipedia 提供了整理和累積知識的方向。本專案採用相同的資料整理思路，將「官方原始紀錄 → 固定格式資料 → 可瀏覽網頁」串接起來。網站沒有額外宣稱具備聊天機器人或即時檢索功能；AI 的角色是依開發規則整理資料與維護程式。')
h('未來新增內容的指令範例')
p('「請先閱讀 AGENTS.md，依官方 gamePk 新增一場其他年度的比賽，填妥 season、seriesId、seriesName 及 number，不覆蓋舊資料。確認新分類自動出現，篩選與統計正常，並記錄檢查結果。」')

doc.add_page_break();h('擴充示範與驗證結果')
p('原先已完成四場新增至五場的擴充測試。本次進一步將網站改成跨年度結構，再用官方 gamePk 748534 的匯入命令，新增 2023 世界大賽第五場，實際驗證非道奇與洋基的比賽也能呈現。過程保存在 tests/extension-log.md。')
table(['項目','原先資料','跨年度新增後'],[['收錄場次','5 場','6 場'],['年度與分類','2024 世界大賽','2023 與 2024 世界大賽'],['球隊數量','2 隊','4 隊'],['球隊出賽場數','道奇與洋基各 5 場','兩隊仍各 5 場，新增兩隊各 1 場'],['資料檢查','995 項通過','1,248 項通過'],['重複匯入','未提供追加介面','拒絕重複 gamePk，原資料不變']])
p('瀏覽器確認 2023 年加遊騎兵勝場只顯示一場；切換總覽仍保持相同範圍。2023 年與道奇交集顯示空結果。Node 回歸檢查涵蓋跨年度、不同球隊、搜尋、空結果與和局。')
picture('cross-year.png',6.1)
p('圖三　選取 2023 年與遊騎兵後，只統計一場比賽，不把部分資料當成完整系列賽。')
h('延伸方式與實作心得')
p('固定資料格式與共用頁面讓 AI 新增其他年度比賽時，只需加入資料與來源快照；分類自動產生，統計不依賴特定球隊。若增加新的數據欄位，仍需同步更新 AGENTS.md、驗證程式及畫面。README 已提供實際匯入命令與操作方式。')
p('目前未提供網頁新增表單、即時更新或帳號寫入。網站透過 GitHub Pages 發布，新增資料並提交 GitHub 後，會自動重新部署。課程平台繳交作業說明 PDF 及 AGENTS.md。')
doc.core_properties.title='棒球逐場賽事紀錄站 作業說明';doc.core_properties.author='Luproject-maker'
for node in list(doc._element.iter(qn('w:pBdr'))):node.getparent().remove(node)
for node in list(doc.styles.element.iter(qn('w:pBdr'))):node.getparent().remove(node)
path=OUT/'Homework9_作業說明.docx';doc.save(path);print(path)
