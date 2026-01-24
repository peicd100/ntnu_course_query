@echo off
chcp 65001
echo 正在安裝依賴...
pip install -r requirements.txt
echo.
echo 正在執行單元測試...
python -m unittest test_timetable_logic.py
if %errorlevel% neq 0 (
    echo 測試失敗！請檢查程式碼。
    pause
    exit /b %errorlevel%
)
echo.
echo 正在打包執行檔...
pyinstaller main.spec --clean --noconfirm
echo.
echo 打包完成！執行檔位於 dist\師大課程查詢系統\師大課程查詢系統.exe
pause