import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from image_info import ImageInfo
from file_renamer import FileRenamer

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Анализатор изображений")
        self.root.geometry("700x550")

        self.image_info = ImageInfo()
        self.file_renamer = FileRenamer()
        self.current_file = None

        self.create_interface()

    def create_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        file_frame = ttk.LabelFrame(main_frame, text="Выбор изображения", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        select_button = ttk.Button(file_frame, text="Выбрать изображение", 
                                 command=self.select_file)
        select_button.pack(side=tk.LEFT, padx=5)

        self.file_label = ttk.Label(file_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=10)

        info_frame = ttk.LabelFrame(main_frame, text="Информация об изображении", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.info_text = tk.Text(info_frame, height=15, width=80, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)

        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        rename_frame = ttk.LabelFrame(main_frame, text="Переименование файла", padding="10")
        rename_frame.pack(fill=tk.X, pady=5)

        ttk.Label(rename_frame, text="Новое имя файла:").pack(side=tk.LEFT, padx=5)

        self.name_entry = ttk.Entry(rename_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        self.rename_button = ttk.Button(rename_frame, text="Переименовать", 
                                      command=self.rename_file, state=tk.DISABLED)
        self.rename_button.pack(side=tk.LEFT, padx=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("Все файлы", "*.*")
            ]
        )

        if file_path:
            self.load_image_info(file_path)

    def load_image_info(self, file_path):
        if not self.image_info.is_valid_image(file_path):
            messagebox.showerror("Ошибка", "Выбранный файл не является изображением!")
            return

        try:
            info = self.image_info.get_image_info(file_path)

            if info:
                self.current_file = file_path
                self.file_label.config(text=os.path.basename(file_path))
                self.display_image_info(info)

                base_name = os.path.splitext(os.path.basename(file_path))[0]
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, base_name)
                self.rename_button.config(state=tk.NORMAL)

            else:
                messagebox.showerror("Ошибка", "Не удалось получить информацию")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке:\n{str(e)}")

    def display_image_info(self, info):
        self.info_text.delete(1.0, tk.END)

        text = f"""
ИНФОРМАЦИЯ О ФАЙЛЕ

Файл: {info['file_name']}
Папка: {info['directory']}

РАЗРЕШЕНИЕ:
   Ширина: {info['resolution']['width']} px
   Высота: {info['resolution']['height']} px
   Размер: {info['resolution']['text']}

РАЗМЕР ФАЙЛА:
   Байты: {info['file_size']['bytes']} B
   Килобайты: {info['file_size']['kb']} KB
   Мегабайты: {info['file_size']['mb']} MB

ХАРАКТЕРИСТИКИ:
   Формат: {info['format']}
   Цветовая модель: {info['color_mode']}

ДАТА СОЗДАНИЯ: {info['creation_date']}
"""
        self.info_text.insert(1.0, text)

    def rename_file(self):
        if not self.current_file:
            messagebox.showwarning("Ошибка", "Выберите файл!")
            return

        new_name = self.name_entry.get().strip()

        if not new_name:
            messagebox.showwarning("Ошибка", "Введите имя файла!")
            return

        success, message = self.file_renamer.rename_file(self.current_file, new_name)

        if success:
            messagebox.showinfo("Успех", message)
            self.update_after_rename()
        else:
            messagebox.showerror("Ошибка", message)

    def update_after_rename(self):
        if not self.current_file:
            return

        new_name = self.name_entry.get().strip()
        if not new_name:
            return

        directory = os.path.dirname(self.current_file)
        extension = self.file_renamer.get_file_extension(self.current_file)
        new_file_path = os.path.join(directory, new_name + extension)
        self.current_file = new_file_path
        self.load_image_info(new_file_path)

    def run(self):
        self.root.mainloop()