# 棒球逐場賽事紀錄站 開發規則

## 專案目的與讀者
建立繁體中文棒球逐場數據網站，支援不同年度、系列賽與球隊。目前收錄2023世界大賽第五場、2024世界大賽五場、2025世界大賽七場、2026世界大賽五場，共18場、四個年度；2023僅收錄一場。網頁沒有直接新增表單，維護者透過匯入命令或AI更新資料。本文件是後續AI新增、修正資料與頁面的共同規範。

## 技術與檔案結構
- 原生 HTML、CSS、JavaScript 與 JSON；不依賴前端框架、付費 API、資料庫或建置流程。
- index.html 是共用入口；使用 #game/比賽id、#stats、#about 切換頁面，重新整理與上一頁都應有效。
- assets/style.css 統一管理視覺，assets/app.js 管理載入、路由、搜尋、統計與安全呈現。
- assets/data.mjs 提供共用篩選及統計，供瀏覽器與 Node 回歸檢查使用，不得寫死特定球隊。
- assets/experience.js 與 experience.css 管理精選主視覺、SVG球場、互動得分走勢、中文時間軸、球員亮點及系列賽進度。SVG使用DOM建立，無外部圖片依賴。
- data/games.json 是前端唯一資料來源；sources/ 保存 MLB 官方原始 JSON 快照。
- scripts/import_mlb.py 匯入官方資料；scripts/validate.mjs 執行資料檢查；tests/ 保存擴充示範紀錄。
- scripts/import_world_series.py --years 2025 2026 可批次追加世界大賽；保存官方賽程，使用官方 seriesGameNumber，不自行依日期猜場次，只收錄已結束賽事。無已結束資料時不得編造或悄悄略過。
- docs/ 保存作業文件與驗證截圖，不放金鑰、登入資訊、個人敏感資料。
- 全部資源採相對路徑，必須相容 GitHub Pages 專案子目錄。

## 視覺與互動規範
- 球場記分板風格：深綠 #123c32、米白 #f6f3eb、金黃 #dfba69、深灰 #202b28。
- 用 CSS 變數管理顏色與間距；系統中文字型，內文 16px 以上，行高 1.6 以上。
- 桌面最大內容寬度 1200px；手機卡片改單欄，長表格只在容器內橫向捲動。
- 沿用共同頁首、頁尾、卡片、統計數字及表格，不為單場另建一套風格。
- 主選單、搜尋、篩選、卡片連結均能鍵盤操作，焦點可見；表格加 caption 與 th。
- 搜尋涵蓋球隊中英文縮寫、球場、日期、系列賽、年度與球員姓名。
- 年度、系列賽、球隊選項由資料自動產生；所有篩選與搜尋取交集，首頁與總覽共用目前條件。
- 勝敗以選取球隊為視角，未選球隊時停用勝敗篩選；卡片標示實際勝隊，和局獨立呈現。
- 無結果、未知路由、讀取失敗均須有可操作提示；清除條件重設全部篩選。

## 資料格式
games.json 最外層包含 title、scope、games。每場必填：
- id：唯一小寫英文、數字、連字號，如 ws-2024-g5；gamePk：MLB 官方唯一編號。
- season：官方賽季年度整數，不以匯入年份代替。
- seriesId：包含年度的系列賽唯一分類，如 mlb-2023-world-series。
- seriesName：顯示名稱，如 2023 世界大賽。同一 seriesId 的年度與名稱必須一致。
- number：系列賽場次；date：官方球場當地 YYYY-MM-DD，不擅自轉成台灣日期。
- 同一 seriesId 的 number 不可重複；只收錄第五場時仍必須標示第五場，不能重新編號。
- venue、status（Final）、source（官方 API URL）、sourcePage（官方賽事頁）、retrieved（擷取日）。
- teams.away 及 teams.home：code、name、runs、hits、errors、innings、batters、pitchers。
- innings：依局序得分；未進行的半局為 null，呈現 X，不能改成 0。
- batters：name、position、atBats、runs、hits、rbi、baseOnBalls、strikeOuts、homeRuns。
- pitchers：name、inningsPitched、hits、runs、earnedRuns、baseOnBalls、strikeOuts、numberOfPitches。
- inningsPitched 保持棒球記法字串，例如 5.2 表示 5 局 2 出局，不能當 5.2 十進位局。
- scoring：官方得分事件，含 inning、half、description、awayScore、homeScore。
- 每項 scoring 另含官方 eventType、batter 與 rbi；中文時間軸只依這些欄位、相鄰比分差與半局產生，英文原文必須可展開核對。未知事件種類使用中性描述，不能猜測球路、守備細節或球員心情。
- summary：只依核對資料產生的繁體中文摘要；reflection：個人心得，未提供為 null。

