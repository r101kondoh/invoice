from typing import Dict
import flet as ft

from app.invoice.logic.invoice_logic import InvoiceLogic
from app.invoice.logic.scraper.sales_sheet_scraper import SalesSheetScraper
from common.my_datepiker import MyDatePicker

class InvoiceView(ft.Column):
    """
    売上表出力画面
    """
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.alignment =ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.invoice_logic = InvoiceLogic(page=page)
        self.controls = [
            MyDatePicker(ref=self.invoice_logic.yearmonth_picker, upd_conponents=self.did_mount),
            ft.FilledButton(
                "売上表出力",
                ref=self.invoice_logic.btn_generate,
                icon=ft.Icons.DOWNLOAD,
                on_click=lambda _ :self.invoice_logic.launch_scraper(
                    scraper=SalesSheetScraper(page),
                    period=f"{self.invoice_logic.yearmonth_picker.current.year}{self.invoice_logic.yearmonth_picker.current.month:02}"
                )
            ),
            ft.FilledButton(
                "売上表シート加工",
                ref=self.invoice_logic.btn_separete,
                icon=ft.Icons.TABLE_BAR,
                on_click=lambda _ :self.invoice_logic.launch_writer(
                    # scraper=SalesSheetScraper(page),
                    period=f"{self.invoice_logic.yearmonth_picker.current.year}{self.invoice_logic.yearmonth_picker.current.month:02}"
                )
            )
        ]

    def did_mount(self):
        str_year = f"{self.invoice_logic.yearmonth_picker.current.year}"
        str_month = f"{self.invoice_logic.yearmonth_picker.current.month:02}"
        self.invoice_logic.upd_btns(period=f"{str_year}{str_month}")
    #     self.invoice_logic.upd_btns(period=f"{self.invoice_logic.yearmonth_picker.current.year}{self.invoice_logic.yearmonth_picker.current.month:02}")