from typing import List
import flet as ft
from abc import ABC, abstractmethod
from common.app import App
from logging import getLogger
my_logger = getLogger()

class AbstractCommonView(ABC):
    """
    共通画面
    """
    def __init__(self, page:ft.Page, app_list:List[App]):
        self.page = page
        self.app_list = app_list

    @abstractmethod
    def init_side_menu(self):
        '''
        サイドメニューの項目をセット
        '''
        pass

    # def route_change(self, handler):
    #     '''
    #     画面遷移処理
    #     '''
    #     troute = ft.TemplateRoute(handler.route)
    #     self.page.views.clear()
    #     for app in self.app_list:
    #         if troute.match(app.url):
    #             self.page.views.append(self.create_view(app))
    #             break
    #         self.page.update()

    @abstractmethod
    def create_view(self, app:App):
        '''
        共通レイアウトにアプリを配置し返す
        '''
        pass

    def route_change(self, handler):
        '''
        画面遷移処理
        '''
        troute = ft.TemplateRoute(handler.route)
        self.page.views.clear()
        for app in self.app_list:
            if troute.match(app.url):
                # 置換前のURLを保持
                origin_url = app.url
                if ":id" in app.url: # クエリキーワオドの置換
                    app.url = app.url.replace(":id", troute.id)
                self.page.views.append(self.create_view(app))
                
                # アプリに設定されているurlを置換前のURLに戻す
                app.url = origin_url
                break
        self.page.update()