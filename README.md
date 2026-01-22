# 師大課程查詢系統

## (1) 專案概述

「師大課程查詢系統（桌面版）」是一個以 PySide6 開發的桌面 GUI 工具，主要用途如下：

* 載入課程 Excel（.xls / .xlsx），自動挑選包含必要欄位的工作表並建立索引。
* 提供課程條件篩選與快速查詢（系所、課名、教師、學分、是否額滿、是否衝堂等）。
* 管理「最愛/納入/鎖定」課程，並以課表視覺化呈現。
* 將使用者課表與選課狀態儲存為 .xlsx，並保留登入歷史。
* 產生「最佳選課組合」候選（最多 5 組），以「總學分最大化」並以最愛排序優先度作為同分時的排序依據。

本專案唯一入口為 `python app_main.py`。

## (2) 重要變數（必填）

* ENV_NAME：course_query

  * 格式：英文小寫 + 底線（lowercase_with_underscore）
  * 用途：Conda 環境名稱；同時作為 GitHub repository 命名依據
* workspace root(EXE_NAME)：師大課程查詢系統

  * 值：專案根目錄資料夾名稱（basename）
  * 用途：打包輸出執行檔命名基準；亦作為本 README H1 與樹狀結構根目錄標示

## (3) workspace root(EXE_NAME) 定義

* workspace root(EXE_NAME) 指「專案根目錄資料夾名稱（basename）」。
* 本 README 使用的 `師大課程查詢系統/` 僅作為「根目錄表示」，不是要求建立同名子資料夾。
* 打包後輸出執行檔名稱必須使用 workspace root(EXE_NAME) 的值（本專案為「師大課程查詢系統」）。

## (4) 檔案與資料夾結構（樹狀；最小必要集合）

```text
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
│  └─ user_schedules/
├─ dist/
└─ build/
```

* `user_data/`：所有輸入/輸出/設定的預設放置位置（見 (6)）。
* `dist/`：PyInstaller 打包輸出資料夾（見 (9)）。
* `build/`：PyInstaller 打包過程中間產物資料夾。

## (5) Python 檔名規則（app_main.py + app_*.py 同層）

* 主入口檔：`app_main.py`
* 模組檔：`app_*.py`
* `app_main.py` 與所有 `app_*.py` 必須位於同一層（同層目錄）。
* 執行與測試唯一入口：`python app_main.py`

## (6) user_data/ 規範（所有輸入/輸出/設定預設放在 user_data/）

### 6.1 user_data 根目錄位置

* 開發期：`user_data/` 位於 workspace root(EXE_NAME) 之下。
* 打包後：`user_data/` 位於 `.exe` 同層（即執行檔所在資料夾）。

### 6.2 課程 Excel 放置位置（輸入）

* 預設課程檔資料夾：`user_data/course_inputs/`
* 啟動時會嘗試從 `user_data/course_inputs/` 自動載入一個 .xls/.xlsx（依檔名排序）。
* 你也可以在程式內使用「檔案 → 開啟課程 Excel…」選取檔案；選取後程式會自動複製到 `user_data/course_inputs/`。

課程 Excel 需包含下列必要欄位（任一工作表符合即可）：

* 開課序號
* 開課代碼
* 系所
* 中文課程名稱
* 教師
* 學分
* 必/選
* 全/半
* 地點時間
* 限修人數
* 選修人數

### 6.3 使用者資料保存位置（輸出）

* 使用者資料根目錄：`user_data/user_schedules/`
* 每位使用者會建立獨立資料夾：`user_data/user_schedules/<username>/`
* 歷史紀錄資料夾：`user_data/user_schedules/<username>/history/`
* 最佳選課輸出資料夾：`user_data/user_schedules/<username>/best_schedule/`

備註：本專案以 `.xlsx` 形式保存使用者的最愛/納入/鎖定與課表匯出結果；若需備份或移機，建議直接整份複製 `user_data/`。

## (7) Conda 環境（ENV_NAME）與安裝規範

### 7.1 原則

* 安裝與執行以 Conda 環境為主，避免要求全域安裝或修改系統 PATH。
* 安裝套件優先使用 `conda install`（建議 `conda-forge`）；只有在 conda 依賴解算/版本相容性因素導致不可行時，才改用 `pip install`。
* 下列指令皆以 Windows CMD 為目標 shell。

