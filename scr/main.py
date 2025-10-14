import sys
import os

def main():
    print("Запуск анализатора изображений...")

    try:
        from main_window import MainWindow
        app = MainWindow()
        app.run()

    except Exception as e:
        print(f"Ошибка при запуске программы: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

main()