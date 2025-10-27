import copy
from functools import wraps
from io import StringIO
from typing import Callable, List, Set, Tuple
import unicodedata
import pandas as pd

from utils.error_handlers import handle_errors

class DataFrameUtils():
    """
    データフレーム処理に関するロジック
    """
    @handle_errors
    def __init__(self, data_source:list=[], columns:List[str]=[]):
        self.df:pd.DataFrame = pd.DataFrame(
            data_source,
            columns=columns
        )

    @staticmethod
    def copy(df:"DataFrameUtils"):
        '''
        DataFrameUtilsインスタンスをシャローコピー
        '''
        return copy.copy(df)
    
    @handle_errors
    def concat_columns(self, df_list:List["DataFrameUtils"]):
        '''
        データフレームの列を結合（横方向への拡張）
        '''
        self.df = pd.concat([df.df for df in df_list], axis=1)

    @handle_errors    
    def concat_rows(self, df_list:List["DataFrameUtils"]):
        '''
        データフレームの行を結合(縦方向への拡張)
        '''
        self.df = pd.concat([df.df for df in df_list], axis=0)

    @handle_errors
    def reorder_columns(self, col_labels:List[str]):
        '''
        列の並べ替えを行う
        '''
        self.df = self.df[col_labels]
    
    @handle_errors
    def get_even_index_row(self, cols:List[int]):
        '''
        インデックスが偶数の行を取得し、指定した列番号の列を残す
        '''
        self.df = self.df[(self.df.index % 2 == 0) & (self.df.index > 1)].iloc[:, cols]

    @handle_errors
    def get_odd_index_row(self, cols:List[int]):
        '''
        インデックスが奇数の行を取得し、指定した列番号の列を残す
        '''
        self.df = self.df[(self.df.index % 2 == 1) & (self.df.index > 1)].iloc[:, cols]
    
    @handle_errors
    def set_columns(self, columns:List[str]):
        '''
        列名を設定
        '''
        self.df.columns = columns

    def set_data_to_col(self, col_label:str, data):
        '''
        指定した列にデータをセット
        '''
        self.df[col_label] = data

    def copy_col_data(self, src_col_label:str, dest_col_label:str):
        '''
        指定した列にデータをセット
        '''
        self.df[dest_col_label] = self.df[src_col_label]

    @handle_errors
    def reset_index(self):
        '''
        インデックスの数値をリセット
        '''
        self.df = self.df.reset_index(drop=True)

    @handle_errors
    def apply(self, col_label:str, func:Callable[[str], str]):
        '''
        指定した列に対してデータ加工を行う
        '''
        self.df[col_label] = self.df[col_label].apply(func)

    @handle_errors
    def remove_space(self, col_label:str):
        '''
        指定した列のデータの空白を除去
        '''
        str_array = self.df[col_label].str.split()
        self.df[col_label] = [''.join(names) if type(names) == list else '' for names in str_array]

    @handle_errors
    def read_html_tbl(self, html:str):
        '''
        htmlを読み込む
        '''
        self.df = pd.read_html(StringIO(html))[0]

    @handle_errors
    def filter_by_col_val(self, col_label:str, value):
        '''
        指定した列が指定した値と一致する行を返す
        '''
        self.df = self.df[self.df[col_label] == value]

    @handle_errors
    def filter_where_columns_equal(self, col1_label:str, col2_label:str):
        '''
        指定した2列の値が一致する行を返す
        '''
        self.df = self.df[self.df[col1_label] == self.df[col2_label]]
    
    @handle_errors
    def sort_num(self, sort_cols:List[str]):
        '''
        指定した列(数値・数値をあらわす文字)でソートしたデータフレームを返す
        '''
        self.df = self.df.sort_values(by=sort_cols, key=lambda x: x.astype(int)).reset_index()

    @handle_errors
    def sort_date(self, sort_cols:List[str]):
        '''
        指定した列(日付)でソートしたデータフレームを返す
        '''
        self.df = self.df.sort_values(by=sort_cols).reset_index()

    @handle_errors
    def sort_index(self):
        '''
        データフレームのインデックスでソート
        '''
        self.df = self.df.sort_index()

    @handle_errors
    def col_val_to_datetime(self, col_label:str, format:str="%Y/%m/%d"):
        '''
        指定した列の型をdatetime型に変換
        '''
        self.df[col_label] = pd.to_datetime(self.df[col_label], format=format)

    @handle_errors
    def read_exel(self, path:str):
        '''
        指定したパスのエクセルファイルを読み込む
        '''
        self.df = pd.read_excel(path, index_col=0)

    @handle_errors
    def save_to_excel(self, path:str, index:int=0):
        '''
        指定したパスにエクセルファイルを保存
        '''
        self.df.to_excel(path, index=index)

    @handle_errors
    def save_to_csv(self, path:str):
        '''
        指定したパスにCSVファイルを保存
        '''
        self.df.to_csv(path, index=False, encoding="shift_jis")

    @handle_errors
    @staticmethod
    def save_to_each_excel_sheets(writer:pd.ExcelWriter, sheet_name:str, target:"DataFrameUtils"):
        '''
        指定したシートに出力
        '''
        target.df.to_excel(writer, sheet_name=sheet_name)

    @handle_errors
    def get_value(self, row:int, col:int):
        '''
        指定した行と列のデータフレームの値を取得
        '''
        return self.df.iloc[row, col]
    
    @handle_errors
    def dropna_all(self):
        '''
        全項目が空白の行を削除
        '''
        self.df = self.df.dropna(how="all")

    @handle_errors
    def drop_in_range(self, start:int, stop:int):
        '''
        指定した範囲のインデックスの行を返す
        '''
        self.df = self.df.drop(index=range(start, stop))

    def drop_dipulicates(self, subset:List[str]):
        '''
        指定した列の値が重複している行を除去
        '''
        self.df = self.df.drop_duplicates(subset=subset, keep="first")

    def dropna_subset(self, subset:List[str]):
        '''
        指定した列が空白である行を除去
        '''
        self.df = self.df.dropna(subset=subset)
    
    def drop_keywards_matched_row(self, col_label:str, subset:List[str]):
        '''
        指定した列に指定した値が含まれている行を除去
        '''
        self.df = self.df[~self.df[col_label].isin(subset)]

    def drop_matched_df_col(self, col_label:str, other_df:"DataFrameUtils", subset:List[str]):
        '''
        指定した列に指定したデータフレーム（の列）の値が含まれる行を除去
        '''
        self.df = self.df[~self.df[col_label].isin(other_df.df[col_label])]

    @handle_errors
    def proccess_each_row(self):
        '''
        データフレームの各行について処理を行うデコレータ
        '''
        def decorator(func):  # NOTE: デコレータにカスタム引数を指定するためにdecoratorでラップ
            @wraps(func)      # NOTE: 関数のメタデータ・ドキュメントが保持される
            def wrapper(*args, **kwargs):
                for index, row in self.df.iterrows():
                    func(row, index, *args, **kwargs)
            return wrapper
        return decorator
    
    @handle_errors
    @staticmethod
    def with_excel_writer(file_path:str, **writer_kwargs):
        '''
        エクセル出力を行うデコレータ
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with pd.ExcelWriter(file_path, **writer_kwargs) as writer:
                    return func(writer, *args, **kwargs)
            return wrapper
        return decorator
    

    def __len__(self):
        '''
        データフレームの長さを返す
        '''
        return len(self.df)