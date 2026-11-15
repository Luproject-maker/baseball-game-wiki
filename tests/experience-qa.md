# 六項閱讀體驗改版驗證

2026-11-15。本次沿用六場官方資料，新增主視覺與閱讀互動，沒有加入虛構正式賽事。

- 精選依再見得分、再見滿貫與延長局排序，選出2024世界大賽第一場；主視覺顯示該場3:6與10局，連結可開啟對應單場。
- 互動走勢圖逐局累加，鍵盤Home顯示賽前0:0，End顯示第10局3:6；曲線與記分板一致。
- 球員亮點顯示Freddie Freeman 4打點；Stanton與Freeman各1支全壘打並列；Jack Flaherty 6次三振。畫面標示非官方MVP。
- 中文事件保留官方eventType、batter、rbi來源，區分本次得分與打點，英文原文可展開。第一場最後事件正確標示再見得分及滿貫。
- 系列賽進度依目前篩選產生。選2023後僅顯示G5及1場收錄，不宣稱完整戰績。
- Chrome實際375px viewport，首頁與單場scrollWidth為356px。圖表容器286px、內容600px，在容器內捲動，頁面無橫向溢出。
- Console捕捉error日誌為空。球隊顏色搭配文字縮寫，圖表具替代文字及完整記分板，CSS有prefers-reduced-motion設定。
- node scripts/validate.mjs通過1,434項官方資料比對；node tests/archive.test.mjs及node tests/experience.test.mjs均通過。
- 截圖home-v3、game-v3、chart-v3、timeline-v3、series-v3保存於docs/screenshots；舊版截圖保留歷史紀錄。
