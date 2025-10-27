import flet as ft

from app.receipt.logic.pdf_converter import PDFConverter
from app.receipt.logic.receipt_extracter import ReceiptExtracter
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
        self.src_dir = r"\\192.168.5.1\scan\近藤"

        # PDF格納フォルダ      
        self.resorce_path = r"./output/receipt/pdf"

        # PDFの画像変換器
        self.pdf_converter = PDFConverter(pdf_path=self.resorce_path)

        # レシート画像切り出し器
        self.receipt_extracter = ReceiptExtracter()

        # オーバーレイ
        self.overlay = ProgressOverlay(page=page)

    @handle_errors
    def fetch_images(self):
        # pass
        files:list[str] = FileUtils.get_files(dir="./output/receipt/img/matching/success", extention=".png")
        images = [ReceiptImage(path=path, row_images=self.row_images, idx=idx) for idx, path in enumerate(files)]
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
            FileUtils.copy_files(src=self.src_dir, dest=self.resorce_path)

            # 画像に変換
            self.pdf_converter.convert()
            
            self.overlay.message_reciever().send("レシート画像抽出中...")

            # テンプレートマッチング実行
            self.receipt_extracter.template_matching(input_path="./output/receipt/img/scan", template_path="./assets/template/template_x1.png")
            self.receipt_extracter.template_matching(input_path="./output/receipt/img/matching/failed", template_path="./assets/template/template_z1.png")
            
            FileUtils.remove_duplicate_files(target_dir="./output/receipt/img/matching/failed", processed_dir="./output/receipt/img/matching/success")
            self.overlay.message_reciever().send("レシート画像抽出処理完了")


            MyMsgBox.show_msgbox(title=f"出力完了", msg=f"レシート画像の出力を完了しました。")
        except Exception as err:
            MyMsgBox.show_errmsgbox(title=f"出力失敗", msg=f"レシート画像の出力に失敗しました。")
            raise err
        finally:
            self.fetch_images()
            self.overlay.dismiss_progress()