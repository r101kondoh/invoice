from abc import ABC, abstractmethod
from typing import List

class BaseHTMLDataToExcelConverter(ABC):
    """
    指定したデータソースを基にエクセル表を出力するインタフェース
    """
    def __init__(self, data_source:List[str]):
        self.data_source = data_source

    @abstractmethod
    def convert_to_excel(self, period:str):
        '''
        エクセルの出力
        '''
        pass