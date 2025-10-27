from abc import ABC, abstractmethod
from typing import Dict, List, Optional, final
import flet as ft

from common.app_state import AppState

# NOTE: ObserverパターンのObserverに相
# 状態の変更に反応する側
class AppView(ft.Column):
    """
    アプリ画面
    """
    def __init__(self, page:ft.Page, states:Optional[List[AppState]]):
        if states is not None:
            for state in states:
                # 状態と画面の紐づけ
                state.bind(self)
        self.page = page
        super().__init__(horizontal_alignment = ft.CrossAxisAlignment.CENTER)

    @final
    def update(self, state:Optional[AppState] = None):
        '''
        状態の変更通知をUIに反映する
        '''
        if state is not None:
            self.apply_state()
        super().update()

    @abstractmethod
    def apply_state():
        '''
        描画処理
        '''
        pass
        

