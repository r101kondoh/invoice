import os
import fitz
from logging import getLogger
my_logger = getLogger()

class PDFConverter:
    """
    PDFを画像変換するクラス
    """
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.output_path = "./output/receipt/img/scan"
        
    def convert(self):
        '''
        PDFの画像変換処理
        '''
        try:
            for file_name in os.listdir(self.pdf_path):
                if file_name.endswith('.pdf'):
                    (f"{file_name}の処理実行中...")
                    # pdfファイルの読み込み
                    pdf_document = fitz.open(os.path.join(self.pdf_path, file_name))
            
                    # 各ページをJPEGに変換
                    for page_num in range(len(pdf_document)):
                        page = pdf_document.load_page(page_num)  # 各ページをロード
                        pix = page.get_pixmap(matrix=fitz.Matrix(2,2))  # 画像ピクセルを取得
                        
                        # 出力するJPEGのパスを設定
                        # file_name = os.path.basename(self.pdf_path)
                        output_image_path = os.path.join(self.output_path, f'{file_name[:-4]}_page{page_num + 1}.png')
                
                        # 画像を保存
                        pix.save(output_image_path)
                        
            my_logger.info("すべてのPDFの変換が完了し、画像は新しいフォルダに保存されました。")
        except Exception as err:
            my_logger.error(err)
            raise err
        finally:
            if pdf_document:
                pdf_document.close()