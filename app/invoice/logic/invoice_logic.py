import flet as ft
from app.invoice.logic.writer.sales_sheet_writer import SalesSheetWriter
from common.my_datepiker import MyDatePicker
from utils.date_utils import DateUtils
from utils.error_handlers import handle_errors
from utils.file_utils import FileUtils
from utils.pos_scraper import PosScraper
from logging import getLogger
my_logger = getLogger()

class InvoiceLogic():
    """
    売上表出力ロジック
    """
    @handle_errors
    def __init__(self, page:ft.Page):
        self.page = page
        self.btn_generate = ft.Ref[ft.FilledButton]()
        self.btn_separete = ft.Ref[ft.FilledButton]()
        self.yearmonth_picker = ft.Ref[MyDatePicker]()
        
    @handle_errors
    def launch_scraper(self, scraper:PosScraper, period:str):
        '''
        自動処理を起動
        ''' 
        try:
            scraper.execute_automation([period])
        except Exception as err:
            raise err
        finally:
            self.upd_btns(period)

    @handle_errors
    def launch_writer(self, period:str):
        '''
        店舗種別別売上表を出力
        '''
        # my_logger.info(f"出力開始:{period}")
        writer = SalesSheetWriter(page=self.page, period=period)
        
        writer.separete_to_shop_type()
        

    @handle_errors
    def upd_btns(self, period:str):
        # TODO: ファイル存在チェック、売上表シート加工ボタンの活性日活性制御
        # pass
        str_year, str_month = DateUtils.split_period_to_str_yearmonth(period)
        output_path = FileUtils.get_yearmonth_dir(str_year, str_month, '請求書明細書')
        is_file_exists = FileUtils.check_file_exists(f"{output_path}/売上表_{period}.xlsx")
        self.btn_separete.current.disabled = not is_file_exists
        self.btn_separete.current.update()