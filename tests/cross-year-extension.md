# 跨年度新增比賽實作

2026-11-15 修訂。原版限定道奇與洋基，加入其他隊伍會使查找 LAD 的統計失敗。本次將資料結構改為 season、seriesId、seriesName，統計改為依比賽實際出賽球隊計算，年度與球隊分類由資料產生。

## 實際新增
完成共用程式修改與資料遷移後，執行：

```text
python scripts/import_mlb.py --game-pk 748534 --season 2023 --series-id mlb-2023-world-series --series-name "2023 世界大賽" --number 5
```

官方快照保存 sources/748534.json，追加 mlb-748534，原有五場保留。新增後共六場、兩個年度、兩個系列賽、四支球隊。新比賽為遊騎兵 5:0 響尾蛇。官方來源：https://statsapi.mlb.com/api/v1.1/game/748534/feed/live 。

## 驗證結果
- node scripts/validate.mjs：六場資料通過 1,248 項檢查。
- node tests/archive.test.mjs：跨年度、非原有球隊、篩選交集、分母、空結果及和局檢查通過。
- 再次以相同 gamePk 執行命令：拒絕重複匯入，前後 SHA-256 一致，games.json 未改變。
- 2024 分類：五場，道奇得分25、洋基得分24，原有統計不變。
- 2023 分類加遊騎兵勝場：只有一場，該隊1勝0敗、得分5；導覽至總覽後保留條件。
- 2023 年加道奇：空結果，不顯示其他年度的資料。
- 清除條件：恢復六場；總得分54；四隊出賽場數為5、5、1、1，沒有誤用六場當每隊分母。
- 新年度單場標題為2023世界大賽，第五場投打數據正常，沒有串入2024的繼續閱讀連結。
- Chrome 實際 CSS viewport 375px，首頁與單場內容寬356px，頁面未水平溢出。
- 跨年度功能於本機驗證，並依使用者後續要求更新 GitHub；部署驗證結果見 docs/publication.json。
