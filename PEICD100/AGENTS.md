from：https://hackmd.io/MujzjuDnTn2vPir2EcVYyw
from:https://chatgpt.com/g/g-p-694775493bb48191a277ba30b540ae2c-peicd/c/696b7d83-9504-8321-b3ae-bff924dfb3c4

# AGENTS.md（供 VS Code / IDE Agent 遵守的唯一作業規範）
# 適用：Codex、GitHub Copilot、Gemini Code Assist、以及任何具備「讀寫 workspace 檔案」能力的 Agent
#
# 核心目標（已調整）：
# - 所有模式：不實際刪除任何檔案或資料夾；只要依照本文件規則「產出可刪清單（含理由）」
# - APP_MAIN_FREE_*：限制最多、流程最完整（README/Log/鎖定檔/測試/可刪清單/打包 全部要做）
# - APP_MAIN_NO_TERMINAL_GEMINI：以 APP_MAIN_FREE 為基礎，但「終端機功能關閉」且「所有需要終端機的規定一律略過」
# - FREE_*：只保留最核心的「系統安全 + conda 環境安全」規定（但仍必須建立/維護 README.md 與 Log.md）
# - CHATGPT vs COPILOT：差異僅在「conda 進入/使用方式」，其餘規則完全一致
# - 使用說明權威：workspace root 的 README.md 為唯一完整使用說明來源；若不存在必須自動建立
#
# Git / GitHub 原則（已採用）：
# - Agent 禁止在終端機執行任何 git 指令（版本控制一律由使用者自行處理）
# - README.md 必須包含可複製的 GitHub 操作指令（僅文件；不執行）
# - dist/、build/ 不上傳：改用 .gitignore（由使用者自行執行初始化指令寫入），例行上傳用 git add .
#
# 重要變更（已採用）：
# - 不使用 backup/ 備份（版本控制由使用者自行處理）
# - 恢復 Log.md：用於累積記錄更新歷程與關鍵結果（與 Git 並存）
# - 刪除行為全面改為「只列出可刪清單，不實際刪」

================================================================================
0. 讀取優先（硬性；必須最先完成）
================================================================================

0.1 在做任何事情之前，你必須先「從頭到尾完整讀完」本 AGENTS.md。
- 不得讀到一半就開始任何動作（包含握手、詢問、執行命令、修改檔案）。
- 不得依賴先前記憶或上次讀取結果；本次任務必須重新完整讀取一次。

0.2 若你無法完整讀取本文件（權限/沙箱/截斷/讀取失敗等）：
- 你必須立刻停止
- 在對話回覆說明原因與影響
- 不得自作主張開始握手或行動

================================================================================
1. 全域硬規則（所有模式都必須遵守）
================================================================================

1.1 語言
- 對話回覆一律使用繁體中文（程式碼/命令/路徑可用英文）。
- 禁止使用任何 emoji、顏文字或表情符號。

1.2 行動前置（握手與模式選擇）
- 在你完成「啟動握手」且使用者完成「模式選擇」之前：
  - 不得執行任何命令（含 python/conda/pip/pyinstaller/git）
  - 不得修改任何檔案
  - 不得進行任何會改變 workspace 狀態的動作
- 例外：無（握手階段不得做任何“嘗試性執行”；只能盤點與回報你目前可見的資訊）

1.3 封閉範圍
- 你的任何檔案操作必須限制在 workspace root 之內（VS Code 目前開啟的資料夾根目錄）。
- 禁止修改 workspace root 以外的任何檔案或設定。

1.4 禁止改系統設定 / 全域設定
- 嚴禁任何系統或全域設定修改：
  - 永久 PATH、永久環境變數
  - PowerShell ExecutionPolicy
  - 登錄檔
  - 需要管理員權限的設定
  - 全域安裝程式（exe/msi）
- 只能使用 Anaconda/Conda 管理 Python 環境；禁止 venv、pipx、poetry、uv、rye、pyenv 等。

1.5 禁止外部 GUI 指令
- 禁止使用會彈出視窗或外部 GUI 編輯器/檢視器的終端機指令（例如 notepad、start、code 等）。
- 檔案內容的檢視/修改必須用 IDE 的檔案能力完成。

