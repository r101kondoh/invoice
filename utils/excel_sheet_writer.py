from abc import ABC, abstractmethod
from utils.df_utils import DataFrameUtils
from utils.excel_utils import ExcelUtils

class ExcelSheetWriter(ABC):
    """
    売上表データの書き込みを行う基底クラス
    """
    def __init__(self, excel_writer:ExcelUtils, period:str, df:DataFrameUtils):
        self.excel_writer = excel_writer
        self.period = period
        self.df = df
        
    
    @abstractmethod
    def set_date_info(self):
        '''
        日付関連情報を書き込む
        '''
        pass

    @abstractmethod
    def add_standard_data_row(self):
        '''
        データ行を追加する
        '''
        pass

    
    @abstractmethod
    def del_standard_data_row(self):
        '''
        データ行を削除する
        '''
        pass

    @abstractmethod
    def set_standard_data_row(self):
        '''
        データ行に値をセット
        '''
        pass