import shutil
from pathlib import Path


def move_to_parent_dir(path):
    parent = Path(path)

    for file in parent.rglob("*.xlsx"):
        if file.parent != parent:  # 親フォルダにあるファイルは除外
            shutil.copy(file, parent / file.name)

if __name__ == "__main__": 
    move_to_parent_dir(r"C:\Users\hisas\Documents\Python\automation\output\請求書明細書\2025")
