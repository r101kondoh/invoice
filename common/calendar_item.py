from typing import Generic
import flet as ft
from common.my_datepiker import DateUtils
from db.setting import T
from utils.date_utils import STR_WEEK_LIST
from utils.error_handlers import handle_errors

class CalendarItem(ft.Container):
    """
    カレンダーグリッドに表示する日付セル
    """
    @handle_errors
    def __init__(self, day:int|str, index:int):
        super().__init__()
        self.stack = ft.Ref[ft.Stack]()
        self.drag_target_area = ft.Ref[ft.DragTarget]()

        # 表記する日付
        self.day = str(day) if day != 0 else "-"

        # セルのインデックス
        self.index:int = index
        
        # 当該日付セルが日曜日かどうか
        self.is_sunday = index % len(STR_WEEK_LIST) == 0

        # 背景色
        if day == 0:
            self.bgcolor = ft.Colors.GREY
        else:
            self.bgcolor = ft.Colors.WHITE

        self.text_color = ft.Colors.GREY_600
        self.padding = ft.padding.all(5)
        self.border = ft.border.all(0.1)
        self.border_radius = ft.border_radius.all(10)
        self.alignment = ft.alignment.center
        self.content = ft.Stack(
            ref=self.stack,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # 日付ラベル
                        ft.Text(
                            self.day,
                            color=self.text_color,
                            weight=ft.FontWeight.W_700, size=8, 
                            text_align=ft.TextAlign.LEFT,
                            width=50
                        ),
                        ft.DragTarget(
                            group="group",
                            visible=False,
                            ref=self.drag_target_area,
                            content=ft.Container(
                                content=None,
                                border=ft.border.all(0.1),
                                border_radius=ft.border_radius.all(50),
                                padding=ft.padding.all(8),
                                bgcolor=ft.Colors.GREY_100
                            ),
                            on_leave=lambda _: self.upd_status(),
                            on_move=lambda _ : self.upd_drag_target_bgcolor(bgcolor=ft.Colors.YELLOW),
                            on_will_accept=lambda _ : self.upd_drag_target_bgcolor(bgcolor=ft.Colors.YELLOW),
                            on_accept= lambda _ : self.upd_status()
                        )
                    ],
                    spacing=1
                )
            ]
        )

    def upd_status(self):
        '''
        ステータス更新関数
        '''
        pass

    def upd_drag_target_bgcolor(self, bgcolor:str):
        '''
        ドラッグ受け入れ領域の背景色更新処理
        '''
        container:ft.Container = self.drag_target_area.current.content
        container.bgcolor = bgcolor
        self.drag_target_area.current.update()


