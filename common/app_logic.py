import flet as ft
from typing import Dict
from db.base import BaseRepository
from utils.error_handlers import handle_errors


class AppLogic():
    """
    アプリロジック
    """
    @handle_errors
    def __init__(self, page:ft.Page, repos:Dict[str, BaseRepository]):
        self.page = page