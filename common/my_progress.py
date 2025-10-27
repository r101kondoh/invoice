from functools import wraps
import flet as ft

class ProgressOverlay:
    """
    処理中に表示するオーバーレイ
    """
    def __init__(self, page:ft.Page):
        self.page = page
        self.overlay_lbl = ft.Ref[ft.Text]()

        # NOTE* オーバーレイ表示のため、ダイアログは透明にする
        self.dlg = ft.AlertDialog(
            bgcolor=ft.Colors.TRANSPARENT,
            title_padding=0,
            content_padding=0,
            inset_padding=0,
            actions_padding=0,
            open=False,
            content=ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        # プログレスバー
                        ft.Row(
                            [ft.ProgressBar(width=self.page.width)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.MainAxisAlignment.CENTER
                        ),
                        # 表示ラベル
                        ft.Row(
                            [
                                ft.Text(
                                    "",
                                    ref=self.overlay_lbl, 
                                    color=ft.Colors.WHITE, 
                                    text_align=ft.TextAlign.CENTER
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    width=self.page.width,
                    height=self.page.height
                )
            )
        )

    def show_progress(self):
        '''
        オーバーレイを表示
        '''
        self.page.overlay.clear()
        self.page.overlay.append(self.dlg)
        self.dlg.open = True
        self.page.update()

    def dismiss_progress(self):
        '''
        オーバーレイを閉じる
        '''
        self.dlg.open = False
        self.page.update()

    def auto_start_coroutine(self, func):
        '''
        コルーチンを自動的に初期化するデコレータ
        '''
        @wraps(func)
        def primer(*args, **kwargs): 
            coroutine = func(*args, *kwargs) # コルーチン生成
            next(coroutine) # NOTE: next()を呼び出し、コルーチンを自動で初期化し開始する
            return coroutine
        return primer
        
    def message_reciever(self):
        '''
        オーバーレイに表示するメッセージを受け取るコルーチン
        '''
        @self.auto_start_coroutine
        def recive_overlay_message():
            self.show_progress()
            while True:
                # メッセージを受け取る
                message = yield
                self.overlay_lbl.current.value = message
                self.overlay_lbl.current.update()
        return recive_overlay_message()

    def build(self):
        return