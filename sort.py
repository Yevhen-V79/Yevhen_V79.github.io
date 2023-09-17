import sys
import shutil
from pathlib import Path
from unidecode import unidecode

def normalize(name: str) -> str:
    # Транслітеруємо кирилічні символи на латиницю за допомогою unidecode
    latin_name = unidecode(name)
    # Замінюємо всі символи, крім літер латинського алфавіту та цифр, на "_"
    normalized_name = ''.join([c if c.isalnum() or c == '.' or c == ' ' or c == '_' else '_' for c in latin_name])

    return normalized_name

CATEGORIES = {
    "audio": [".mp3", ".waw", ".flac", ".wma"],
    "documents": [".docx", ".txt", ".doc", ".pdf", ".xlsx", ".pptx"],
    "video": [".avi", ".mov", ".mp4", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"]
}

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)  # Створюємо папку, якщо її не існує
    
    new_path = target_dir.joinpath(file.name)
    
    if not new_path.exists():
        file.replace(new_path)  # Переміщуємо файл

def sort_folder(path: Path, print_folders=False) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
            print(element)
        elif element.is_dir() and not any(element.glob("*")):
            element.rmdir()  # Видаляємо порожні папки
        elif print_folders:
            print(element)  # Друкуємо імена папок, якщо встановлено параметр print_folders

def unpack(path: Path) -> None:
    archives_dir = path.joinpath("archives")
    
    for element in archives_dir.glob("*"):
        if element.is_file() and (element.suffix == ".zip" or element.suffix == ".gz" or element.suffix == ".tar"):
            # Отримуємо назву архіву без розширення
            archive_name = element.stem
            # Створюємо папку з назвою архіву без розширення у папці "archives"
            archive_folder = archives_dir.joinpath(archive_name)
            archive_folder.mkdir(parents=True, exist_ok=True)
            # Розпаковуємо архів у нову папку
            shutil.unpack_archive(str(element), str(archive_folder))
            print(element)

def main() -> str:
    try:
        path_str = sys.argv[1]
        path = Path(path_str)  # Convert the input string to a Path object
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder does not exist"

    sort_folder(path, print_folders=True)  # Включаємо роздрукування імен папок та файлів
    return "All ok"

if __name__ == '__main__':
    print(main())

    sort_folder(Path(sys.argv[1]), print_folders=True)





