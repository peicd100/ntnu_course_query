# 師大課程查詢系統

## 1. 專案概述

「師大課程查詢系統」是一套以 **PySide6（Qt for Python）** 製作的桌面 GUI 工具，透過讀取師大課程 Excel 檔（.xls / .xlsx），提供：

* 多條件課程查詢（開課序號、開課代碼、課名、教師、系所、全面關鍵字）。
* 課程分類快速篩選（通識 / 一般體育 / 教育學程）。
* 我的最愛管理（勾選顯示於課表、鎖定課程、拖曳排序、優先度）。
* 課表檢視（支援衝突顯示、顯示時間列、顯示週六、縮放）。
* 時段選取篩課（以滑鼠拖曳課表格子選取可上課時段，並可設定匹配模式）。
* 使用者歷史紀錄（只讀檢視歷史檔、套用歷史紀錄）。
* 最佳選課（在「已選/候選」最愛中，依「總學分最大化」並以「優先度和」作為同分排序，輸出最多 5 組方案檔）。

本專案以 Windows 11 + Conda（Miniforge/Anaconda）為主要安裝與執行環境，並以 `app_main.py` 作為唯一入口點。

---

## 2. 重要變數

* ENV_NAME：`course_query`
* workspace root(EXE_NAME)：`師大課程查詢系統`

---

## 3. workspace root(EXE_NAME) 定義

* **workspace root(EXE_NAME)** 代表：

  1. 你在本機存放專案的資料夾名稱（建議直接使用此名稱）。
  2. 使用 PyInstaller 打包後的 `.exe` 主要輸出名稱（建議與資料夾同名，以利辨識與佈署）。

---

## 4. 檔案與資料夾結構

以下為最小必要結構（含 `user_data/` 規範資料夾；其子資料夾多由程式首次執行時自動建立）：

```
師大課程查詢系統/
  README.md
  app_main.py
  app_constants.py
  app_excel.py
  app_mainwindow.py
  app_timetable_logic.py
  app_user_data.py
  app_utils.py
  app_widgets.py
  app_workers.py
  user_data/
    .gitkeep
    course_inputs/
      .gitkeep
    user_schedules/
      .gitkeep
  dist/
  build/
```

* `app_main.py`：唯一入口點（GUI 啟動與 smoke test）。
* `app_mainwindow.py`：主視窗與主要互動邏輯。
* `app_excel.py`：Excel 讀取、工作表選擇、必要欄位驗證、資料清理與索引欄位生成。
* `app_timetable_logic.py`：課表矩陣生成、衝突檢測與車道（lane）排版。
* `app_user_data.py`：使用者資料檔（.xlsx）讀寫、歷史紀錄與最佳方案輸出路徑。
* `app_workers.py`：背景執行（自動儲存、最佳選課運算與輸出）。
* `app_widgets.py`：GUI 元件（課表、結果表格、我的最愛表格等）。
* `user_data/`：使用者資料與輸入課程檔的**唯一落地位置**（打包後亦需保留）。
* `dist/`、`build/`：PyInstaller 產物（通常不提交版本控制）。

---

## 5. Python 檔名規則

* **入口檔固定**：`app_main.py`。
* 其他模組檔名均以 `app_*.py` 命名，維持「功能分層」與「可追蹤性」。
* 若未來擴充：

  * GUI / 視窗：優先放在 `app_mainwindow.py` 或拆分到 `app_views_*.py`（仍以 `app_` 為前綴）。
  * 純計算邏輯：優先放在 `app_utils.py` / `app_timetable_logic.py` / `app_workers.py`。

---

## 6. user_data/ 資料夾規範

### 6.1 目的

`user_data/` 是本程式所有可變資料（輸入檔、副本、使用者狀態、輸出方案）的唯一落地位置，方便：

* 專案資料與使用者資料分離。
* 打包後可直接攜帶 `user_data/` 進行移機或備份。

### 6.2 子資料夾與用途

* `user_data/course_inputs/`

  * 放置「課程 Excel」檔案（`.xls` / `.xlsx`）。
  * 程式啟動時會嘗試自動載入此資料夾中的課程檔。
  * 透過「檔案 → 開啟課程 Excel…」選取檔案後，程式會自動將檔案**複製**到此資料夾，再進行讀取。

* `user_data/user_schedules/`

  * 使用者資料根目錄；每位使用者會建立一個資料夾（名稱會做安全化處理）。
  * 每位使用者下至少包含：

    * `history/`：登入時自動建立的本次登入檔（`YYYYMMDD_HHMMSS.xlsx`），並由程式自動儲存更新。
    * `best_schedule/`：最佳選課輸出（多個 `.xlsx`）與快取（`best_schedule_cache.json`）。

### 6.3 使用者檔案格式（.xlsx）

每個使用者檔案包含兩個工作表：

* `我的最愛`

  * 欄位：`開課序號`、`課表`（是否顯示於課表）、`鎖定`（強制保留於課表）、`加入順序`（用於優先度/最佳選課排序）。

* `課表匯出`

  * 匯出目前顯示於課表的課程明細（保留原始欄位並附加 `_tba`、`_slots`）。

---

## 7. Conda 環境（course_query）與安裝規範

### 7.1 取得專案原始碼（必做）

請先完成 clone 與進入專案目錄（以下命令必須置於同一個文字框內）：

```
git clone https://github.com/peicd100/course_query.git 師大課程查詢系統
cd 師大課程查詢系統
```

