import flet as ft

class MySnackBar(ft.SnackBar):
    """
    スナックバー
    """
    def __init__(self, msg:str, is_err:bool = False):
        super().__init__(
            content = ft.Row([
                ft.Icon(ft.Icons.ERROR if is_err else ft.Icons.CHECK, color=ft.Colors.WHITE),
                ft.Text(msg, color=ft.Colors.WHITE)
            ]),
            bgcolor= ft.Colors.RED if is_err else ft.Colors.GREEN
        )