# 棒球賽事 Wiki

生成式 AI Homework 9：透過 AGENTS.md 建立可重複擴充的棒球賽事數據網站。

## 專案與公開網址
- Repository：https://github.com/Luproject-maker/baseball-game-wiki
- 預定 GitHub Pages：https://luproject-maker.github.io/baseball-game-wiki/
- 發布是否成功請以 docs/publication.json 及實際連線結果為準，不將預定網址視為已發布。

## 功能
2024 世界大賽五場真實資料，逐局比分、完整出賽打者與投手數據、官方得分事件、球隊球員搜尋、道奇勝敗篩選、累計數據與逐場得分圖。日期採球場當地官方日期。

## 本機使用
在專案根目錄執行 `python -m http.server 8766`，開啟 http://localhost:8766 。不能直接雙擊 HTML，因為瀏覽器會限制 file:// 讀取 JSON。

## 結構
`index.html` 為入口，`assets/` 為共用樣式及程式，`data/games.json` 是呈現資料，`sources/` 是官方快照，`scripts/` 為匯入與檢查工具，`tests/` 是擴充與驗證紀錄，`docs/` 為說明及截圖。

## 新增或修正內容
先讀 AGENTS.md。依其欄位規格新增資料，保留原始官方來源，不需修改 HTML 卡片或統計程式。`node scripts/validate.mjs` 執行資料檢查。`python scripts/import_mlb.py` 可由本機來源快照重建資料；缺少快照時才下載官方資料。

AI 指令範例：「請閱讀 AGENTS.md，依 sources/775296.json 新增 ws-2024-g5，驗證資料後檢查新增卡片與累計統計，記錄真實的修改結果。」

## GitHub Pages 發布
將專案內容上傳至公開 Repository，Settings → Pages → Deploy from a branch → main / (root) → Save。根目錄 .nojekyll 避免不必要的 Jekyll 處理。資料與資源皆使用相對路徑，hash 路由可直接分享單場頁。

## 資料來源與限制
MLB Stats API：https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live 。每場保存 gamePk、官方連結及擷取日期，原始快照供核對。官方英文事件原文保留；中文摘要僅整理數據，不編造現場觀察。統計只代表本站五場，不是全年數據。無自動即時更新、無帳號及雲端寫入功能。本站非 MLB 官方網站，教育用途，未使用球隊商標或球員照片。