### 7.2 Excel 檔格式要求（讀取前檢核）

課程 Excel 的目標工作表必須包含下列欄位（缺一不可）：

* `開課序號`
* `開課代碼`
* `中文課程名稱`
* `教師`
* `學分`
* `系所`
* `上課時間`
* `人數`
* `限修人數`

說明：

* `.xlsx` 依賴 `openpyxl`。
* `.xls` 可能需要額外安裝 `xlrd`（建議一併安裝以避免讀取失敗）。

### 7.3 安裝方案（請擇一；Windows CMD；可一鍵複製）

注意事項：

* 下列命令皆以 **Windows CMD** 為基準（啟用 conda 請使用 `call conda.bat activate ...`）。
* 每套方案最後一行皆含最小驗證（匯入依賴 + 啟動 smoke test）。
* 若你要進入完整互動模式，將最後一行的 `--smoke-test` 移除即可。

#### 方案 A（建議；conda-forge 為主；pip 補足 .xls 讀取）

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge pyside6 numpy pandas openpyxl pyinstaller -y
python -m pip install xlrd
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('deps-ok')" && python app_main.py --smoke-test
```

#### 方案 B（備用；若 conda 解相依遇到 Qt/平台衝突，改用 pip 安裝 GUI/打包套件）

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge numpy pandas openpyxl -y
python -m pip install pyside6 pyinstaller xlrd
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('deps-ok')" && python app_main.py --smoke-test
```

#### 方案 C（偏向 pip；僅用 conda 建 Python 與提供 pip）

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge pip -y
python -m pip install pyside6 numpy pandas openpyxl xlrd pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('deps-ok')" && python app_main.py --smoke-test
```

---

## 8. 測試與驗證（兩個時間點）

### 8.1 安裝完成後（最小驗證）

1. 啟用環境：

```
call conda.bat activate course_query
```

2. 執行 smoke test（視窗會短暫啟動後自動結束；無錯誤即視為通過）：

```
python app_main.py --smoke-test
```

### 8.2 改動程式碼後（互動驗證）

請執行完整 GUI 並人工確認主要流程：

```
python app_main.py
```

建議檢核項：

* 能自動或手動載入課程 Excel。
* 查詢條件變更能即時更新查詢結果。
* 勾選查詢結果的「最愛」可同步到「我的最愛」。
* 「我的最愛」中勾選「課表」可顯示在課表。
* 「鎖定」課程在最佳選課與課表中皆強制保留。
* 「檢視歷史紀錄」可讀取並套用歷史檔。
* 「最佳選課」可輸出最多 5 組方案到 `best_schedule/`。

---

## 9. 打包（PyInstaller）

本章僅提供打包指令與預期輸出位置；不在此章節驗證執行檔。

### 9.1 建議打包方式：onedir（較穩定）

```
call conda.bat activate course_query
pyinstaller --noconsole --clean --name "師大課程查詢系統" app_main.py
```

預期輸出：

* `dist/師大課程查詢系統/師大課程查詢系統.exe`
* 執行後會在 `dist/師大課程查詢系統/user_data/` 建立/使用使用者資料。

### 9.2 需要單一檔案時：onefile（便利但相依收集較敏感）

```
call conda.bat activate course_query
pyinstaller --noconsole --clean --onefile --name "師大課程查詢系統" app_main.py
```

預期輸出：

* `dist/師大課程查詢系統.exe`
* 執行後會在 `dist/user_data/` 建立/使用使用者資料。

---

## 10. 使用者要求（必填；長期約束；需持續維護）

* 全專案（包含 README）採用繁體中文（除非另有明確要求）。
* 主要執行環境為 Windows 11；指令以 Windows CMD 風格呈現。
* 安裝以 Conda 為主（優先 conda-forge）；僅在 conda 不可行或相依解衝突時使用 pip。
* `app_main.py` 為唯一入口點；README 與文件不可引導使用者以其他檔案作為入口。
* `workspace root(EXE_NAME)` 必須維持為 `師大課程查詢系統`，並作為 PyInstaller 的 `--name`。
* 所有可變資料必須落地在 `user_data/`（包含輸入課程檔副本、使用者歷史、最佳方案與快取）。
* `user_data/course_inputs/` 為課程 Excel 的唯一放置位置；「開啟課程 Excel」必須複製至此再讀取。
* 使用者資料檔案格式需向後相容（至少相容舊檔缺少 `鎖定` 欄位的情形）。
* `dist/`、`build/`、`user_data/` 的實際內容不應提交到 Git（可提交 `.gitkeep` 保留空資料夾結構）。

---

## 11. GitHub 操作

以下指令以 Windows CMD 為預設；請在專案根目錄（`師大課程查詢系統/`）執行。

### 11.1 初始化

```
git config --global user.name "peicd100"
git config --global user.email "peicd100@gmail.com"

git init
git add .
git commit -m "PEICD100"
git branch -M main
git remote add origin https://github.com/peicd100/course_query.git
git push -u origin main
```

### 11.2 例行上傳

```
git add .
git commit -m "PEICD100"
git push -u origin main
```

### 11.3 還原成 GitHub 最新資料

```
git rebase --abort || echo "No rebase in progress" && git fetch origin && git switch main && git reset --hard origin/main && git clean -fd && git status
```

### 11.4 查看儲存庫

```
git remote -v
```
