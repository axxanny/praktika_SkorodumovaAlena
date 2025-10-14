import os
import datetime
import tkinter as tk

class ImageInfo:
    def get_image_info(self, file_path):
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл {file_path} не найден")
            return None

        try:
            root = tk.Tk()
            root.withdraw()  
            
            img = tk.PhotoImage(file=file_path)
            width = img.width()
            height = img.height()

            root.destroy()

            file_size_bytes = os.path.getsize(file_path)
            creation_timestamp = os.path.getctime(file_path)
            creation_date = datetime.datetime.fromtimestamp(creation_timestamp)
            file_extension = os.path.splitext(file_path)[1].upper().replace('.', '')

            color_mode = 'RGB' if file_extension in ['JPG', 'JPEG', 'BMP'] else 'RGBA'

            info = {
                'file_name': os.path.basename(file_path),
                'file_size': {
                    'bytes': file_size_bytes,
                    'kb': round(file_size_bytes / 1024, 2),
                    'mb': round(file_size_bytes / (1024 * 1024), 2)
                },
                'resolution': {
                    'width': width,
                    'height': height,
                    'text': f"{width} x {height}"
                },
                'format': file_extension,
                'color_mode': color_mode,
                'creation_date': creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                'directory': os.path.dirname(file_path)
            }
            return info

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            try:
                root.destroy()
            except:
                pass
            return None

    def is_valid_image(self, file_path):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
        if not os.path.exists(file_path):
            return False
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in valid_extensions