1.6 禁止無效重試
- 禁止在受限環境中反覆重試同一件必然失敗的事。
- 一旦確認受限，必須立刻停止重試並清楚回報：
  - 限制是什麼
  - 影響是什麼
  - 替代方案是什麼

1.7 違規拒絕
- 若使用者要求違反任何硬規則，你必須拒絕並指出違反哪一條（章節編號），並提出合規替代方案（若存在）。

1.8 Git 指令禁令（硬性；所有模式）
- 在任何模式下，你禁止在終端機執行任何 git 指令（包含但不限於 git init/add/commit/push/fetch/pull/reset/clean/status 等）。
- 版本控制與 GitHub 操作一律由使用者自行處理。
- 你仍必須維護 README.md 中的「GitHub操作指令」章節（作為使用者可複製執行的指令文件）。

1.9 刪除行為禁令（硬性；所有模式）
- 你不得刪除任何檔案或資料夾。
- 任何原本規定「必須刪除」之處，均改為「必須列入可刪清單」並附上理由與路徑。
- 你仍必須依照白名單/判定規則完成分析與清單輸出。

================================================================================
2. 啟動握手（必做；硬性；列出模式並等待使用者選擇）
================================================================================

在開始任何動作之前，你必須先在對話回覆中輸出以下 1)～12)。
你必須完整輸出，不得省略。輸出完後必須停止，等待使用者選擇模式。

1) 我已在本次任務中「重新完整讀取」並正在遵守本檔案（AGENTS.md）：是 / 否
2) 我實際讀取到的 AGENTS.md 路徑：<絕對路徑或可定位路徑>
3) 我判定的 workspace root（VS Code 開啟的資料夾根目錄）：<絕對路徑>

4) 我偵測到的專案狀態（擇一）：
   - A. 既有專案（workspace root 同層已存在 app_main.py）
   - B. 新專案/空專案（workspace root 同層尚不存在 app_main.py，需要從無到有建立）

5) 可用模式清單（請使用者選擇其一；不得自行預設）：
   - APP_MAIN_FREE_CHATGPT
   - APP_MAIN_FREE_COPILOT
   - APP_MAIN_NO_TERMINAL_GEMINI
   - FREE_CHATGPT
   - FREE_COPILOT

6) 請使用者回覆要使用的模式（必須回覆其中一個字串）：
   APP_MAIN_FREE_CHATGPT / APP_MAIN_FREE_COPILOT / APP_MAIN_NO_TERMINAL_GEMINI / FREE_CHATGPT / FREE_COPILOT

7) 能力盤點（必填；簡短但具體）：
   - 檔案：可否讀取/修改/新增 workspace 內檔案：是/否（若否，說明原因）
   - 終端機：可否執行命令：是/否（若否，說明原因）
   - 網路：可否連線（conda/pip 下載）：是/否（若否，說明原因）
   - pylanceRunCodeSnippet：是否存在且可用：是/否/不確定（握手階段不得嘗試；只能回報你“已知/可見”的狀態）

8) 你預計使用的 conda 進入方式（只列出，不得執行）：
   - *_CHATGPT：使用 5.2.1 的 cmd + activate.bat + conda activate
   - *_COPILOT：允許任何方式（含 pylanceRunCodeSnippet/conda run/conda activate/conda.exe 絕對路徑等），但必須遵守 5.3 的環境安全驗證
   - APP_MAIN_NO_TERMINAL_GEMINI：終端機功能關閉；所有終端機規定一律略過

9) 你必須承諾：本次任務不使用 notepad/start/code 等 GUI 指令。

10) 你必須列出任務完成時的固定完成宣告（只列出，不得提前輸出）：
    - # PEICD100您交代的事情已經全數完成

11) Git 指令執行狀態（硬性；必填）：
    - 我是否會在終端機執行任何 git 指令：否（硬性禁止；見 1.8）
    - 我是否會修改 README.md 中的「GitHub操作指令」章節：是（僅維護文件；不執行）

12) 在使用者選定模式之前：
    - 你必須停止於此
    - 不得執行任何命令、不得修改任何檔案

================================================================================
3. 模式定義與模式進入宣告（硬性）
================================================================================