## 資料可信度
- 優先使用 MLB 官方 Stats API 及官方賽事頁，保留來源快照；不得憑空填入真實比賽數字。
- 未提供數據使用 null，畫面顯示「—」；零分、未出賽與缺資料不可混淆。
- 不把示意資料混入正式統計，不編造觀賽心得、資料來源或完成驗證的紀錄。
- 得分事件保留官方英文原文並標示；中文重點不是逐字翻譯，使用官方事件種類及打點，並以相鄰比分差計算得分。不得把得分數與打者打點混淆，失誤可能造成兩者不同。
- 每隊逐局得分加總等於總得分；非負整數欄位不得為負值；球員安打不得大於打數。
- 不收錄尚未結束的比賽；延長局與主隊最後半局未打必須正確顯示。
- 彙總只涵蓋已收錄場次，勝率分母為該隊實際收錄出賽場數。
- 統計只計算目前所有篩選的交集；各隊場數分開計算，不能把總資料筆數當成每隊場數。
- 單場標題讀取 seriesName，繼續閱讀只列同一 seriesId；圖表以主客隊呈現，不寫死對戰球隊。

## 精選與視覺呈現規則
- 首頁精選排序依再見得分100分、再見滿貫另加100分、超過9局每局10分，再以日期較新者優先；只稱「本站精選」，不得冒稱官方推薦。
- 再見得分須為最後得分事件、9局後的下半局、主隊從未領先變為領先，且事件後比分等於終場。滿貫須官方 home_run、4打點且比分增加4分。
- 逐局折線圖從賽前0分累加每局得分；null半局不可畫成已進行，讀值需標示未攻擊。圖表為得分走勢，不能宣稱勝率預測。
- 局數滑桿必須能用鍵盤操作，更新可讀比分；SVG有替代文字，逐局記分板仍提供完整資料。
- 球員亮點按兩隊打者最高打點、最多全壘打、投手最高三振計算；所有並列者都列出。零紀錄顯示無此項紀錄，不選出假冠軍，不稱官方MVP。
- 系列賽進度只根據目前篩選後的已收錄場次產生勝場與G場次入口；部分收錄不得宣稱系列賽冠軍或完整戰績。
- 球隊識別色只輔助辨識，必須同時顯示縮寫或隊名；不使用未授權商標或球員照片。動態效果遵守 prefers-reduced-motion。

## 新增比賽流程
1. 先閱讀本文件、README 與現有資料；確認官方年度、系列賽、場次，不必為新增其他年度改寫頁面。
2. 取得官方 gamePk，保存 sources/<gamePk>.json，依既有欄位轉換。
3. 執行 python scripts/import_mlb.py --game-pk 編號 --season 年度 --series-id 分類id --series-name 名稱 --number 場次。命令只追加新比賽；重複 gamePk 或系列賽場次必須拒絕，不能覆蓋舊資料。
4. 無需手寫卡片或統計；共用 renderer 應自動產生列表、內頁及統計。
5. 執行 node scripts/validate.mjs、node tests/archive.test.mjs 及 node tests/experience.test.mjs，再用 HTTP 預覽驗證新分類、精選、圖表、時間軸、內頁與總覽。列表按日期由新到舊排序。
6. 在 tests/extension-log.md 記錄真實的前後場次、統計變化、修改檔案與檢查結果。
7. 新增年度時執行 node tests/seasons.test.mjs，核對官方賽程ID、場次、比分及每年度統計；舊年度回歸斷言必須限定其年度，不把舊資料總數當成全站不變規則。

## 修改頁面流程
改動前確認相關路由及共用樣式。只調整需求範圍，不引入不必要套件。所有 JSON 文字用 textContent 或安全的 DOM 節點呈現，不以未轉義 innerHTML 插入；外部連結限制 https，另開分頁需 noopener。

## 完成標準
- 全部資料的年度、系列賽、逐局總分與球員資料檢查通過；原始來源可追溯。
- 首頁、全部賽事頁、總覽、說明頁與找不到頁面正常。
- 年度、系列賽、球隊、搜尋、勝敗交集、清除條件與上一頁正常；非道奇比賽不會造成錯誤。
- 375px 與桌面寬度可閱讀，頁面無水平溢出；表格可獨立捲動。
- 使用 HTTP 預覽；Console 無非預期錯誤；GitHub Pages 上相對路徑正常。
- 如未完成任何檢查或發布，明確記錄限制，不宣稱已完成。
