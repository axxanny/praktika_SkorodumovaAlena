import os
import shutil
import logging
from PIL import Image, ImageOps
from datetime import datetime

class ImageProcessor:
    """
    Модуль обработки и работы с изображениями
    """
    
    def __init__(self):
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
    
    def convert_to_grayscale(self, image_path):
        """
        Преобразование изображения в черно-белое
        
        Args:
            image_path (str): Путь к исходному изображению
            
        Returns:
            str: Путь к обработанному изображению
            
        Raises:
            Exception: Если обработка не удалась
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
            
            with Image.open(image_path) as img:
                grayscale_img = ImageOps.grayscale(img)
                
                original_name = os.path.splitext(os.path.basename(image_path))[0]
                original_ext = os.path.splitext(image_path)[1]
                output_filename = f"{original_name}_bw{original_ext}"
                output_path = os.path.join(os.path.dirname(image_path), output_filename)
                
                grayscale_img.save(output_path)
                
                logging.info(f"Изображение преобразовано в Ч/Б: {output_path}")
                return output_path
                
        except Exception as e:
            logging.error(f"Ошибка преобразования в Ч/Б: {e}")
            raise
    
    def move_image(self, image_path, destination_folder):
        """
        Перемещение изображения в указанную папку
        
        Args:
            image_path (str): Путь к исходному изображению
            destination_folder (str): Папка назначения
            
        Returns:
            str: Новый путь к изображению
            
        Raises:
            Exception: Если перемещение не удалось
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Исходный файл не найден: {image_path}")

            if not os.path.exists(destination_folder):
                raise FileNotFoundError(f"Папка назначения не найдена: {destination_folder}")
            
            if not os.path.isdir(destination_folder):
                raise ValueError(f"Указанный путь не является папкой: {destination_folder}")

            filename = os.path.basename(image_path)
            destination_path = os.path.join(destination_folder, filename)

            counter = 1
            original_name, original_ext = os.path.splitext(filename)
            while os.path.exists(destination_path):
                new_filename = f"{original_name}_{counter}{original_ext}"
                destination_path = os.path.join(destination_folder, new_filename)
                counter += 1

            shutil.move(image_path, destination_path)
            
            logging.info(f"Изображение перемещено: {image_path} -> {destination_path}")
            return destination_path
            
        except Exception as e:
            logging.error(f"Ошибка перемещения изображения: {e}")
            raise
    
    def get_image_info(self, image_path):
        """
        Получение информации об изображении
        
        Args:
            image_path (str): Путь к изображению
            
        Returns:
            dict: Информация об изображении
        """
        try:
            with Image.open(image_path) as img:
                info = {
                    'filename': os.path.basename(image_path),
                    'file_size': os.path.getsize(image_path),
                    'file_size_kb': round(os.path.getsize(image_path) / 1024, 2),
                    'dimensions': img.size,
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'creation_time': datetime.fromtimestamp(os.path.getctime(image_path)),
                    'modification_time': datetime.fromtimestamp(os.path.getmtime(image_path))
                }
                return info
        except Exception as e:
            logging.error(f"Ошибка получения информации об изображении: {e}")
            raise
    
    def validate_image(self, image_path):
        """
        Валидация изображения
        
        Args:
            image_path (str): Путь к изображению
            
        Returns:
            bool: True если изображение валидно
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            logging.error(f"Изображение невалидно: {e}")
            return False