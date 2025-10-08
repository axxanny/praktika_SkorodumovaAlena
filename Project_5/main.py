import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from gui_module.main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project5.log'),
        logging.StreamHandler()
    ]
)

def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Project5 - Image Processor")
        app.setApplicationVersion("1.0")
        
        window = MainWindow()
        window.show()
        
        logging.info("Приложение Project5 успешно запущено")
        return app.exec_()
        
    except Exception as e:
        logging.error(f"Ошибка при запуске приложения: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())