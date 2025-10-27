
from logging import getLogger
from functools import wraps
import traceback
from typing import Callable
from common.my_msgbox import MyMsgBox
from common.my_progress import ProgressOverlay
my_logger = getLogger()

def log_error(func, err:Exception):
    '''
    エラーをログに記録する
    '''
    my_logger.error(f"[{func.__name__}] raised : {type(err).__name__}")

def log_error_with_traceback(func, err:Exception):
    '''
    エラースタックトレースをログに記録する
    '''
    # tb = traceback.extract_tb(err.__traceback__)[-1]    # 最新のトレース情報を取得
    # log_error(func, err)
    my_logger.error(f"[{func.__name__}] catched: {type(err).__name__}")
    my_logger.error(traceback.format_exc())

# デコレータ
def handle_errors(func):
    '''
    エラーログを記録するデコレータ
    '''
    @wraps(func) # NOTE: 関数のメタデータ・ドキュメントが保持される
    def wrapper(*args, **kwargs):
        try:
            # 関数を実行
            return func(*args, **kwargs)
        except Exception as err:
            log_error(func, err)
            raise err
    return wrapper

# デコレータ
def show_msgbox_on_error(
        err_title:str, err_msg:str,
        success_title:str|None = None, success_msg:str|None= None,
        show_success_msg_flg:bool = False, raise_err_flg:bool = False,
        finally_method: Callable | None = None
    ):
    '''
    メッセージボックスにより処理の成否を表示するデコレータ
    '''
    def decorator(func): # NOTE: デコレータにカスタム引数を指定するためにdecoratorでラップ
        @wraps(func)      # NOTE: 関数のメタデータ・ドキュメントが保持される
        def wrapper(*args, **kwargs):
            self = args[0]
            overlay = None
            is_ok = False

            # 処理中にオーバーレイが表示されている場合
            if "overlay" in dir(self):
                if isinstance(self.overlay, ProgressOverlay):
                    overlay = self.overlay
                    overlay.show_progress()
            try:
                func(*args, **kwargs)
                is_ok = True
            except Exception as err:
                log_error_with_traceback(func, err)
                MyMsgBox.show_errmsgbox(err_title, f"{err_msg}\n:{err}")
            finally:
                if is_ok and show_success_msg_flg:
                    MyMsgBox.show_msgbox(success_title, success_msg)
                if overlay is not None:
                    overlay.dismiss_progress()
        return wrapper
    return decorator