# 市場數據整合系統

這個項目旨在自動化從多個市場Excel文件提取財務交易詳情、處理這些數據，然後系統性地更新指定的Google表格文檔。

## 描述

市場數據整合系統設計用於處理存儲在指定目錄中的`.xls`和`.xlsx`文件中的財務數據。它能夠提取特定的交易細節，處理這些數據，並以結構化的方式更新Google表格文檔，使數據易於訪問和管理。

## 開始使用

### 先決條件

你需要安裝的軟件：

- Python 3.x
- Pandas
- Pygsheets
- Glob

使用pip安裝必要的Python庫：

```bash
pip install pandas pygsheets glob2