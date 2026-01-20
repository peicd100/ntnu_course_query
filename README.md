# 師大課程查詢系統

## (1) 專案概述
本專案為「師大課程查詢系統」，旨在提供課程查詢相關功能。

## (2) workspace root 定義
VS Code 開啟的資料夾根目錄：
`d:\x1064\PEICD100\0_python\1_師大課程查詢系統\師大課程查詢系統`

## (3) 檔案與資料夾結構
```text
師大課程查詢系統/
├── app_main.py          # 主程式入口
├── app_*.py             # 其他應用程式模組
├── user_data/           # 使用者資料 (輸入/輸出/設定)
├── PEICD100/            # 專案文件與 Agent 規範
├── explicit-spec.txt    # Conda 鎖定檔
├── requirements.txt     # Pip 鎖定檔
├── README.md            # 專案說明文件
├── Log.md               # 變更歷程記錄
└── .gitignore           # Git 忽略設定
```

## (4) Python 檔名規則
- 入口程式：`app_main.py`
- 同層模組：`app_*.py`

## (5) user_data/ 規範
- 所有輸入檔案、輸出結果、設定檔預設皆存放於 `user_data/` 資料夾中。

## (6) 重要變數
- **ENV_NAME**：`peicd100`
- **EXE_NAME**：`師大課程查詢系統`

## (7) Conda 環境 (ENV_NAME) 規範
- 本專案使用 Conda 環境名稱：`peicd100`

## (8) 從零開始安裝流程

### 兩種方式差異說明
- **手動法**：解析時間點可能導致版本略有差異（非完全一致）。
- **自動法（鎖定檔法）**：以 `explicit-spec.txt` 與 `requirements.txt` 重建，目標是最大程度一致。

### (8.1) 手動安裝
```bash
conda create -n peicd100 python=3.10 -y
conda activate peicd100
conda install -y requests pandas beautifulsoup4
python app_main.py
```
(註：若有其他 pip 套件需求，請自行執行 `pip install <package>`。)

### (8.2) 自動安裝
```bash
conda create -n peicd100 --file explicit-spec.txt
conda activate peicd100
pip install -r requirements.txt
python app_main.py
```

## (9) 鎖定檔 (Lockfiles)
### 目的
- `explicit-spec.txt`：精準鎖定 conda 套件 URL（重建一致性最高）。
- `requirements.txt`：補上 pip-only 套件（conda explicit 不包含）。

### 產出方式
```bash
conda activate peicd100
conda list --explicit > explicit-spec.txt
pip freeze > requirements.txt
```

### 檔案位置
- `workspace root/explicit-spec.txt`
- `workspace root/requirements.txt`

## (10) 測試方式
只測 `python app_main.py`；若程式不退出需主動 Ctrl+C。
```bash
python app_main.py
```

## (11) 打包成 .exe
```bash
pyinstaller --noconfirm --onedir --windowed --name "師大課程查詢系統" --clean app_main.py
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
git remote add origin https://github.com/peicd100/peicd100.git
git add .
git commit -m "PEICD100"
git push -u origin main
```

# 例行上傳
```
git add .
git commit -m "PEICD100"
git push
```

# 還原成Git Hub最新資料
```
git fetch origin && git switch main && git reset --hard origin/main && git clean -fd && git status
```

# 查看儲存庫
```
git remote -v
```