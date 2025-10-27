from typing import Generic, List
import flet as ft
from common.my_datepiker import DateUtils
from db.setting import T
from utils.date_utils import STR_WEEK_LIST
from utils.error_handlers import handle_errors

class CalendarGrid(ft.GridView):
    """
    カレンダーのグリッド
    """
    # XXX: CalendarGridViewへの関数の渡し方
    @handle_errors
    def __init__(self, ref:ft.Ref["CalendarGrid"], item_width:int = 60):
        super().__init__(ref=ref)
        self.item_width = item_width
        self.width = self.item_width * 7
        self.max_extent = self.item_width
        self.child_aspect_ratio = 1.0
        self.spacing = 1
        self.run_spacing = 1

    @handle_errors
    def update(self, calendar_items:List[ft.Container]):
        '''
        カレンダーの更新
        '''
        # days_list = DateUtils.generete_calendar_days(year, month)

        # 曜日ヘッダーを追加
        self.controls = [CalendarHeaderItem(weekday) for weekday in STR_WEEK_LIST]
        
        
        # 日付セルを追加
        self.controls.extend(calendar_items)
        # self.controls.extend([
        #     CalendarItem(
        #         day=day, index=index,
        #         attendance_logic=self.attendance_logic,
        #         data=None if day == 0 else next((record for record in records), None)
        #     ) 
        #     for index, day in enumerate(days_list)
        # ])
        super().update()

class CalendarHeaderItem(ft.Container):
    """
    曜日ヘッダーセル
    """
    def __init__(self, weekday:str):
        super().__init__()
        # self.bgcolor =  ft.Colors.WHITE
        if weekday == "日":
            self.text_color = ft.Colors.RED
        elif weekday == "土":
            self.text_color = ft.Colors.BLUE
        else:
            self.text_color = ft.Colors.BLACK
        # self.padding = ft.padding.all(5)
        # self.border = ft.border.all(0.1)
        self.border_radius = ft.border_radius.all(10)
        self.alignment = ft.alignment.center
        self.content = ft.Text(weekday, color=self.text_color, size=16)