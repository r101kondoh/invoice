from typing import Callable
import flet as ft
from utils.date_utils import DateUtils

class MyDatePicker(ft.Row):
    """
    年月選択
    """
    # XXX: MyDatePickerへのコンポーネント更新処理を渡し方
    def __init__(self, ref:ft.Ref, upd_conponents:Callable[[], None]|None=None):
        super().__init__(ref=ref)
        self.upd_components:Callable[[], None]|None = upd_conponents
        self.lbl_date = ft.Ref[ft.Text]()
        self.btn_next = ft.Ref[ft.IconButton]()
        self.btn_prev = ft.Ref[ft.IconButton]()
        self.year, self.month = DateUtils.todays_yearmonth()
        self.max_year = self.year
        self.min_year = self.year -1
        self.current_month = self.month
        self.controls = [
            ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, ref=self.btn_prev, on_click=lambda _ : self.upd_yearmonth(delta_month=-1)),
            # 日付ラベル
            ft.Text(ref=self.lbl_date, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.IconButton(ft.Icons.ARROW_FORWARD_ROUNDED, ref=self.btn_next, on_click=lambda _ :self.upd_yearmonth(delta_month=1))
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 50
        
    def upd_yearmonth(self, delta_month:int|None=None):
        '''
        日付ラベルと前月翌月ボタンの活性・非活性更新
        '''
        if delta_month is not None:
            self.month += delta_month
            if self.month > 12:
                self.month = 1
                self.year += 1
            if self.month < 1:
                self.month = 12
                self.year -=1
        self.btn_next.current.disabled = self.year == self.max_year and self.month == self.current_month
        self.btn_prev.current.disabled = self.year == self.min_year and self.month == 1
        self.lbl_date.current.value = f"{self.year}年{self.month}月"
        self.btn_next.current.update()
        self.btn_prev.current.update()
        self.lbl_date.current.update()
        if self.upd_components is not None:
            self.upd_components()
        
    def did_mount(self):
        self.upd_yearmonth()
