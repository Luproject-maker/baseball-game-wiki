# AI 依規則擴充實作紀錄

本文件保留原版四場到五場的歷史測試結果；新版跨年度追加至六場的實作與最新檢查數量，請見 cross-year-extension.md。before-g5.json 與 added-g5.json 已補入新版分類欄位，重新檢查的項目數會與原始紀錄不同。

日期：2026-11-15。此紀錄是本次實際執行的重現測試，非虛構第二次對話。

## 操作任務
閱讀 AGENTS.md，將只含前四場的資料集，依官方 sources/775296.json 加入第五場 ws-2024-g5；沿用 renderer，自動更新卡片、內頁與統計。

## 前置基準
tests/before-g5.json 保存四場資料；實際複製到 data/games.json，再重新載入 HTTP 首頁確認。檢查通過 803 項，頁面顯示 4 場、道奇 3 勝 1 敗、兩隊總得分各 18。docs/screenshots/before-g5.png 為實際瀏覽器截圖。

## 擴充動作
依既有 scripts/import_mlb.py 讀取已保存的官方快照並重建五場資料。tests/added-g5.json 保存新增資料物件。未修改 index.html、assets/app.js 或 assets/style.css。

## 擴充後結果
node scripts/validate.mjs 通過 995 項。道奇 4 勝 1 敗、總得分 25、安打 33、失誤 2；洋基 1 勝 4 敗、總得分 24、安打 36、失誤 5。第五場是道奇 7 比 6 洋基，官方 gamePk 775296。首頁、單場及統計由同一套 renderer 讀取新增資料。

## 規則作用
唯一 id 避免重複場次；固定 JSON 欄位使頁面不用重做；逐局加總和來源比對防止比分錯誤；共用 CSS 保持視覺一致。未來擴充其他系列賽時，需同步更新 scope、首頁介紹與勝敗視角，不應直接沿用世界大賽限定文案。
