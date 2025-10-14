import os
import shutil

class FileRenamer:
    def rename_file(self, old_path, new_name):
        if not os.path.exists(old_path):
            return False, "Файл не найден"

        try:
            directory = os.path.dirname(old_path)
            file_extension = os.path.splitext(old_path)[1]
            new_path = os.path.join(directory, new_name + file_extension)

            if os.path.exists(new_path):
                return False, "Файл с таким именем уже существует"

            os.rename(old_path, new_path)
            return True, "Файл успешно переименован"

        except Exception as e:
            error_message = f"Ошибка при переименовании: {str(e)}"
            return False, error_message

    def get_file_extension(self, file_path):
        return os.path.splitext(file_path)[1]

    def get_safe_filename(self, directory, base_name, extension):
        counter = 1
        current_name = base_name

        while True:
            possible_path = os.path.join(directory, current_name + extension)
            if not os.path.exists(possible_path):
                return current_name
            current_name = f"{base_name}_{counter}"
            counter += 1