import os

cwd = os.getcwd()
print(f"Текущая рабочая директория: {cwd}")

import os

# Получить абсолютный путь к текущему файлу
current_file_path = os.path.abspath(__file__)
# Получить директорию, в которой лежит файл
current_dir = os.path.dirname(current_file_path)

print(f"Файл лежит в: {current_dir}")
