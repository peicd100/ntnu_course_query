# 師大課程查詢系統

## 1. 專案概述

本專案為桌面版「課程查詢與排課系統」，以 `python app_main.py` 作為唯一入口。

核心功能（依程式現況）：

* 課程 Excel 載入：支援 `.xls / .xlsx`；可由「檔案 → 開啟課程 Excel…」選取，系統會自動複製到 `user_data/course_inputs/` 並讀取。
* 多條件查詢：開課序號、開課代碼、科目名稱、教師、全面搜尋、系所；可搭配通識/體育/教育學程等選項與「未滿額、排除衝突、排除已選、顯示無時間」等條件。
* 我的最愛與課表：可將課程加入「我的最愛」，並勾選是否顯示於課表；支援「鎖定」課程（鎖定課程強制顯示於課表）。
* 課表檢視：顯示已選總學分、已鎖定學分；可切換顯示週六與顯示時間。
* 歷史紀錄：可檢視過往使用者檔案並以只讀模式預覽。
* 最佳選課：以目前「我的最愛」為候選，計算並輸出多個不衝堂的最佳組合（最多 5 個結果），輸出為 Excel 檔。

## 2. 重要變數（必填）

1. ENV_NAME：`course_query`

   * 英文小寫 + 底線
   * 同時作為 GitHub repository 命名依據
2. workspace root(EXE_NAME)：`師大課程查詢系統`

   * 專案根目錄資料夾名稱（basename）

## 3. workspace root(EXE_NAME) 定義

* workspace root(EXE_NAME) 指「專案根目錄資料夾名稱（basename）」。
* 本專案文件敘述一律使用名詞 **workspace root(EXE_NAME)**；在命令列/檔名/路徑上，需直接使用其實際值 `師大課程查詢系統`。
* 格式限制：

  * 必須是 basename（不得包含 `/` 或 `\`）
  * 不得包含括號字樣 `(` `)`

## 4. 檔案與資料夾結構（樹狀；最小必要集合）

以下為本專案運作所需的最小集合（以 workspace root(EXE_NAME) 的實際值展示）：

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
│  └─ user_schedules/
├─ dist/                       （可能存在；打包輸出資料夾）
├─ build/                      （可能存在；打包中間產物）
└─ .gitignore                  （可能存在；需忽略 dist/、build/）
```

## 5. Python 檔名規則（app_main.py + app_*.py 同層）

* 主入口檔：`app_main.py`
* 模組檔：`app_*.py`
* `app_main.py` 與所有 `app_*.py` 必須位於同一層（workspace root(EXE_NAME) 根目錄）。

## 6. user_data/ 規範

本專案所有「輸入／輸出／設定」預設放在 `user_data/`，並由程式自動建立必要資料夾。

### 6.1 課程 Excel 放置規範

* 預設課程輸入資料夾：`user_data/course_inputs/`
* 你可以：

  1. 直接把課程 Excel 放入 `user_data/course_inputs/`（支援 `.xls / .xlsx`），再啟動程式。
  2. 或於程式內使用「檔案 → 開啟課程 Excel…」選取檔案；選取後會自動複製到 `user_data/course_inputs/`。

### 6.2 課程 Excel 內容要求（欄位）

程式會檢查課程 Excel 是否具備必要欄位；缺少欄位會視為格式錯誤。

必要欄位（REQUIRED_COLUMNS）：

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

工作表選擇：

* 優先尋找工作表名稱 `課程 / Courses / Sheet1`；若都不存在，會使用第一個工作表。

`.xls` 注意事項：

* 讀取 `.xls` 需要 `xlrd`；若未安裝，程式會提示安裝。

### 6.3 使用者資料保存規範

* 使用者資料保存根目錄：`user_data/user_schedules/`
* 每位使用者會建立一個子資料夾（以使用者名稱清理後作為資料夾名）。
* 主要子資料夾：

  * `history/`：每次「新增/切換」登入會建立一個時間戳的 Excel（作為該次會話檔）。
  * `best_schedule/`：最佳選課輸出的 Excel 檔，以及 `best_schedule_cache.json` 快取。

