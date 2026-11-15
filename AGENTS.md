# 棒球賽事 Wiki 開發規則

## 專案目的與讀者
建立繁體中文棒球逐場數據網站，讓一般球迷查詢比分、逐局得分、球員投打數據及得分事件。初版範圍是 2024 MLB 世界大賽五場，不代表全年賽季。本文件是後續 AI 新增、修正資料與頁面的共同規範。

## 技術與檔案結構
- 原生 HTML、CSS、JavaScript 與 JSON；不依賴前端框架、付費 API、資料庫或建置流程。
- index.html 是共用入口；使用 #game/比賽id、#stats、#about 切換頁面，重新整理與上一頁都應有效。
- assets/style.css 統一管理視覺，assets/app.js 管理載入、路由、搜尋、統計與安全呈現。
- data/games.json 是前端唯一資料來源；sources/ 保存 MLB 官方原始 JSON 快照。
- scripts/import_mlb.py 匯入官方資料；scripts/validate.mjs 執行資料檢查；tests/ 保存擴充示範紀錄。
- docs/ 保存作業文件與驗證截圖，不放金鑰、登入資訊、個人敏感資料。
- 全部資源採相對路徑，必須相容 GitHub Pages 專案子目錄。

## 視覺與互動規範
- 球場記分板風格：深綠 #123c32、米白 #f6f3eb、金黃 #dfba69、深灰 #202b28。
- 用 CSS 變數管理顏色與間距；系統中文字型，內文 16px 以上，行高 1.6 以上。
- 桌面最大內容寬度 1200px；手機卡片改單欄，長表格只在容器內橫向捲動。
- 沿用共同頁首、頁尾、卡片、統計數字及表格，不為單場另建一套風格。
- 主選單、搜尋、篩選、卡片連結均能鍵盤操作，焦點可見；表格加 caption 與 th。
- 搜尋涵蓋球隊中英文縮寫、球場、日期與球員姓名；勝敗一律以道奇視角標示。
- 搜尋與勝敗篩選同時作用，無結果、未知路由、讀取失敗均須有可操作提示。

## 資料格式
games.json 最外層包含 title、scope、games。每場必填：
- id：唯一小寫英文、數字、連字號，如 ws-2024-g5；gamePk：MLB 官方唯一編號。
- number：系列賽場次；date：官方球場當地 YYYY-MM-DD，不擅自轉成台灣日期。
- venue、status（Final）、source（官方 API URL）、sourcePage（官方賽事頁）、retrieved（擷取日）。
- teams.away 及 teams.home：code、name、runs、hits、errors、innings、batters、pitchers。
- innings：依局序得分；未進行的半局為 null，呈現 X，不能改成 0。
- batters：name、position、atBats、runs、hits、rbi、baseOnBalls、strikeOuts、homeRuns。
- pitchers：name、inningsPitched、hits、runs、earnedRuns、baseOnBalls、strikeOuts、numberOfPitches。
- inningsPitched 保持棒球記法字串，例如 5.2 表示 5 局 2 出局，不能當 5.2 十進位局。
- scoring：官方得分事件，含 inning、half、description、awayScore、homeScore。
- summary：只依核對資料產生的繁體中文摘要；reflection：個人心得，未提供為 null。

## 資料可信度
- 優先使用 MLB 官方 Stats API 及官方賽事頁，保留來源快照；不得憑空填入真實比賽數字。
- 未提供數據使用 null，畫面顯示「—」；零分、未出賽與缺資料不可混淆。
- 不把示意資料混入正式統計，不編造觀賽心得、資料來源或完成驗證的紀錄。
- 得分事件保留官方英文原文並標示；摘要不從總比分推測全壘打、逆轉或球員表現。
- 每隊逐局得分加總等於總得分；非負整數欄位不得為負值；球員安打不得大於打數。
- 不收錄尚未結束的比賽；延長局與主隊最後半局未打必須正確顯示。
- 彙總只涵蓋已收錄場次，勝率分母為該隊實際收錄出賽場數。

## 新增比賽流程
1. 先閱讀本文件、README 與現有資料；確認新賽事屬於宣告範圍，範圍變動要同步更新文案。
2. 取得官方 gamePk，保存 sources/<gamePk>.json，依既有欄位轉換。
3. 檢查 id 與 gamePk 均無重複；新增到 games，依 number 排序，不覆蓋舊資料。
4. 無需手寫卡片或統計；共用 renderer 應自動產生列表、內頁及統計。
5. 執行 node scripts/validate.mjs，再用本機 HTTP 伺服器驗證新連結、搜尋及總覽。
6. 在 tests/extension-log.md 記錄真實的前後場次、統計變化、修改檔案與檢查結果。

## 修改頁面流程
改動前確認相關路由及共用樣式。只調整需求範圍，不引入不必要套件。所有 JSON 文字用 textContent 或安全的 DOM 節點呈現，不以未轉義 innerHTML 插入；外部連結限制 https，另開分頁需 noopener。

## 完成標準
- 資料檢查通過，五場逐局總分與球員資料合理；原始來源可追溯。
- 首頁、全部賽事頁、總覽、說明頁與找不到頁面正常。
- 搜尋、勝敗篩選、清除條件、瀏覽器上一頁正常。
- 375px 與桌面寬度可閱讀，頁面無水平溢出；表格可獨立捲動。
- 使用 HTTP 預覽；Console 無非預期錯誤；GitHub Pages 上相對路徑正常。
- 如未完成任何檢查或發布，明確記錄限制，不宣稱已完成。
