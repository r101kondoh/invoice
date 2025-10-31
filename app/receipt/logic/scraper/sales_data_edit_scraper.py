import time
from bs4 import BeautifulSoup
import flet as ft
from logging import getLogger
from utils.automation import ChromeAutomation
from utils.date_utils import DateUtils
from utils.df_utils import DataFrameUtils
from utils.error_handlers import handle_errors
from utils.file_utils import FileUtils
from utils.pos_scraper import PosScraper
import os
my_logger = getLogger()

class SalesDataEditScraper(ChromeAutomation):
    """
    売上データ自動入力クラス
    """
    @handle_errors
    def __init__(self, page:ft.Page):
        super().__init__(page=page)
        self.login_user = os.environ.get("SALES_EDIT_LOGIN_ID")
        self.login_pass = os.environ.get("SALES_EDIT_LOGIN_PASS")

    @handle_errors
    def login(self):
        '''
        ログイン処理
        '''
        self.driver.get(os.environ.get("SALES_EDIT_AUTH_URL"))
        self.overlay.message_reciever().send("システムにログイン中...")

        # ログインID入力
        txt_login_id = self.get_elem("login_user_code")
        self.input_elem(txt_login_id, self.login_user, key_code=None)
                        
        # パスワード入力
        txt_pass = self.get_elem("login_user_password")
        self.input_elem(txt_pass, self.login_pass)

    @handle_errors
    def edit_sales_data(self, year:int, month:int):
        '''
        売上データ編集
        '''
        self.overlay.message_reciever().send("売上表画面に遷移中...")

        # 切り出したレシート画像を格納しているディレクトリ
        dir = FileUtils.get_yearmonth_dir(f"{year}", f"{month:02}", "receipt")
        success_dir = f"{dir}/img/matching/success"

        # メニュー画面に遷移するまで待機
        self.wait_for_url(url=os.environ.get("SALES_EDIT_MENU_URL"))

        # 売上データ一覧画面に遷移
        self.redirect(url=os.environ.get("SALES_EDIT_SALES_DATA_LIST"))

        # 売上期間入力
        self.overlay.message_reciever().send("期間入力中...")

        # 開始日
        from_date = self.get_elem("from_date")
        self.input_elem(from_date, f"{year}/{month}/1")

        # 終了日
        to_date = self.get_elem("to_date")
        end_day = DateUtils.lastday(year, month)
        self.input_elem(to_date, f"{year}/{month}/{end_day}")

        # レシート画像ファイルパス一覧
        files:list[str] = FileUtils.get_files(dir=success_dir, extention=".png")
        
        # 画像ファイル名の「日付_来客人数_売上金額」から各データをリスト形式で取得
        day_quantity_amount_list = [file.replace('.png', '').split('\\')[1].split('_') for file in files]
        time.sleep(1)

        # テーブルから各日付の売上データ編集画面(状態が「未確定」)のリンクを取得
        links = self.get_unconfirmed_links("shop-sales-report-list")
        dates = [link[0].split('/')[1].split('(')[0] for link in links]
        
        # ベースURL
        base_url = f"{os.environ.get("SALES_EDIT_SALES_DATA_LIST")}"

        # 新規作成画面URL
        new_url = os.environ.get("SALES_EDIT_NEW")
        
        for day in range(1, end_day+1):

            # 日付と合致する売上・来客数データを取得
            day_quantity_amount = next((x for x in day_quantity_amount_list if x[0] == f"{day:02}"), None)

            # 日付と合致する画像パスを取得
            img_file_path = next((f for f in files if f.split('\\')[1].split('_')[0] == f"{day:02}"), None)
            
            # 「未確定」日付のデータを更新
            if str(day) in dates:
                # 編集画面に遷移
                link = next((x for x in links if x[0].split('/')[1].split('(')[0] == str(day)), None)
                str_date, href = link
                self.overlay.message_reciever().send(f"{str_date}の編集画面に遷移中...")
                id = href.split('/')[3].split("?")[0]
                edit_url = f"{base_url}/{id}/edit"
                self.redirect(edit_url)

                # 登録画像削除ボタン押下
                if "日" not in str_date:
                    try:
                        buttons = self.get_presence_of_all_elements_located(css_selector="a.js-remove-element")
                        for i, btn in enumerate(buttons, start=1):
                            self.click_elem(btn)
                    except Exception as err:
                        my_logger.info("登録画像なし")

                receipt_img = self.get_presence_elem("data_")
                if img_file_path is not None:
                    self.upload_file(target_elem=receipt_img, file_path=img_file_path)

                amount = self.get_elem("shop_sales_detail_net_sales")
                self.input_elem(amount, day_quantity_amount[2] if day_quantity_amount is not None else 0, None)
                
                quantity = self.get_elem("shop_sales_detail_customer_quantity")
                self.input_elem(quantity, day_quantity_amount[1] if day_quantity_amount is not None else 0)
            
            # 新規登録 
            else:
                # 新規作作成画面に遷移
                self.redirect(url=new_url)
                    
                receipt_img = self.get_presence_elem("data_")
                if img_file_path is not None:
                    self.upload_file(target_elem=receipt_img, file_path=img_file_path)

                amount = self.get_elem("shop_sales_detail_net_sales")
                self.input_elem(amount, day_quantity_amount[2] if day_quantity_amount is not None else 0, None)
                
                quantity = self.get_elem("shop_sales_detail_customer_quantity")
                self.input_elem(quantity, day_quantity_amount[1] if day_quantity_amount is not None else 0, None)

                sales_date = self.get_elem("shop_sales_detail_sales_date")
                self.input_elem(sales_date, f"{year}/{month}/{day}")

                submit_btn = self.get_elem_by_css("input[type='submit'][value='売上報告を登録して終了する']")
                self.click_elem(submit_btn)
            
            time.sleep(1)

    def execute_automation(self, year:int, month:int):
        '''
        売上データ入力自動処理を実行
        '''
        # NOTE: 親クラスの自動処理のエラーハンドリングデコレータでラップ
        @self.handle_automation_error(msg="売上データ入力")
        def execute_process():
            '''
            売上表取得自動処理
            '''
            self.overlay.message_reciever().send("Chromeを起動中...")
            self.launch_webdriver()
            self.login()
            self.edit_sales_data(year=year, month=month)
            self.overlay.message_reciever().send("データ入力完了")
        return execute_process()
    
    @handle_errors
    def get_unconfirmed_links(self, element_id) -> list[tuple[str, str]]:
        '''
        table内の各trを走査し、tdに「未確定」を含む行のaタグリンク(テキスト, href)を抽出
        '''
        table = self.get_table_from_elem(element_id)
        html = table.get_attribute("outerHTML")

        soup = BeautifulSoup(html, "html.parser")

        result = []

        # 各行(tr)をループ
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")

            # どれかのtdに「未確定」が含まれているかチェック
            if any("未確定" in td.get_text(strip=True) for td in tds):
                # その行のaタグを取得
                for a in tr.find_all("a", href=True):
                    text = a.get_text(strip=True)
                    href = a["href"]
                    result.append((text, href))

        return result
