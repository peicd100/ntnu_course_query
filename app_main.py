# -*- coding: utf-8 -*-
r"""專案架構與環境:
  完整使用說明請見 README.md
  所有輸入/設定預設放在 user_data/
"""

from __future__ import annotations

import os
import sys
import traceback

# 設定 High DPI 縮放策略 (必須在建立 QApplication 之前)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from app_mainwindow import MainWindow


def main() -> int:
    # 啟用 High DPI 支援 (針對 PySide6/Qt6 的相容性設定)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    smoke_test = "--smoke-test" in sys.argv[1:]

    qt_args = [sys.argv[0]] + [arg for arg in sys.argv[1:] if arg != "--smoke-test"]

    app = QApplication(qt_args)
    app.setApplicationName("師大課程查詢系統")

    try:
        w = MainWindow()
        w.show()

        if smoke_test:
            QTimer.singleShot(400, app.quit)

        return app.exec()

    except Exception:
        # 確保有 QApplication 實例以顯示錯誤訊息
        if not QApplication.instance():
            _ = QApplication(sys.argv)
            
        error_message = f"發生未預期的嚴重錯誤，應用程式即將關閉。\n\n錯誤資訊：\n{traceback.format_exc()}"
        QMessageBox.critical(None, "應用程式錯誤", error_message)
        return 1

if __name__ == "__main__":
    sys.exit(main())