3.1 模式切換唯一來源
- 模式切換只能由使用者明確指示。
- 未選模式前不得行動。

3.2 進入模式固定句（硬性；必須完全一致）
使用者選定模式後，你必須在「下一次回覆的最開頭」輸出對應固定句（完全一致）：
- 已進入APP_MAIN_FREE_CHATGPT模式
- 已進入APP_MAIN_FREE_COPILOT模式
- 已進入APP_MAIN_NO_TERMINAL_GEMINI模式
- 已進入FREE_CHATGPT模式
- 已進入FREE_COPILOT模式

3.3 模式語意（硬性）

A) APP_MAIN_FREE_CHATGPT
- 限制最多、流程最完整：必須執行本文件第 4～10 章全部要求（含終端機行為；但不含 git 指令；且不實際刪除）
- conda 進入方式：5.2.1（cmd + activate.bat）
- 允許終端機：是

B) APP_MAIN_FREE_COPILOT
- 限制最多、流程最完整：必須執行本文件第 4～10 章全部要求（含終端機行為；但不含 git 指令；且不實際刪除）
- conda 進入方式：允許任何方式，但必須遵守 5.3 的環境安全驗證
- 允許終端機：是

C) APP_MAIN_NO_TERMINAL_GEMINI
- 以 APP_MAIN_FREE 為基礎，但：
  - 終端機功能：關閉（不得執行任何命令；包含 python/conda/pip/pyinstaller/git）
  - 所有「需要使用終端機」的規定：一律略過、不執行
  - 所有「不需要終端機」的規定：仍必須執行（例如 README.md、檔名規則、可刪清單、Log.md）

D) FREE_CHATGPT / FREE_COPILOT
- 只保留最核心的「系統安全 + conda 環境安全」規定（第 1 章與第 5 章）
- 但仍必須建立/維護 README.md 與 Log.md（第 4 章）
- FREE 模式只強制：README/Log 的存在、ENV_NAME 記錄與核心禁令（其餘可簡化，但不得矛盾）。

================================================================================
4. 使用說明權威：README.md 與 Log.md（所有模式都必須遵守）
================================================================================

4.1 唯一權威（硬性）
- 本專案「唯一完整使用說明來源」為：workspace root/README.md

4.2 自動建立（硬性）
- 若 workspace root 下不存在 README.md：你必須自動建立 README.md 並寫入 4.4 的章節骨架。

4.3 README.md 的 H1 規則（硬性）
- README.md 第一行必須為：# <workspace_root_basename>

4.4 README.md 必填章節（硬性）
README.md 必須至少包含以下章節（可依專案擴充，但不得刪除）：

(1) 專案概述

(2) workspace root 定義（VS Code 開啟的資料夾根目錄）

(3) 檔案與資料夾結構（樹狀；需與實際一致）

(4) Python 檔名規則（app_main.py + app_*.py 同層）

(5) user_data/ 規範（所有輸入/輸出/設定預設放在 user_data/）

(6) 重要變數（必填）
    - ENV_NAME：<英文小寫+底線；同時作為 GitHub repositories 命名依據>
    - EXE_NAME：<workspace root 資料夾名稱（basename）>

(7) Conda 環境（ENV_NAME）規範

(8) 從零開始安裝流程（必須提供兩種：手動/自動；皆可一鍵複製）
    - 兩種方式差異說明（必填）：
      - 手動法：解析時間點可能導致版本略有差異（非完全一致）
      - 自動法（鎖定檔法）：以 explicit-spec.txt 與 requirements.txt 重建，目標是最大程度一致
    - 註解不得寫在命令同一行（避免一鍵複製失敗）
    - 指令區塊內只放純命令

    (8.1) 手動安裝（硬性前置條件：必須先讀完所有程式碼才能產出）
    - 在撰寫本節內容之前，必須完成「4.5 手動安裝產出前置條件」。
    - 本節必須包含：
      - conda create / conda activate
      - conda install（優先）
      - 只有 conda 無法取得、版本不適用或相容性因素必要時才 pip install（原因需在命令區塊外獨立換行）
      - 最終 python app_main.py

    (8.2) 自動安裝（鎖定檔重建：explicit-spec.txt + requirements.txt）
    - 本節必須包含：
      - conda create -n <ENV_NAME> --file explicit-spec.txt
      - conda activate <ENV_NAME>
      - pip install -r requirements.txt
      - python app_main.py

