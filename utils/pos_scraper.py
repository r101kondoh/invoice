from typing import List, Tuple
from utils.automation import ChromeAutomation
from utils.error_handlers import handle_errors
import os
import flet as ft

class PosScraper(ChromeAutomation):
    """
    POSのスクレイピング自動処理クラス
    """
    @handle_errors
    def __init__(self, page:ft.Page, target_name:str, target_url:str, target_shop_codes:List[str]):
        super().__init__(page=page)
        self.login_user = os.environ.get("POS_LOGIN_ID")
        self.login_pass = os.environ.get("POS_LOGIN_PASS")
        self.target_name = target_name
        self.target_url = target_url
        self.target_shop_codes = target_shop_codes

    @handle_errors
    def login(self):
        '''
        ログイン処理
        '''
        self.driver.get(os.environ.get("POS_AUTH_URL"))
        self.overlay.message_reciever().send("システムにログイン中...")
        
        # ログインID入力
        txt_login_id = self.get_elem("userid")
        self.input_elem(txt_login_id, self.login_user)
        
        # パスワード入力
        txt_pass = self.get_elem("pass")
        self.input_elem(txt_pass, self.login_pass)
        
        # ログインボタン押下
        btn_login = self.get_elem("btn1")
        self.click_elem(btn_login)

        # メニュー画面に遷移するまで待機
        self.wait_for_url(url=os.environ.get("POS_MENU_URL"))
    
    
    def execute_automation(self, periods:Tuple[str, ...]):
        '''
        自動処理を実行
        '''
        pass