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
p('本專案將棒球逐場比賽資料整理成可搜尋、可閱讀與持續擴充的網站。收錄2024世界大賽5場、2025世界大賽7場、2026世界大賽5場，以及2023世界大賽第五場，共18場、四個年度、七隊。提供逐局比分、球員投打數據及目前範圍的統計。2023僅收錄一場，不代表完整系列賽。')
p('本次作業的核心是先建立 AGENTS.md，明確定義資料與開發方式，再讓 AI 依規則完成網站。後續只要加入符合格式的賽事資料，共用程式就能產生新卡片、單場頁及統計，不必重做整個網站。')
h('專案與網站連結')
hyperlink('GitHub Repository  https://github.com/Luproject-maker/baseball-game-wiki','https://github.com/Luproject-maker/baseball-game-wiki')
hyperlink('公開網站  https://luproject-maker.github.io/baseball-game-wiki/','https://luproject-maker.github.io/baseball-game-wiki/')
hyperlink('開發規則  AGENTS.md','https://github.com/Luproject-maker/baseball-game-wiki/blob/main/AGENTS.md')
picture('home-v3.png')
p('圖一　精選賽事搭配原生 SVG 球場與記分板，提供比賽故事入口及年度、系列賽、球隊分類。')

doc.add_page_break();h('網站功能與資料來源')
table(['頁面','主要內容'],[['賽事紀錄','精選故事、球場主視覺、系列賽進度、年度及球隊篩選。'],['單場數據','球員亮點、互動得分走勢、中文關鍵時刻及完整投打表格。'],['數據總覽','依目前篩選範圍計算各隊出賽場數、勝敗與得分資料。'],['關於本站','說明資料來源、數據記法、精選依據與新增比賽方式。']])
p('資料來自 MLB 官方 Stats API，擷取日期為 2026 年 11 月 15 日。每場保留 gamePk、官方賽事頁、API 連結與 sources 原始 JSON 快照，供重現及核對。網頁日期採球場當地官方日期，不混用台灣跨日日期。')
hyperlink('來源範例  2026 世界大賽第五場官方 API','https://statsapi.mlb.com/api/v1.1/game/849799/feed/live')
table(['年度','收錄場次','對戰球隊','資料範圍'],[['2023','1場','遊騎兵／響尾蛇','僅第五場'],['2024','5場','道奇／洋基','全部已完成場次'],['2025','7場','道奇／藍鳥','全部已完成場次'],['2026','5場','釀酒人／光芒','全部已完成場次']])
picture('game-v3.png',6.1)
p('圖二　單場頁從球員亮點切入，依本場數據呈現打點、全壘打與三振焦點；並列最高者同時顯示。')

doc.add_page_break();h('AGENTS.md 如何規範 AI')
p('AGENTS.md 放在專案根目錄，讓 AI 開始工作時先理解專案目的、內容界線與完成標準。規則採用具體欄位與操作流程，避免只要求「美觀」或「正確」而缺少可執行的方法。')
table(['規則面向','具體要求'],[['專案與結構','原生 HTML、CSS、JavaScript、JSON；data.mjs 共用篩選、統計與閱讀邏輯。'],['視覺一致性','深綠、米白與金黃配色；SVG球場與球隊色輔助辨識，動畫可減少。'],['內容與分類','固定 season、seriesId、seriesName；id、gamePk 及系列賽場次不可重複。'],['數據可信度','中文事件依官方種類、比分差與打點產生，可展開核對英文；不得混淆得分與打點。'],['精選與亮點','精選標示本站依據；並列最高球員全列出；不冒稱官方MVP。'],['統計與驗證','每隊分別計算場數；圖表從零累加；部分系列賽不當成完整戰績。']])
h('檔案如何分工')
p('index.html 是入口；app.js 呈現頁面；data.mjs 提供可測試的篩選與計算；experience.js 與 experience.css 管理精選、SVG圖表及時間軸；games.json 保存資料；sources 保存官方來源；scripts 與 tests 提供匯入及驗證。')
h('AI 協作與 LLM Wiki 的對應')
p('課堂的 LLM Wiki 與個人化 Wikipedia 提供了整理和累積知識的方向。本專案採用相同的資料整理思路，將「官方原始紀錄 → 固定格式資料 → 可瀏覽網頁」串接起來。網站沒有額外宣稱具備聊天機器人或即時檢索功能；AI 的角色是依開發規則整理資料與維護程式。')
h('未來新增內容的指令範例')
p('「請先閱讀 AGENTS.md，依官方 gamePk 新增一場其他年度的比賽，填妥 season、seriesId、seriesName 及 number，不覆蓋舊資料。確認新分類自動出現，篩選與統計正常，並記錄檢查結果。」')

