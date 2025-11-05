import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":[
        "tkinter",
        "numpy",
        "openpyxl",
        "pandas",
        "selenium",
        "dotenv",
        "flet",
        "sqlite3",
        "sqlalchemy",
        "PIL",
        "cv2",
        "bs4",
        "win32com",
        "pymupdf"
    ],
    "include_files":{
        "./.env",
        "./assets",
    }
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="MyApp",
    version="1.0",
    description="Descripotion of my app",
    options={
        "build_exe":build_exe_options
    },
    executables=[
        Executable("main.py", base=base)
    ]
)