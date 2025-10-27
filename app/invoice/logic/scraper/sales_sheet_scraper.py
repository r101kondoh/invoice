import os
from typing import Dict, List, Tuple
import flet as ft
from app.invoice.logic.converter.deposit_sheet_converter import DepositSheetConverter
from app.invoice.logic.converter.sales_sheet_converter import SalesSheetConverter
from utils.df_utils import DataFrameUtils
from utils.excel_utils import ExcelUtils
from utils.pos_scraper import PosScraper
import pandas as pd
# from app.invoice.logic.converter.sales_sheet_converter import SalesSheetConverter
# from db.base import BaseRepository, QueryBuilder
# from db.shop import InvoiceType, Shop, ShopRepository
from utils.date_utils import DateUtils
from utils.error_handlers import handle_errors
from logging import getLogger

from utils.file_utils import FileUtils
my_logger = getLogger()

class SalesSheetScraper(PosScraper):
    """
    売上表自動取得クラス
    """
    @handle_errors
    def __init__(self, page:ft.Page):
        
        # 店舗モデルのCRUD処理を行うリポジトリ
        # self.shop_repo:ShopRepository = repos[Shop.__tablename__]
        # self.records:List[Shop] = self.shop_repo.get_by_output_types(output_types=[InvoiceType.RATE.value, InvoiceType.SALARY.value])

        # shop_sheet = ExcelUtils(path=FileUtils.get_shop_list_excel_path())
        
        # shop_df = DataFrameUtils(
        #     [],
        #     columns=["ID", '店舗名', "店舗種別", "税込/税抜"]
        # )
        # self.records = shop_df.read_exel(path=FileUtils.get_shop_list_excel_path())

        self.df = pd.read_excel("./assets/店舗一覧.xlsx")
        super().__init__(
            page=page, 
            target_name="売上表", 
            target_url=os.environ.get("POS_SALES_SHEET_URL"),
            target_shop_codes=[row["ID"] for _, row in self.df.iterrows()]
        )
        self.summary = []
        self.deposit_list = []

    def execute_automation(self, periods:Tuple[str, ...]):
        '''
        売上表取得自動処理を実行
        '''
        # NOTE: 親クラスの自動処理のエラーハンドリングデコレータでラップ
        @self.handle_automation_error(msg="売上表取得")
        def execute_process():
            '''
            売上表取得自動処理
            '''
            period = periods[0] # NOTE: 指定する期間は１種類
            self.overlay.message_reciever().send("Chromeを起動中...")
            self.launch_webdriver()
            self.login()
            for shop_code in self.target_shop_codes:
                self.redirect(self.target_url)
                self.fetch_sales_sheet_by_year_month(period, shop_code)
                self.capture_result(period, shop_code)
            self.table_html_to_excel(period)
            self.overlay.message_reciever().send("請求書・明細書エクセルファイル出力完了")
        return execute_process()

    @handle_errors
    def fetch_sales_sheet_by_year_month(self, period:str, target_shop_code:str):
        '''
        指定した年月の売上表を出力
        '''
        target_shop_name =  [row["店舗名"] for _, row in self.df.iterrows() if row["ID"] == target_shop_code][0]
        self.overlay.message_reciever().send(f"「{target_shop_code}_{target_shop_name}」の売上表のデータ取得条件入力中...\n(処理店舗数残り {len(self.target_shop_codes)-self.target_shop_codes.index(target_shop_code)}件)")
        # 店舗コードの入力
        txt_start_shop_code = self.get_elem('Form1Main_txtMiseCode')
        txt_end_shop_code = self.get_elem("Form1Main_txtSyuryoMiseCode")        
        @self.retry_execution()
        def input_shop_code(shop_code):
            self.input_elem(txt_start_shop_code, shop_code)
            self.input_elem(txt_end_shop_code, shop_code)
        input_shop_code(shop_code=target_shop_code)
        
        # 年月日の入力
        txt_start_date = self.get_elem('Form1Main_txtNengetu')
        txt_end_date = self.get_elem('Form1Main_txtSyuryoNengetu')
        @self.retry_execution()
        def input_date(yearmonth:str):
            self.input_elem(txt_start_date, yearmonth)
            self.input_elem(txt_end_date, yearmonth)
        input_date(period)

        # 出力ボタン押下
        btn_generate = self.get_elem('Form1Main_btnF2_UPD')
        self.click_elem(btn_generate)

        deposits =  self.wait_for_all_elements_visible_by_name("通帳入金額1")

        # 各店舗の通帳入金額を入れる
        for index, deposit in enumerate(deposits):
            if deposit.text != "0":
                year = int(period[0:4])
                month = int(period[4:6])
                self.deposit_list.append([target_shop_code, target_shop_name, f"{year}年{month}月{index+1}日", int(deposit.text.replace(",", ""))])

        # 出力されたテーブルから、現金売上、クレジット売上、金券・他の売上、商業施設掛、ショップ掛、合計のデータを取得
        # TODO: 調整金の値の取得（金券他の値から調整金の値を引かなければならない）
        cash_amount = int(self.wait_for_all_elements_visible_by_name("現金2")[-1].text.replace(",", ""))
        credit_amount = int(self.wait_for_all_elements_visible_by_name("クレジット2")[-1].text.replace(",", ""))
        coupon_amount = int(self.wait_for_all_elements_visible_by_name("金券他2")[-1].text.replace(",", ""))
        coupon_adjust = int(self.wait_for_all_elements_visible_by_name("金券他3")[-1].text.replace(",", "")) # 調整金
        # coupon_amount -= coupon_adjust
        com_facility_amount = int(self.wait_for_all_elements_visible_by_name("商業施設掛2")[-1].text.replace(",", ""))
        shop_amount = int(self.wait_for_all_elements_visible_by_name("ショップ掛2")[-1].text.replace(",", ""))
        total = int(self.wait_for_all_elements_visible_by_name("本日計2")[-1].text.replace(",", ""))
        deposit_total = int(self.wait_for_all_elements_visible_by_name("通帳入金額2")[-1].text.replace(",", ""))
        deposit_adjust = int(self.wait_for_all_elements_visible_by_name("通帳入金額3")[-1].text.replace(",", ""))
        # target_shop = [record for record in self.records if record.id == target_shop_code][0]
        # self.summary.append([target_shop_code, target_shop.name, cash_amount, credit_amount, coupon_amount, com_facility_amount, shop_amount, total, target_shop.output_type, target_shop.rate])
        self.summary.append([target_shop_code, target_shop_name, cash_amount, credit_amount, coupon_amount, com_facility_amount, shop_amount, total, deposit_total, deposit_adjust])
    
    @handle_errors
    def table_html_to_excel(self, period:str):
        '''
        売上表をエクセルに出力
        '''
        # テーブル出力まで待機
        # self.overlay.message_reciever().send(f"売上表データ取得中...")

        # # 集計データを格納するリスト

        # TODO: 店舗別に
        excel_generator  = SalesSheetConverter(data_source=self.summary)

        # self.overlay.message_reciever().send("請求書・明細書エクセルファイル出力中...")
        excel_generator.convert_to_excel(period)

        deposit_generator = DepositSheetConverter(data_source=self.deposit_list)
        deposit_generator.convert_to_excel(period)
    
    @handle_errors
    def capture_result(self, period:str, shop_code:str):
        '''
        売上表の取得結果のスクリーンショットを撮る
        '''
        str_year, str_month = DateUtils.split_period_to_str_yearmonth(period)
        output_path = FileUtils.get_yearmonth_dir(str_year, str_month, '請求書明細書')
        file_name = f"{shop_code:04}_{[row['店舗名'] for _, row in self.df.iterrows() if row['ID'] == shop_code][0]}_{period}.png"
        # file_name = f"0007_薬院_{period}.png"
        self.scroll_to_bottom_right()
        self.capture_window(f"{output_path}/{file_name}")
            