使用者檔案格式（Excel）：

* 工作表 `我的最愛`：包含「開課序號 / 課表 / 鎖定 / 加入順序」。
* 工作表 `課表匯出`：匯出顯示於課表的課程明細（含 `_tba`、`_slots` 等欄位）。

## 7. Conda 環境（ENV_NAME）與安裝規範

本章節最前面必須先提供 `git clone` 與 `cd` 兩行命令（同一個文字框）。

```
git clone https://github.com/peicd100/course_query.git 師大課程查詢系統
cd 師大課程查詢系統
```

以下提供三套安裝方案（Windows CMD）。

### A. 推薦方案（conda 優先）

* 目標：安裝成功率最高、相依一致、後續打包（PyInstaller）也一併就緒。

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge pyside6 numpy pandas openpyxl xlrd pyinstaller -y
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('OK')"
```

### B. 備援方案（conda + pip；針對 conda solver 在 GUI/打包套件上解析失敗的情境）

* 目標：若 `conda-forge` 在 `pyside6` / `pyinstaller` 解析或下載上遇到問題，改用 PyPI wheel 降低卡住機率。

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge numpy pandas openpyxl xlrd -y
pip install pyside6 pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('OK')"
```

### C. 最後手段（pip only；僅保留 conda 建環境，其餘全部 pip）

* 目標：在 conda-forge 網路/solver/鏡像不穩定時，以 pip wheels 完成安裝。

```
conda create -n course_query python=3.11 -y
call conda.bat activate course_query
conda install -c conda-forge pip -y
pip install pyside6 numpy pandas openpyxl xlrd pyinstaller
python -c "import PySide6, numpy, pandas, openpyxl, xlrd; print('OK')"
```

## 8. 測試方式（只測 python app_main.py；兩時點）

兩時點測試定義：

1. 安裝完成後測試：在乾淨環境中執行一次 `python app_main.py` 並確認通過。
2. 修改／更新後回歸測試：變更完成後再次執行 `python app_main.py` 並確認通過。

建議操作（Windows CMD）：

### 8.1 安裝完成後測試

```
call conda.bat activate course_query
python app_main.py
```

### 8.2 修改／更新後回歸測試

```
call conda.bat activate course_query
python app_main.py
```

補充（可選）：

* `python app_main.py --smoke-test` 會在短時間內自動結束，適合做最小啟動檢查（不取代上述兩時點測試定義）。

## 9. 打包成 .exe（必填；提供可複製指令；不測試 .exe）

* 打包輸出的 `.exe` 命名必須使用 workspace root(EXE_NAME) 的實際值：`師大課程查詢系統`。
* 不測試 `.exe`；只需確保第 8 節兩時點測試通過。

### 9.1 PyInstaller 指令（Windows CMD）

若你使用第 7 節 A 方案，通常已包含 `pyinstaller`；否則先確保環境中已安裝：

* `pip install pyinstaller` 或 `conda install -c conda-forge pyinstaller -y`

打包指令：

```
call conda.bat activate course_query
pyinstaller --noconfirm --clean --onefile --windowed --name "師大課程查詢系統" app_main.py
```

產物位置：

* 預期輸出：`dist/師大課程查詢系統.exe`
* 打包後執行時，`user_data/` 會以 `.exe` 同層作為根目錄，建議把課程 Excel 放在：`dist/user_data/course_inputs/`。

## 10. 使用者要求（必填；長期約束；需持續維護）

* 所有輸入／輸出／設定預設放在 `user_data/`（包含課程 Excel、使用者檔案、最佳選課輸出與快取）。
* 測試與執行以 `python app_main.py` 為唯一入口。
* 打包 `.exe` 名稱必須為 `師大課程查詢系統.exe`（PyInstaller `--name` 使用 `師大課程查詢系統`）。
* 安裝與相依管理以 conda 為優先；僅在 conda 不可行/相容性因素時才使用 pip。

## 11. GitHub操作指令（必填；必須置於 README.md 最後面；內容必須完全一致；凍結區塊）

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
