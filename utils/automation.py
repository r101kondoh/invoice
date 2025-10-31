from functools import wraps
import time
from typing import Callable, Tuple
import flet as ft
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchAttributeException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.remote.webelement import WebElement
from common.my_msgbox import MyMsgBox
from common.my_progress import ProgressOverlay
from utils.error_handlers import handle_errors, log_error_with_traceback, show_msgbox_on_error
from logging import getLogger

from utils.file_utils import FileUtils
my_logger = getLogger()
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ChromeAutomation():
    """
    ブラウザ自動操縦クラス
    """
    @handle_errors
    def __init__(self, page:ft.Page):
        self.driver = None
        self.login_user = ""
        self.login_pass = ""
        self.overlay = ProgressOverlay(page=page)
        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-size=1920x1080")
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")

    @handle_errors
    def launch_webdriver(self):
        '''
        Webドライバを起動
        '''
        self.driver = webdriver.Chrome(options=self.chrome_options)

    @handle_errors
    def get_presence_elem(self, element_id) -> WebElement:
        '''
        指定したIDの表示されている要素を取得
        '''
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return elem
    
    @handle_errors
    def get_elem(self, element_id)->WebElement:
        '''
        指定したIDの要素を取得
        '''
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        return elem
    
    @handle_errors
    def get_class_elem(self, element_class)->WebElement:
        '''
        指定したクラス名の要素を取得
        '''
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, element_class))
        )
        return elem
    

    @handle_errors
    def get_elem_by_css(self, css_selector)->WebElement:
        '''
        指定したCSSセレクタの要素を取得
        '''
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        return elem

    @handle_errors    
    def get_table_from_elem(self, element_id) -> WebElement:
        '''
        指定したIDの要素からtableタグを抽出
        '''
        elem = self.get_elem(element_id)
        table = elem.find_element(By.TAG_NAME, "table")
        return table
    
    @handle_errors    
    def get_presence_of_all_elements_located(self, css_selector:str):
        '''
        指定したCSSセレクタと合致する要素を取得
        '''
        elems = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return elems
    
    @handle_errors
    def input_elem(self, target_elem:WebElement, script_value:str|None=None, key_code:str|None = Keys.ENTER, ):
        '''
        指定した要素に値を入力
        '''
        # 要素をクリック
        target_elem.click()

        # スクリプトを実行
        if script_value != None:
            script = f"arguments[0].value = '{script_value}';"
            self.driver.execute_script(script, target_elem)

        # 指定した値を入力
        if key_code != None:
            target_elem.send_keys(key_code)

    @handle_errors
    def upload_file(self, target_elem: WebElement, file_path: str):
        '''
        ファイルアップロード専用関数
        <input type="file"> にファイルを送信する
        '''
        # ファイル存在チェック
        abs_path = FileUtils.get_abspath(file_path)
        if not FileUtils.check_file_exists(abs_path):
            raise FileNotFoundError(f"指定されたファイルが存在しません: {abs_path}")

        # 非表示状態の場合は一時的に表示させる
        is_displayed = target_elem.is_displayed()
        if not is_displayed:
            self.driver.execute_script("arguments[0].style.display = 'block';", target_elem)

        # ファイルパスを送信（これでアップロードが実行される）
        target_elem.send_keys(abs_path)

        # 元の状態に戻す（必要なら）
        if not is_displayed:
            self.driver.execute_script("arguments[0].style.display = 'none';", target_elem)


    @handle_errors
    def click_elem(self, target_elem:WebElement):
        '''
        指定した要素をクリック
        '''
        self.input_elem(target_elem=target_elem, key_code=None)

    @handle_errors
    def redirect(self, url:str):
        '''
        指定したURLの画面に遷移
        '''
        while self.driver.current_url != url:
            self.driver.get(url)
    
    @handle_errors
    def wait_for_url(self, url:str, timeout=30):
        '''
        指定したURLの画面に遷移するまで待機する
        '''
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )
    
    @handle_errors
    def wait_for_element_visible_by_id(self,  element_id:str, timeout=10):
        '''
        指定したIDの要素が可視になるまで待機する
        '''
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
    
    @handle_errors
    def wait_for_table_visible(self, timeout=10):
        '''
        table要素が可視になるまで待機する
        '''
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, 'table'))
        )
    
    @handle_errors
    def wait_for_all_elements_visible_by_name(self,  name:str, timeout=10):
        '''
        指定したnameと一致する全ての要素が可視になるまで待機する
        '''
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located((By.NAME, name))
        )                               
    
    @handle_errors
    def wait_for_element_clickable(self, element_id:str, timeout=10):
        '''
        指定した要素がクリック可能になるまで待機する
        '''
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
    
    @handle_errors
    def scroll_to_bottom(self):
        '''
        最下部までスクロール
        '''
        # body =  WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.TAG_NAME, "body"))
        # )
        # body.click()
        # body.send_keys(Keys.PAGE_DOWN)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @handle_errors
    def scroll_to_bottom_right(self):
        '''
        右下までスクロール
        '''
        self.driver.execute_script("window.scrollTo(document.body.scrollWidth, document.body.scrollHeight);")


    @handle_errors
    def capture_window(self, path:str):
        '''
        スクリーンショットを撮る
        '''
        self.driver.save_screenshot(path)
    
    def quit_driver(self):
        '''
        ブラウザを閉じる
        '''
        if self.driver != None:
            self.driver.quit()

    # デコレータ
    def handle_automation_error(self, msg:str, ):
        '''
        自動処理のエラーハンドリング用デコレータ
        '''
        def decorator(func):  # NOTE: デコレータにカスタム引数を指定するためにdecoratorでラップ
            @wraps(func)      # NOTE: 関数のメタデータ・ドキュメントが保持される
            def wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    MyMsgBox.show_msgbox(title=f"{msg}完了", msg=f"{msg}を完了しました。")
                except PermissionError as err:
                    log_error_with_traceback(func, err)
                    MyMsgBox.show_errmsgbox(
                        f"{type(err).__name__}", 
                        f"{msg}に失敗しました。\n以下に示すエクセルファイルを閉じた後、\n{msg}を再実行してください。\n\n閉じるエクセルファイル：「{err.filename}」"
                    )
                except Exception as err:
                    log_error_with_traceback(func, err)
                    MyMsgBox.show_errmsgbox(f"{type(err).__name__}", f"{msg}に失敗しました。")
                finally:
                    self.overlay.message_reciever().send("Chrome終了中...")
                    self.quit_driver()
                    self.overlay.dismiss_progress()
            return wrapper
        return decorator
    
    # デコレータ
    def retry_execution(self, retries:int=5):
        '''
        指定した回数処理を繰り返すデコレータ
        '''
        def decorator(func):  # NOTE: デコレータにカスタム引数を指定するためにdecoratorでラップ
            @wraps(func)      # NOTE: 関数のメタデータ・ドキュメントが保持される
            def wrapper(*args, **kwargs):
                for _ in range(retries):
                    time.sleep(0.1) 
                    func(*args, **kwargs)
            return wrapper
        return decorator
    
    def conditional_loop(self, max_retries:int = 1000):
        '''
        指定した条件を満たすまでループを行うデコレータ
        '''
        def decorator(func):  # NOTE: デコレータにカスタム引数を指定するためにdecoratorでラップ
            @wraps(func)      # NOTE: 関数のメタデータ・ドキュメントが保持される
            def wrapper(*args, **kwargs):
                loop_count = 0
                while loop_count < max_retries:
                    # NOTE: funcは真偽値と文字列のタプルを返すように設計
                    complete = func(*args, **kwargs)
                    if complete:
                        break
                    loop_count += 1
            return wrapper
        return decorator