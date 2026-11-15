# 棒球逐場賽事紀錄站

生成式 AI Homework 9：使用 AGENTS.md 定義可持續新增比賽的資料與開發規則。

## 網址與版本
- Repository：https://github.com/Luproject-maker/baseball-game-wiki
- 網站：https://luproject-maker.github.io/baseball-game-wiki/
- 跨年度修訂版包含六場官方賽事，透過 GitHub Pages 部署。部署驗證紀錄見 docs/publication.json；課程平台作業由使用者自行提交。

## 功能與範圍
支援不同年度、系列賽、球隊的逐場紀錄。初始資料是 2024 世界大賽五場，以及 2023 世界大賽第五場，共六場官方比賽。2023 系列賽僅收錄一場，不代表完整系列賽。

首頁與數據總覽共用年度、系列賽、球隊、勝敗、搜尋條件，全部條件取交集。勝敗以選取球隊為視角，未選球隊時停用。各球隊統計以自己的實際出賽場數計算。單場頁保留逐局比分、打者與投手成績、官方得分事件與來源。

## 比賽閱讀體驗
首頁提供依再見得分、滿貫及延長局排序的本站精選，搭配原生SVG球場與記分板，並用系列賽進度列串起已收錄場次。球隊色彩與縮寫輔助辨識，動畫遵守減少動態效果偏好。

單場頁提供可鍵盤操作的局數滑桿、逐局累計得分折線圖、中文關鍵時刻與可展開的官方英文原文。球員亮點以兩隊最高打點、全壘打與投手三振計算，並列者全部顯示，非官方MVP。得分走勢不是勝率預測；中文時間軸是依官方事件種類與數據的重點整理，不是逐字翻譯。

## 本機使用
專案根目錄執行 `python -m http.server 8766`，開啟 http://localhost:8766 。不要直接用 file:// 開啟 HTML。

## 新增比賽
網站是靜態資料站，沒有直接新增或雲端儲存表單。維護者可執行匯入命令，或請 AI 讀取 AGENTS.md 協助整理。

以未收錄的官方 gamePk 替換下列「官方編號」，並填入正確年度、分類、名稱與場次：

```text
python scripts/import_mlb.py --game-pk 官方編號 --season 2025 --series-id mlb-2025-world-series --series-name "2025 世界大賽" --number 1
node scripts/validate.mjs
node tests/archive.test.mjs
node tests/experience.test.mjs
```

命令保存 sources/<gamePk>.json，核對官方年度與結束狀態，再追加 games.json。重複編號、同系列賽重複場次、名稱衝突會被拒絕。不帶參數只補入缺少的 2024 世界大賽五場，保留其他年度的既有資料。分類選項由資料自動產生，不用修改 HTML 或 app.js。完成後提交資料及快照，更新 GitHub 即可。

AI 指令範例：「請閱讀 AGENTS.md，依官方 gamePk 新增一場 2025 世界大賽資料。確認 season、seriesId、seriesName 與 number，不覆蓋已有比賽。執行檢查，確認新分類自動出現且統計只涵蓋目前篩選範圍。」

## 結構與檢查
index.html 為入口，assets/app.js 呈現畫面，assets/data.mjs 提供篩選及統計，assets/style.css 管理樣式；data/games.json 是前端唯一資料來源，sources 保存官方快照，scripts 提供匯入與驗證，tests 保存回歸檢查與擴充紀錄，docs 保存文件與截圖。

`node scripts/validate.mjs` 比對全部官方快照；`node tests/archive.test.mjs` 驗證跨年度、不同球隊、篩選交集、正確分母、空結果及和局。虛構測試場次只在記憶體使用，不加入正式資料。

## 發布與限制
GitHub Pages 維持 main / (root)，檔案使用相對路徑及 hash 路由。上傳完整解壓後的資料夾結構，不能只上傳 ZIP 或把資料夾攤平。

來源為 MLB Stats API，每場保留官方連結與擷取日，日期採球場當地日期。官方得分事件保留英文，摘要只整理數據，不編造觀賽心得。本站非 MLB 官方網站，不提供即時比分或帳號寫入，未使用球隊商標及球員照片。
