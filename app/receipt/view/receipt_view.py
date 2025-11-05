import flet as ft

from app.receipt.logic.receipt_logic import ReceiptLogic
from common.my_datepiker import MyDatePicker

class ReceiptView(ft.Column):
    """
    レシート画像抽出操作画面
    """
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.alignment =ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.receipt_logic = ReceiptLogic(page=page)

        self.controls = [
            MyDatePicker(ref=self.receipt_logic.yearmonth_picker, upd_conponents=self.receipt_logic.fetch_images),
            ft.Row(
                controls=[        
                    ft.FilledButton(
                        "レシート画像抽出",
                        icon=ft.Icons.IMAGE,
                        on_click=lambda _: self.receipt_logic.extract_receipt_img()
                    ),
                    ft.FilledButton(
                        "レシート画像登録",
                        icon=ft.Icons.APP_REGISTRATION,
                        on_click=lambda _: self.receipt_logic.scraper.execute_automation(year=self.receipt_logic.yearmonth_picker.current.year, month=self.receipt_logic.yearmonth_picker.current.month)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS, ref=self.receipt_logic.row_images),
            ft.Text("ファイル名は、「日付_客数_金額(税抜計).png」の形式で名前変更してください")
        ]

    def did_mount(self):
        self.receipt_logic.fetch_images()