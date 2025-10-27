from typing import List
from utils.constants import *
# from app.invoice.logic.writer.detail_writer import DetailWriter
# from app.invoice.logic.writer.invoice_writer import InvoiceWriter
from utils.date_utils import DateUtils
from utils.df_utils import DataFrameUtils
from utils.error_handlers import handle_errors
from utils.excel_utils import ExcelUtils
from utils.file_utils import FileUtils
from utils.html_tbl_to_excel import BaseHTMLDataToExcelConverter
from logging import getLogger
my_logger = getLogger()

class DepositSheetConverter(BaseHTMLDataToExcelConverter):
    """
    通帳入金一覧表テーブルのhtmlをエクセルに整形するクラス
    """
    def __init__(self, data_source:List[str]):
        super().__init__(data_source)
        # self.excel_writer = ExcelUtils(path=FileUtils.get_invoice_templaet_excel_path())
        self.output_path:str = ""

    @handle_errors
    def convert_to_excel(self, period:str):

        # 出力パス設定
        self.set_output_path(period)

        # 売上表から取得したデータをエクセルに保存
        df = DataFrameUtils(
            self.data_source,
            columns=["店舗番号", '店舗名', "通帳入金年月日", "入金額"]
        )
        df.save_to_excel(f"{self.output_path}/通帳入金_{period}.xlsx")

        # # TODO: 詳細の給与体系請求の行数もデータベースから取得できるようにする
        # invoice_writer = InvoiceWriter(excel_writer=self.excel_writer, period=period, df=df)
        # detail_writer = DetailWriter(excel_writer=self.excel_writer, period=period, df=df)

        # # 請求書の日付情報を出力
        # invoice_writer.set_date_info()

        # # 請求書の行を追加・削除
        # invoice_writer.add_standard_data_row()
        # invoice_writer.del_standard_data_row()

        # # 請求書の行に値を書き込む
        # invoice_writer.set_standard_data_row()

        # # 請求明細の日付情報を出力
        # detail_writer.set_date_info()

        # # 請求明細の行を追加・削除
        # detail_writer.add_standard_data_row()
        # detail_writer.del_standard_data_row()

        # # 請求明細の行に値を書き込む
        # detail_writer.set_standard_data_row()

        # # 請求書明細書の出力
        # self.excel_writer.save_wb(f"{self.output_path}/請求書明細書_{period}.xlsx")

    def set_output_path(self, period:str):
        '''
        出力パスを設定
        '''
        str_year, str_month = DateUtils.split_period_to_str_yearmonth(period)
        self.output_path = FileUtils.get_yearmonth_dir(str_year, str_month, '請求書明細書')
        # self.excel_writer.set_sheet_title(f"{str_year[2:]}.{int(str_month)}請求書,明細書")