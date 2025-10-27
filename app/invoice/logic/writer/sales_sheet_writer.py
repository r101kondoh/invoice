import pandas as pd
from logging import getLogger
import flet as ft
from common.my_msgbox import MyMsgBox
from common.my_progress import ProgressOverlay
from utils.date_utils import DateUtils
from utils.file_utils import FileUtils
my_logger = getLogger()

class SalesSheetWriter():
    """
    売上表の書き込みを行うクラス
    """
    def __init__(self, page:ft.Page, period:str):
        self.path = "" 
        self.set_output_path(period)
        self.sales_df = pd.read_excel(f"{self.path}/売上表_{period}.xlsx")
        self.shop_df = pd.read_excel("./assets/店舗一覧.xlsx")
        self.output_file_name = f"{self.path}/店舗種別別売上表_{period}.xlsx"
        self.overlay = ProgressOverlay(page=page)

    def separete_to_shop_type(self):
        '''
        店舗種別ごとにシートを分離
        '''
        try:
            my_logger.info(f"出力スタート")

            self.overlay.message_reciever().send("店舗別売上表出力中...")
            self.sales_df["店舗番号"].astype(int).astype(str).str.zfill(4)
            df_merged = pd.merge(
                self.sales_df,
                self.shop_df[["ID", "店舗種別"]],
                left_on="店舗番号",
                right_on="ID",
                how="left"
            )
            my_logger.info(f"出力ファイル：{self.output_file_name}")
            with pd.ExcelWriter(self.output_file_name, engine="openpyxl") as writer:
                for shop_type, group in df_merged.groupby("店舗種別"):
                    # 店舗種別ごとにシートを作成
                    sheet_name = str(shop_type)[:31]  # Excelシート名は31文字制限あり
                    group.drop(columns=["ID"], inplace=True)  # ID列は不要なら削除
                    group.to_excel(writer, sheet_name=sheet_name, index=False)
                    self.overlay.message_reciever().send("店舗別売上表出力完了")
                MyMsgBox.show_msgbox(title=f"店舗別売上表出力完了", msg=f"店舗別売上表出力を完了しました")
        except Exception as err:
            # self.overlay.message_reciever().send(title="店舗別売上表出力失敗", msg=f"店舗別売上表出力に失敗しました")
            MyMsgBox.show_errmsgbox(
                f"{type(err).__name__}", 
                f"店舗別売上表出力に失敗しました"
            )
            raise err
        finally:
            self.overlay.dismiss_progress()

    def set_output_path(self, period:str):
        '''
        入力パスを取得
        '''
        str_year, str_month = DateUtils.split_period_to_str_yearmonth(period)
        self.path = FileUtils.get_yearmonth_dir(str_year, str_month, '請求書明細書')