(9) 鎖定檔（Lockfiles）：explicit-spec.txt 與 requirements.txt（必填）
    - 目的（必填）：
      - explicit-spec.txt：精準鎖定 conda 套件 URL（重建一致性最高）
      - requirements.txt：補上 pip-only 套件（conda explicit 不包含）
    - 產出方式（必填；必須可一鍵複製）：
      - conda activate <ENV_NAME>
      - conda list --explicit > explicit-spec.txt
      - pip freeze > requirements.txt
    - 檔案位置（必填）：
      - workspace root/explicit-spec.txt
      - workspace root/requirements.txt

(10) 測試方式（只測 python app_main.py；兩個時點；若程式不退出需主動 Ctrl+C）

(11) 打包成 .exe（必填；提供可複製指令；不測試 .exe）

(12) GitHub操作指令（必填；必須置於 README.md 最後面；內容必須完全一致）
    - 本段落的「內容必須完全一致」定義：
      - 除了下列「唯一允許變更」之外，其餘每一字每一行都不得變更（含空白、縮排、大小寫、引號、code fence）。
      - 唯一允許變更：
        - 僅允許將下方 URL 行中的 `https://github.com/peicd100/ENV_NAME.git` 之 `ENV_NAME` 字樣，
          替換為 README.md (6) 的 ENV_NAME 實際值。
      - 除此之外不得更動任何內容（包含 commit message）。
    - code fence 縮排規則（硬性）：
      - 下列每個 code block 的「```」與其內文命令行，必須具有相同縮排。

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
    git remote add origin https://github.com/peicd100/ENV_NAME.git
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

4.5 手動安裝產出前置條件（硬性；必須先完成才能撰寫 README (8.1)）
- 在撰寫 README 的「(8.1) 手動安裝」之前，你必須完成下列步驟，否則不得撰寫手動安裝內容：

(1) 完整閱讀程式碼範圍（硬性）
- 必須讀完 workspace root 下：
  - app_main.py（若存在）
  - 所有 app_*.py
- 並且必須檢視程式碼中引用的必要資源路徑（例如 user_data/ 下的設定檔、資料檔、模板等），以判定是否需要額外安裝/放置檔案。

(2) 依據程式碼推導依賴（硬性）
- 依實際 import、子模組使用、以及程式碼中提及的外部工具/套件需求，列出「必要套件清單」。
- 不得憑印象或使用通用模板。
- 若無法從程式碼確定是否必要，必須在 README 註明「可選/待確認」，不得硬寫成必裝。

(3) 手動安裝內容生成規則（硬性）
- 必須先用 conda 安裝（conda install -y ...），只有 conda 無法取得或相容性不適用時才使用 pip（pip install ...），且原因必須獨立換行寫在命令區塊外（避免影響一鍵複製）。
- 指令區塊內只放純命令，不得含註解。
- 內容必須包含：建立 env / 啟用 env / conda 安裝 / pip 安裝（若有）/ 最終 python app_main.py。

4.6 Log.md（硬性；所有模式都必須維護）
- 位置：workspace root/Log.md
- 若不存在：必須自動建立。
- 每次完成任何修改都必須追加新紀錄（H1 時間戳 YYYY-MM-DD HH:MM:SS）
- 每筆至少包含：變更摘要 / 影響範圍 / 檔案變更清單 / 測試結果摘要 / 鎖定檔更新狀態 / 可刪清單摘要

================================================================================
5. Conda / 環境安全核心（所有模式都必須遵守）
================================================================================

5.1 核心禁令（硬性）
- 嚴禁對 base install/remove（允許 activate base 作為入口）。
- 嚴禁改動任何非本專案 ENV_NAME 的 conda 環境（install/remove/upgrade 等皆禁止）。
- 嚴禁使用非 conda env 的 python 做 pip install（包含系統 python）。
- 禁止使用其他環境管理工具（venv、poetry、uv、rye、pyenv 等）。

5.2 conda 進入方式（硬性；CHATGPT vs COPILOT 唯一差異）
5.2.1 *_CHATGPT
- 使用 cmd + activate.bat：
  call "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3"
  conda activate base
  conda activate <ENV_PATH 或 ENV_NAME>

5.2.2 *_COPILOT
- conda 進入方式不限制（可用 pylanceRunCodeSnippet / conda run / conda activate / conda.exe 絕對路徑等）。
- 但每次涉及「安裝/執行/產生鎖定檔/打包」之前，必須完成 5.3 的環境安全驗證。

5.3 環境驗證（僅允許終端機的模式適用；NO_TERMINAL 略過）
- 驗證最終證據必須來自 python 本身：
  python -c "import sys; print(sys.executable); print(sys.prefix)"
- 必須能從輸出路徑辨識其落在 ENV_NAME（不可猜）。
- 若無法驗證：必須停止相關行為（安裝/打包/鎖定檔/測試）。

================================================================================
6. APP_MAIN_FREE_*：完整流程（限制最多；不含 git 指令；且不實際刪除）
================================================================================

6.1 README.md / Log.md（硬性；必做）
- 必須確保 README.md 存在且為唯一完整使用說明來源。
- 必須確保 Log.md 存在並依 4.6 追加紀錄。
- 你不得執行任何 git 指令（見 1.8）。

6.2 鎖定檔輸出（需要終端機；必做）
- conda list --explicit > explicit-spec.txt
- pip freeze > requirements.txt

6.3 測試（需要終端機；必做；只測 python app_main.py）
- 兩個時點必測：
  (1) 改碼後、產出可刪清單之前
  (2) 打包前：先產出可刪清單，再測
- 通過判定：
  - 連續觀察 5–15 秒不得出現任何錯誤資訊
  - 若程式未自行退出：由 Agent 主動 Ctrl+C 中止

6.4 可刪清單（硬性；必做；不實際刪除）
- 對白名單以外的每個檔案/資料夾，必須先「讀取其內容」以判定必要性。
- 判定規則（硬性；偏向列入清單）：
  - 只要無法從程式碼（app_main.py / app_*.py）或 README.md 推導「確實會用到」，就列入可刪清單。
  - 只要看起來是中間產物/暫存/舊輸出/重複檔/未被引用之資源，就列入可刪清單。
- 可刪清單每筆至少包含：
  - 路徑（相對於 workspace root）
  - 類型（檔案/資料夾）
  - 判定理由（簡短但具體）
  - 風險等級（低/中/高）
- README 的樹狀結構維持實際存在狀態；可附「預期刪除後樹狀（參考）」但不得取代實際樹狀。

6.5 打包（需要終端機；必做；不測 .exe）
- EXE_NAME 必須等於 README.md (6) 的 EXE_NAME，且等於 workspace root 資料夾名稱（basename）。
- 打包方式由 Agent 自行判斷最穩方法（spec/onedir/onefile 皆可），但 README.md 必須提供至少一組可複製的 PyInstaller 指令。
- 不測試 .exe；僅需確保 python app_main.py 的兩時點測試通過。

================================================================================
7. APP_MAIN_NO_TERMINAL_GEMINI：基於 APP_MAIN_FREE，但終端機規定全部略過
================================================================================

7.1 終端機關閉（硬性）
- 不得執行任何命令（含 python/conda/pip/pyinstaller/git）。

7.2 規則裁決（硬性）
- 所有「需要終端機」的規定一律略過、不執行（含 5.3、6.2、6.3、6.5）。
- 所有「不需要終端機」的規定仍必須執行：
  - README.md（第 4 章）
  - Log.md（第 4.6）
  - 可刪清單（6.4；以靜態分析產出；略過測試門檻）

================================================================================
8. 白名單（不得列入可刪清單；硬性）
================================================================================

- .git/
- .gitignore（若存在）
- README.md
- Log.md
- explicit-spec.txt（若存在）
- requirements.txt（若存在）
- dist/
- dist/user_data/
- user_data/
- PEICD100/（若存在）
- app_main.py（若存在）
- app_*.py（若存在）

================================================================================
10. 完成宣告（硬性；所有模式都必須遵守）
================================================================================

# PEICD100您交代的事情已經全數完成
