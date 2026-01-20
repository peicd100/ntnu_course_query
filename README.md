# 師大課程查詢系統

## (1) 專案概述
本專案為一個使用 Python 與 PySide6 開發的師大課程查詢系統桌面應用程式。

## (2) workspace root 定義（VS Code 開啟的資料夾根目錄）
`d:\x1064\PEICD100\0_python\1_師大課程查詢系統\師大課程查詢系統`

## (3) 檔案與資料夾結構
```
.
├── app_constants.py
├── app_excel.py
├── app_main.py
├── app_mainwindow.py
├── app_timetable_logic.py
├── app_user_data.py
├── app_utils.py
├── app_widgets.py
├── app_workers.py
├── Log.md
├── README.md
├── requirements.txt
├── .git/
├── PEICD100/
│   └── AGENTS.md
└── user_data/
    ├── course_inputs/
    └── user_schedules/
```

## (4) Python 檔名規則
- 主程式入口固定為 `app_main.py`。
- 其他所有 Python 模組檔案必須與 `app_main.py` 位於同一層，且檔名必須符合 `app_*.py` 的格式。

## (5) user_data/ 規範
- 所有使用者特定的輸入檔案、設定檔與輸出結果，都應存放於 `user_data/` 資料夾中。
- `dist/` 資料夾內也會包含一個 `user_data/`，用於存放打包後程式執行時所需的資料。

## (6) 重要變數
- **ENV_NAME**: `ntnu_course_query` (本專案 conda env 名稱，同時作為 GitHub repository 命名依據)
- **EXE_NAME**: `師大課程查詢系統` (workspace root 資料夾名稱)

## (7) Conda 環境（ENV_NAME）規範
本專案使用唯一的 Conda 環境：`ntnu_course_query`。
請勿使用 base 環境或其他環境進行開發或執行。

## (8) 從零開始安裝流程
以下提供兩種安裝方式，請擇一使用。

### 兩種方式差異說明
- **手動法**：解析時間點可能導致版本略有差異（非完全一致）。
- **自動法（鎖定檔法）**：以 `explicit-spec.txt` 與 `requirements.txt` 重建，目標是最大程度一致。

### (8.1) 手動安裝
```bash
conda create -n ntnu_course_query python=3.10
conda activate ntnu_course_query
conda install -c conda-forge pyside6 pandas requests openpyxl beautifulsoup4
python app_main.py
```

### (8.2) 自動安裝（鎖定檔重建）
```bash
conda create -n ntnu_course_query --file explicit-spec.txt
conda activate ntnu_course_query
pip install -r requirements.txt
python app_main.py
```

## (9) 鎖定檔（Lockfiles）：explicit-spec.txt 與 requirements.txt
- **目的**：
  - `explicit-spec.txt`：精準鎖定 conda 套件 URL（重建一致性最高）。
  - `requirements.txt`：補上 pip-only 套件（conda explicit 不包含）。
- **產出方式**（請在 `ntnu_course_query` 環境下執行）：
  ```bash
  conda activate ntnu_course_query
  conda list --explicit > explicit-spec.txt
  pip freeze > requirements.txt
  ```
- **檔案位置**：
  - `workspace root/explicit-spec.txt`
  - `workspace root/requirements.txt`

## (10) 測試方式
本專案主要測試 `app_main.py` 是否能正常啟動。
```bash
python app_main.py
```
建議在「修改程式碼後」與「打包前」各執行一次測試。

## (11) 打包成 .exe
使用 PyInstaller 進行打包：
```bash
pyinstaller --noconfirm --onedir --windowed --name "師大課程查詢系統" --add-data "user_data;user_data" app_main.py
```

## (12) GitHub操作指令
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
```bash
git add .
git commit -m "PEICD100"
git push
```

# 還原成Git Hub最新資料
```bash
git fetch origin && git switch main && git reset --hard origin/main && git clean -fd && git status
```

# 查看儲存庫
```bash
git remote -v
```
