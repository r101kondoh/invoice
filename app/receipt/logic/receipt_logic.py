import flet as ft

from app.receipt.logic.pdf_converter import PDFConverter
from app.receipt.logic.receipt_extracter import ReceiptExtracter
from app.receipt.logic.scraper.sales_data_edit_scraper import SalesDataEditScraper
from app.receipt.view.receipt_img import ReceiptImage
from common.my_datepiker import MyDatePicker
from common.my_msgbox import MyMsgBox
from common.my_progress import ProgressOverlay
from utils.error_handlers import handle_errors
from utils.file_utils import FileUtils
from logging import getLogger
my_logger = getLogger()

class ReceiptLogic():
    """
    レシート画像抽出操作ロジック
    """
    @handle_errors
    def __init__(self, page:ft.Page):
        self.page = page

        self.yearmonth_picker = ft.Ref[MyDatePicker]()
        self.row_images = ft.Ref[ft.Row]()

        
        # 共有フォルダのパス（UNCパス）
        self.base_dir =r"\\192.168.5.1\scan\近藤" 
        self.src_dir = ""

        # PDF・画像格納フォルダ      
        self.yearmonth_dir = ""
        self.scan_dir = ""
        self.pending_scan_dir = ""
        self.processed_scan_dir = ""
        self.success_dir = ""
        self.failed_dir = ""
        self.pdf_dir = ""

        # PDFの画像変換器
        self.pdf_converter = PDFConverter()

        # レシート画像切り出し器
        self.receipt_extracter = ReceiptExtracter()

        # オーバーレイ
        self.overlay = ProgressOverlay(page=page)

        self.scraper = SalesDataEditScraper(page=page)

    @handle_errors
    def set_img_dir(self):
        '''
        画像パスの変更
        '''
        str_year = self.yearmonth_picker.current.year
        str_month = f"{self.yearmonth_picker.current.month:02}"
        self.dir = FileUtils.get_yearmonth_dir(str_year, str_month, "receipt")
        self.scan_dir = f"{self.dir}/img/scan"
        self.pdf_dir = f"{self.dir}/pdf"
        self.pending_scan_dir = f"{self.dir}/img/scan/pending"
        self.processed_scan_dir = f"{self.dir}/img/scan/processed"
        # pending: 未処理
        # processed: 処理済
        self.success_dir = f"{self.dir}/img/matching/success"
        self.failed_dir = f"{self.dir}/img/matching/failed"
        self.src_dir = f"{self.base_dir}/{self.dir}"
        FileUtils.make_dir(self.scan_dir)
        FileUtils.make_dir(self.success_dir)
        FileUtils.make_dir(self.failed_dir)
        FileUtils.make_dir(self.pdf_dir)
        FileUtils.make_dir(self.src_dir)
        FileUtils.make_dir(self.pending_scan_dir)
        FileUtils.make_dir(self.processed_scan_dir)

    @handle_errors
    def fetch_images(self):
        '''
        画像取得
        '''
        self.set_img_dir()
        my_logger.info(self.success_dir)
        files:list[str] = FileUtils.get_files(dir=self.success_dir, extention=".png")
        images = [ReceiptImage(path=path, row_images=self.row_images, idx=idx, upd_imgs=self.fetch_images) for idx, path in enumerate(files)]
        self.row_images.current.controls = images
        self.row_images.current.update()
    
    @handle_errors
    def extract_receipt_img(self):
        '''
        レシート画像抽出
        '''
        try:
            self.overlay.message_reciever().send("営業日報スキャンPDFを画像に変換中...")

            # スキャン結果のPDFをコピー
            FileUtils.copy_files(src=self.src_dir, dest=self.pdf_dir)

            # 画像に変換
            self.pdf_converter.convert(input_path=self.pdf_dir, output_path=self.pending_scan_dir, processed_dir=self.processed_scan_dir)
            
            self.overlay.message_reciever().send("レシート画像抽出中...")

            # テンプレートマッチング実行
            self.receipt_extracter.template_matching(input_path=self.pending_scan_dir, processed_dir=self.processed_scan_dir, success_path=self.success_dir, failed_path=self.failed_dir, template_path="./assets/template/template_x1.png")
            self.receipt_extracter.template_matching(input_path=self.pending_scan_dir, processed_dir=self.processed_scan_dir, success_path=self.success_dir, failed_path=self.failed_dir, template_path="./assets/template/template_z1.png")
            
            FileUtils.remove_duplicate_files(target_dir=self.failed_dir, processed_dir=self.success_dir)
            self.overlay.message_reciever().send("レシート画像抽出処理完了")

            MyMsgBox.show_msgbox(title=f"出力完了", msg=f"レシート画像の出力を完了しました。")
        except Exception as err:
            MyMsgBox.show_errmsgbox(title=f"出力失敗", msg=f"レシート画像の出力に失敗しました。")
            raise err
        finally:
            self.fetch_images()
            self.overlay.dismiss_progress()