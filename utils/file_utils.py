
import os
import shutil
# from db.branch import Branch
# from db.staff import Staff, StaffRole
from utils.error_handlers import handle_errors


class FileUtils():
    """
    ファイル・ディレクトリ操作に関するロジック
    """
    @handle_errors
    def check_file_exists(file_name:str):
        '''
        ファイルの存在チェック
        '''
        return os.path.exists(file_name) and os.path.isfile(file_name)
    
    @handle_errors
    def check_dir_exists(dir:str):
        '''
        ディレクトリの存在チェック
        '''
        return os.path.exists(dir) and os.path.isdir(dir)
    
    @handle_errors
    def make_dir(dir_name:str):
        '''
        ディレクトリの新規作成
        '''
        os.makedirs(dir_name, exist_ok=True)

    @handle_errors
    def rename(old_path:str, new_path:str):
        '''
        パスのリネーム
        '''
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    @handle_errors
    def move_dir(srt_path, dest_path):
        '''
        ディレクトリの移動
        '''
        if os.path.exists(srt_path):
            shutil.move(srt_path, dest_path)

    @handle_errors
    def get_yearmonth_dir(str_year:str, str_month:str, target_dir:str):
        '''
        指定した年月に対応するディレクトリのパスを取得
        '''
        path = f"./output/{target_dir}/{str_year}/{str_month}"
        FileUtils.make_dir(path)
        return path
    
    @handle_errors
    def get_date_dir(str_year:str, str_month:str, str_date:str, target_dir:str):
        '''
        指定した年月に対応するディレクトリのパスを取得
        '''
        path = f"./output/{target_dir}/{str_year}/{str_month}/{str_date}"
        FileUtils.make_dir(path)
        return path
    
    @handle_errors
    def copy_files(src:str, dest:str):
        '''
        指定したディレクトリー間のファイルコピー処理
        '''
        # dest_file_path = 
        for file_name in os.listdir(src):
            if file_name.endswith('.pdf'):
                src_file_path = os.path.join(src, file_name)
                dest_file_path = os.path.join(dest, file_name)

                if not os.path.exists(dest_file_path):
                    shutil.copy2(src_file_path, dest_file_path)

    @handle_errors
    def remove_duplicate_files(target_dir: str, processed_dir: str):
        """
        処理済みフォルダに同名ファイルが存在する場合、
        ターゲットフォルダ内の重複ファイルを削除する。
        """
        for filename in os.listdir(target_dir):
            error_file_path = os.path.join(target_dir, filename)
            processed_file_path = os.path.join(processed_dir, filename)

            if os.path.isfile(error_file_path) and os.path.exists(processed_file_path):
                os.remove(error_file_path)

    @handle_errors
    def get_files(dir:str, extention:str):
        '''
        指定したディレクトリ内の全てのファイルを削除
        '''
        return [os.path.join(dir, file_name)  for file_name in os.listdir(dir) if file_name.endswith(extention)]
            
    @handle_errors
    def del_files(dir:str):
        '''
        指定したディレクトリ内の全てのファイルを削除
        '''
        for file_name in os.listdir(dir):
            file_path = os.path.join(dir, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    @handle_errors
    def del_file(file_path:str):
        '''
        指定したファイルを削除
        '''
        if os.path.isfile(file_path):
            os.unlink(file_path)
    
    @handle_errors
    def get_invoice_templaet_excel_path():
        '''
        請求書明細書テンプレートのパスを取得
        '''
        return "./assets/templates/請求書明細書テンプレート(結合解除).xlsx"
    
    @handle_errors
    def get_invoice_templaet_excel_path():
        '''
        請求書明細書テンプレートのパスを取得
        '''
        return "./assets/templates/請求書明細書テンプレート(結合解除).xlsx"
    
    @handle_errors
    def get_shop_list_excel_path():
        '''
        店舗一覧表のパスを取得
        '''
        return "./assets/店舗一覧.xlsx"
    
    @handle_errors
    def get_factory_invoice_templaet_excel_path():
        '''
        工場請求書明細書テンプレートのパスを取得
        '''
        return "./assets/templates/きょくとう 春糸事業所テンプレート.xlsx"
    
    @handle_errors
    def get_abspath(file_path:str):
        '''
        指定したパスの絶対パスを取得
        '''
        return os.path.abspath(file_path)
    
    # @handle_errors
    # def get_staff_dir(staff:Staff, branch:Branch|None=None):
    #     '''
    #     指定したスタッフのフォルダを取得
    #     '''
    #     branch:Branch = branch if branch is not None else staff.branch
    #     return f"./output/スタッフ/{branch.id}_{branch.name}/{StaffRole.from_value(staff.role).label}/{staff.id}_{staff.name}"