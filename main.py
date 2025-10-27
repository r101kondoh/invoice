import flet as ft

from app.invoice.view.invoice_view import InvoiceView
from app.receipt.view.receipt_view import ReceiptView
from common.app import App
from common.common_view_with_sidebar import CommonViewWithSideBar
from dotenv import load_dotenv
load_dotenv()
from utils.my_logger import set_logger
set_logger()

def main(page: ft.Page):
    '''
    エントリーポイント
    '''
    page.title = "社内業務アプリ"
    page.window.width = 700
    page.window.height = 640
    page.window.min_width = 700
    page.window.min_height = 640
    page.window.max_width = 700
    page.window.max_height = 640

    app_list = [
        App(
            app=ReceiptView(page=page),
            url="/receipt", title="レシート画像出力",
            icon=ft.Icons.RECEIPT,
            icon_outlined=ft.Icons.RECEIPT_OUTLINED,
        ),
        App(
            app=InvoiceView(page=page),
            url="/invoice", title="売上表出力",
            icon=ft.Icons.DOWNLOAD,
            icon_outlined=ft.Icons.MANAGE_ACCOUNTS_OUTLINED,
        ),
    ]

    # サポート言語を日本語と英語で、初期値を日本語に設定する
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("ja", "JP"), ft.Locale("en", "US")], current_locale=ft.Locale("ja", "JP")
        )
    
    # 共通画面
    common_view = CommonViewWithSideBar(page=page, app_list=app_list)

    # 画面遷移処理設定
    page.on_route_change = common_view.route_change

    # 画面の要素の並べ方の設定
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # 初期ページに繊維
    page.go(common_view.app_list[0].url)
    
ft.app(target=main)