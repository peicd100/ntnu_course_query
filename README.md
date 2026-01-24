# 師大課程查詢系統

## 1. 專案概述

本專案為桌面版「課程查詢與排課系統」，以 PySide6（Qt）打造 GUI，從課程 Excel（.xls/.xlsx）載入資料後，提供查詢篩選、我的最愛、課表檢視、歷史紀錄與最佳選課（不衝突組合搜尋）等功能。所有輸入／輸出／使用者狀態檔皆預設存放於 `user_data/`。

## 2. 重要變數

1. ENV_NAME：`ntnu_course_query`（Conda 環境名稱；同時作為 GitHub repository 命名依據）
2. workspace root(EXE_NAME)：`師大課程查詢系統`（專案根目錄資料夾名稱 basename；亦作為 .exe 命名依據）

## 3. workspace root(EXE_NAME) 定義

* workspace root(EXE_NAME) 指「專案根目錄資料夾名稱（basename）」，本專案為：`師大課程查詢系統`。
* 文件敘述層面使用「workspace root(EXE_NAME)」此名詞。
* 程式碼／命令列／工具參數需要使用該值時，必須直接使用其實際值 `師大課程查詢系統`（不得以佔位符呈現）。

## 4. 檔案與資料夾結構

以下為最小必要集合（實際打包後可能額外出現 `dist/`、`build/`）：

```
師大課程查詢系統/
├─ README.md
├─ app_main.py
├─ app_constants.py
├─ app_excel.py
├─ app_mainwindow.py
├─ app_timetable_logic.py
├─ app_user_data.py
├─ app_utils.py
├─ app_widgets.py
├─ app_workers.py
├─ user_data/
│  ├─ course_inputs/
│  │  └─ （課程 Excel：*.xls / *.xlsx）
│  └─ user_schedules/
│     └─ <username>/
│        ├─ history/
│        │  └─ <YYYYMMDD_HHMMSS>.xlsx
│        └─ best_schedule/
│           ├─ 學分_<學分>，優先度和_<數值>.xlsx
│           └─ best_schedule_cache.json
├─ dist/
└─ build/
```

## 5. Python 檔名規則

* 主入口檔：`app_main.py`
* 模組檔：`app_*.py`
* `app_main.py` 與所有 `app_*.py` 必須位於同一層（workspace root(EXE_NAME) 根目錄）。

## 6. user_data/ 規範

* `user_data/` 為所有輸入／輸出／設定的預設根目錄。
* `user_data/` 的位置規則：

  * 開發期（直接執行 `python app_main.py`）：位於 workspace root(EXE_NAME)/user_data/
  * 打包後（執行 .exe）：位於 .exe 同層資料夾的 user_data/
* `user_data/course_inputs/`

  * 用途：存放課程 Excel（`*.xls` / `*.xlsx`）。
  * 啟動時會自動嘗試載入此資料夾內第一個可用檔案（會略過 `~$` 暫存檔）。
  * 亦可由選單「檔案 → 開啟課程 Excel…」手動選取，程式會複製檔案到此資料夾以便下次自動載入。
* `user_data/user_schedules/<username>/`

  * `history/`：每次登入會建立一個時間戳記檔（`YYYYMMDD_HHMMSS.xlsx`）保存「我的最愛／課表／鎖定／加入順序」。
  * `best_schedule/`：最佳選課輸出（最多 5 組）與快取檔 `best_schedule_cache.json`。

## 7. Conda 環境（ENV_NAME）與安裝規範

先取得專案並進入 workspace root(EXE_NAME)（兩行命令需置於同一個文字框內）：

```
git clone https://github.com/peicd100/ntnu_course_query.git 師大課程查詢系統
cd 師大課程查詢系統
```

A. 推薦方案（conda 優先）

```
conda create -n ntnu_course_query python=3.10 -y
call conda.bat activate ntnu_course_query
conda install -c conda-forge pyside6 numpy pandas openpyxl xlrd pyinstaller -y
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; import app_main; print('OK')"
```

B. 備援方案（conda + pip；pip 必須附原因）

* 原因：若 conda 解算器在 Qt/PySide6 依賴上出現衝突，改用 pip 安裝 PySide6 通常較容易成功。

```
conda create -n ntnu_course_query python=3.10 -y
call conda.bat activate ntnu_course_query
conda install -c conda-forge numpy pandas openpyxl xlrd pyinstaller -y
python -m pip install PySide6
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; import app_main; print('OK')"
```

C. 最後手段（pip only）

```
conda create -n ntnu_course_query python=3.10 -y
call conda.bat activate ntnu_course_query
python -m pip install PySide6 numpy pandas openpyxl xlrd pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; import app_main; print('OK')"
```

建議優先使用 A 方案（conda-forge）以提高 Windows 上的相依套件一致性與安裝成功率；若遇到 Qt/solver 相依衝突，再改用 B 方案。

## 8. 測試方式（只測 python app_main.py；兩時點）

1. 安裝完成後測試（乾淨環境）

```
python app_main.py
```

（可選）快速煙霧測試（程式會自動開啟後短暫時間關閉）：

```
python app_main.py --smoke-test
```

2. 修改／更新後回歸測試（再次執行同一入口）

```
python app_main.py
```

驗收標準：程式可正常啟動並顯示主視窗，且未出現未處理例外導致的錯誤視窗。

## 9. 打包成 .exe（必填；提供可複製指令；不測試 .exe）

前置：已在 `ntnu_course_query` 環境安裝 `pyinstaller`。

建議使用 `--onedir`（較容易處理 Qt 依賴）：

```
pyinstaller --noconsole --onedir --name "師大課程查詢系統" app_main.py -y
```

輸出位置（預設）：

* `dist/師大課程查詢系統/師大課程查詢系統.exe`

注意：本專案不測試 .exe；僅要求第 (8) 節兩時點測試可通過。

## 10. 使用者要求（必填；長期約束；需持續維護）

* 文件與說明以繁體中文為主（程式碼／命令列／檔名／路徑依實務需要維持英文/原樣）。
* 所有輸入／輸出／設定預設放在 `user_data/`；若未來需要改為可選擇輸出路徑，需新增設定並集中由 `app_constants.user_data_root_path()` 控制。
* GitHub 操作指令需以第 (11) 節內容為準（凍結區塊）。

## 11. GitHub操作指令

# 初始化

```
(
echo.
echo # ignore build outputs
echo dist/
echo build/
)>> .gitignore
git init
git branch -M main
git remote add origin https://github.com/peicd100/ntnu_course_query.git
git add .
git commit -m "PEICD100"
git push -u origin main
```

# 例行上傳

```
git add .
git commit -m "PEICD100"
git push -u origin main
```

# 還原成Git Hub最新資料

```
git rebase --abort || echo "No rebase in progress" && git fetch origin && git switch main && git reset --hard origin/main && git clean -fd && git status
```

# 查看儲存庫

```
git remote -v
```
