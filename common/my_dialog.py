import flet as ft
from utils.error_handlers import handle_errors

class MyDialog(ft.AlertDialog):
    """
    ダイアログ
    """
    def __init__(self, page:ft.Page, title:str|None=None):
        super().__init__()
        self.page = page
        self.title = ft.Text(title, text_align=ft.TextAlign.CENTER) if  title is not None else None
        self.actions_alignment=ft.MainAxisAlignment.END
        self.modal = True

    @handle_errors
    def open_dialog(self):
        '''
        ダイアログを開く
        '''
        self.page.open(self)

    @handle_errors
    def close_dialog(self):
        '''
        ダイアログを閉じる
        '''
        self.page.close(self)

    @handle_errors
    def set_title(self, title:str):
        '''
        タイトルを設定
        '''
        self.title = ft.Text(title, text_align=ft.TextAlign.CENTER)
        self.update()