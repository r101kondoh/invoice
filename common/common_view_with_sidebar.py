from typing import List
import flet as ft
from common.abstract_common_view import AbstractCommonView
from common.app import App


class CommonViewWithSideBar(AbstractCommonView):
    """
    共通画面（サイドバーver）
    """
    def __init__(self, page:ft.Page, app_list:List[App]):
        super().__init__(page=page, app_list=app_list)

        self.side_menu = ft.NavigationRail(
            selected_index=0,
            on_change=lambda e: page.go(self.app_list[e.control.selected_index].url),
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=[]
        )

        # サイドメニューの項目をセット
        self.init_side_menu()

    def init_side_menu(self):
        '''
        サイドメニューの項目をセット
        '''
        self.side_menu.destinations = [
            ft.NavigationRailDestination(
                label=app.title,
                icon=app.icon,
                selected_icon=app.icon_outlined
            )
            for app in self.app_list if not app.hidden_flg
        ]

    def create_view(self, app:App):
        '''
        共通レイアウトにアプリを配置
        '''
        view = ft.View(
            route=app.url,
            controls=[
                ft.Row(
                    [
                        self.side_menu,
                        ft.VerticalDivider(width=1),
                        ft.Column(
                            [app.app],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True
                        )
                    ],
                    expand=True
                )
            ]
        )
        return view