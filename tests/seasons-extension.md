# 2025 與 2026 世界大賽追加紀錄

2026-11-15，依MLB官方賽程API確認後，執行 python scripts/import_world_series.py --years 2025 2026。

新增2025世界大賽7場（道奇對藍鳥）及2026世界大賽5場（釀酒人對光芒），均為Final。保留原有6場，共18場、2023至2026四個年度、四個世界大賽分類、七隊。新球隊有繁體中文名稱與識別色。

官方賽程快照：sources/schedule-2025-world-series.json與schedule-2026-world-series.json。全部新比賽保留完整live/feed官方快照，場次使用seriesGameNumber，不自行用日期重新編號。

node scripts/validate.mjs通過4,556項資料檢查。archive、experience、seasons三組回歸檢查通過。2025第三場18局的比分走勢、2025及2026分類的出賽場數與勝場均正確。兩年度總得分分別60與37，全站總得分151。2023仍只有第五場，不宣稱完整系列賽。