### 7.2 從零開始安裝（提供三套方案）

A. 推薦方案（conda 優先；安裝成功率與相依一致性最佳）

```cmd
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge pyside6 numpy pandas openpyxl xlrd pyinstaller -y
python -c "import PySide6, numpy, pandas, openpyxl; print('OK')"
```

B. 備援方案（conda + pip；當 conda-forge 解相依失敗或 PySide6/pyinstaller 版本衝突時使用）

```cmd
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge numpy pandas openpyxl xlrd -y
pip install pyside6 pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl; print('OK')"
```

C. 最後手段（pip only；當 conda-forge 連線/解相依長期不可用時使用）

```cmd
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
pip install pyside6 numpy pandas openpyxl xlrd pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl; print('OK')"
```

推薦採用：A（conda 優先）。理由：本專案依賴 PySide6 與科學計算/資料套件（numpy/pandas），以 conda-forge 的相依組合通常在 Windows 上最穩定。

## (8) 測試方式（只測 python app_main.py；兩時點）

> 測試前提：所有命令預設以「專案根目錄」為工作目錄執行；若不在該目錄，必須先 `cd` 進入 workspace root(EXE_NAME)。

### 8.1 安裝完成後的測試（時點 1）

```cmd
cd /d "<你的專案路徑>\師大課程查詢系統"
call conda.bat activate course_query
python app_main.py
```

判定標準（最低）：程式能正常啟動並顯示主視窗；關閉視窗後程序正常結束。

（可選）若要做快速煙霧測試（自動啟動後短暫即退出），可用：

```cmd
cd /d "<你的專案路徑>\師大課程查詢系統"
call conda.bat activate course_query
python app_main.py --smoke-test
```

### 8.2 修改/更新後的回歸測試（時點 2）

在任何程式碼修改、依賴調整、或打包參數變更後，需再次執行同一測試：

```cmd
cd /d "<你的專案路徑>\師大課程查詢系統"
call conda.bat activate course_query
python app_main.py
```

判定標準同 8.1。

## (9) 打包成 .exe（必填；提供可複製指令；不測試 .exe）

* `.exe` 檔名必須使用 workspace root(EXE_NAME) 的值：`師大課程查詢系統`。
* 打包輸出預設位於 `dist/`；打包中間產物位於 `build/`。
* 本專案不要求也不進行 `.exe` 測試；僅需確保 (8) 的 `python app_main.py` 兩時點測試通過。

### 9.1 推薦（onedir；對 PySide6 GUI 通常較穩定）

```cmd
cd /d "<你的專案路徑>\師大課程查詢系統"
call conda.bat activate course_query
pyinstaller --noconfirm --clean --name "師大課程查詢系統" --windowed app_main.py
```

輸出位置（常見）：

* `dist/師大課程查詢系統/師大課程查詢系統.exe`

### 9.2 備援（onefile；需要單一檔案分發時使用）

```cmd
cd /d "<你的專案路徑>\師大課程查詢系統"
call conda.bat activate course_query
pyinstaller --noconfirm --clean --onefile --name "師大課程查詢系統" --windowed app_main.py
```

備註：打包後程式仍會在 `.exe` 同層建立/使用 `user_data/`（含 `course_inputs/` 與 `user_schedules/`）。

## (10) 使用者要求（必填；長期約束；需持續維護）

* 本專案以 Windows 11（win-64）為主要目標環境。
* 依賴管理以 Conda 為主（ENV_NAME：`course_query`），優先 `conda install -c conda-forge`；僅在 conda 不可行時才使用 pip。
* 所有輸入/輸出/設定預設放置於 `user_data/`（以及其子資料夾 `course_inputs/`、`user_schedules/`），避免將資料散落到其他位置。
* 所有命令列指令預設以「專案根目錄（workspace root(EXE_NAME)）」為工作目錄；若不在該目錄，必須先 `cd` 進入後再執行。
* 打包 `.exe` 檔名必須使用 workspace root(EXE_NAME) 的值：`師大課程查詢系統`。

## (11) GitHub操作指令（必填；必須置於 README.md 最後面；內容必須完全一致；凍結區塊）

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
git remote add origin https://github.com/peicd100/course_query.git
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
