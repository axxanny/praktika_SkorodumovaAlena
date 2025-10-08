import os
import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, 
                             QMessageBox, QGroupBox, QProgressBar, QTextEdit,
                             QSplitter, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPalette
from image_module.image_processor import ImageProcessor

class ProcessingThread(QThread):
    """
    Поток для обработки изображений (чтобы не блокировать GUI)
    """
    finished = pyqtSignal(str, str)  
    progress = pyqtSignal(int)      
    
    def __init__(self, operation, image_path, destination_folder=None):
        super().__init__()
        self.operation = operation
        self.image_path = image_path
        self.destination_folder = destination_folder
        self.processor = ImageProcessor()
    
    def run(self):
        try:
            self.progress.emit(10)
            
            if self.operation == "grayscale":
                result_path = self.processor.convert_to_grayscale(self.image_path)
                self.progress.emit(100)
                self.finished.emit("success", f"Изображение преобразовано в черно-белое:\n{result_path}")
                
            elif self.operation == "move":
                if not self.destination_folder:
                    self.finished.emit("error", "Не указана папка назначения")
                    return
                
                result_path = self.processor.move_image(self.image_path, self.destination_folder)
                self.progress.emit(100)
                self.finished.emit("success", f"Изображение перемещено:\n{result_path}")
                
            else:
                self.finished.emit("error", "Неизвестная операция")
                
        except Exception as e:
            logging.error(f"Ошибка в потоке обработки: {e}")
            self.finished.emit("error", f"Ошибка обработки: {str(e)}")

class MainWindow(QMainWindow):
    """
    Главное окно приложения - Модуль взаимодействия с пользователем
    """
    
    def __init__(self):
        super().__init__()
        self.current_image_path = ""
        self.processing_thread = None
        self.init_ui()
        self.init_data_storage()
        
    def init_data_storage(self):
        """
        Инициализация хранения данных о операциях
        """
        self.operations_history = []
        self.settings = {
            'last_used_folder': '',
            'default_destination': '',
            'auto_open_result': True
        }
        
    def init_ui(self):
        """
        Инициализация пользовательского интерфейса
        """
        self.setWindowTitle("Project 5 - Обработка изображений")
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("Project 5 - Изменение цветовой гаммы и перемещение изображений")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: 