doc.add_page_break();h('擴充示範與驗證結果')
p('原先已完成四場到五場、再追加2023年比賽的示範。本次透過 import_world_series.py --years 2025 2026 批次加入12場，沿用共用頁面、圖表及中文事件。官方賽程與完整比賽快照均保存在 sources，新增過程見 tests/seasons-extension.md。')
table(['項目','擴充前','目前版本'],[['收錄場次','6場','18場'],['年度與分類','2023、2024','2023至2026，共4個年度'],['新增世界大賽','未收錄','2025七場、2026五場'],['球隊數量','4隊','7隊'],['資料檢查','1,434項通過','4,556項通過，含官方事件比對'],['新增流程','單場命令追加','按官方賽程與場次批次追加']])
p('瀏覽器確認2025分類有7場、2026有5場，各年度統計不混入其他年度。2025第三場18局滑桿可顯示終場藍鳥5比6道奇。三組回歸檢查涵蓋分類、搜尋、和局、球員亮點與官方賽程ID、場次及比分。')
picture('seasons-v4.png',6.1)
p('圖三　選取2026年後，只計算該年已收錄的五場，釀酒人4勝、光芒1勝，未混入其他年度。')
h('延伸方式與實作心得')
p('固定資料格式與共用頁面讓 AI 新增其他年度比賽時，只需加入資料與來源快照；分類自動產生，統計不依賴特定球隊。若增加新的數據欄位，仍需同步更新 AGENTS.md、驗證程式及畫面。README 已提供實際匯入命令與操作方式。')
p('目前未提供網頁新增表單、即時更新或帳號寫入。網站透過 GitHub Pages 發布，新增資料並提交 GitHub 後，會自動重新部署。課程平台繳交作業說明 PDF 及 AGENTS.md。')

h('六項閱讀體驗設計');doc.paragraphs[-1].paragraph_format.page_break_before=True
p('網站從資料查詢延伸到比賽回顧。以下功能皆沿用同一份官方資料，新增賽事時可自動產生，不需為每場比賽另外製作圖表或卡片。')
table(['設計','呈現與規則'],[['精選賽事','依再見得分、再見滿貫與延長局排序，提供明確的比賽故事入口。'],['得分走勢','逐局累加比分，滑桿可用鍵盤選擇局數；未進行半局另行標示。'],['中文時間軸','以官方事件種類、打者、打點及比分差整理，原文可展開核對。'],['球員亮點','兩隊單場最高打點、全壘打及投手三振，並列全列出，非官方評選。'],['棒球視覺','SVG球場、記分板數字、球隊識別色與輕微動畫，支援減少動態效果。'],['系列賽進度','串連已收錄的G場次、勝隊與比分，清楚標示目前篩選範圍。']])
picture('chart-v3.png',6.1)
p('圖四　互動逐局得分走勢與記分板相互對照，可讀取賽前到終場比分；圖表不代表勝率預測。')
p('閱讀體驗回歸檢查涵蓋再見滿貫、中文事件、逐局總分、並列球員、部分系列賽與未進行半局。手機版圖表在容器內捲動，頁面保持單欄閱讀。')
doc.core_properties.title='棒球逐場賽事紀錄站 作業說明';doc.core_properties.author='Luproject-maker'
for node in list(doc._element.iter(qn('w:pBdr'))):node.getparent().remove(node)
for node in list(doc.styles.element.iter(qn('w:pBdr'))):node.getparent().remove(node)
path=OUT/'Homework9_作業說明.docx';doc.save(path);print(path)
