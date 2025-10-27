import calendar
import datetime
import itertools
import json
from typing import Dict, List, TypedDict
from dateutil.relativedelta import relativedelta
import jpholiday
STR_WEEK_LIST =("日", "月", "火", "水", "木", "金", "土")
NUM_DAYS = len(STR_WEEK_LIST) * 6 
from logging import getLogger
my_logger = getLogger()

class EraInfo(TypedDict):
    """
    和暦の情報
    """
    start_date:str      # 開始年月日
    abbreviation:str    # 和暦略称（例：R、H、S）
EraData = Dict[str, EraInfo]

class DateUtils():
    """
    日付処理に関するロジック
    """   
    def today():
        '''
        今日の日付を取得
        '''
        return datetime.date.today()
    
    def now():
        '''
        現在時刻を取得
        '''
        return datetime.datetime.now()
    
    def todays_yearmonth():
        today:datetime.date = DateUtils.today()
        return today.year, today.month
    
    def firstdate(year:int, month:int) ->datetime.date:
        '''
        指定した年月の初日を取得
        '''
        return datetime.datetime(year, month, 1).date()

    def firstday(year:int, month:int) ->datetime.date:
        '''
        指定した年月の初日の日を取得
        '''
        return datetime.datetime(year, month, 1).day
    
    def selectdate(year:int, month:int, day:int) -> datetime.date:
        '''
        指定した年月日を取得
        '''
        return datetime.date(year, month, day)
    
    def is_today_expired_target_date(year:int, month:int, day:int):
        '''
        今日が指定年月以降かどうか判定
        '''
        return DateUtils.today() > DateUtils.selectdate(year, month, day)
    
    def lastdate(year:int, month:int) -> datetime.date:
        '''
        指定した年月の最終日付を取得
        '''
        return (datetime.datetime(year, month, 1) + relativedelta(months=1, days=-1)).date()

    def lastday(year:int, month:int)->int:
        '''
        指定した年月の最終日を取得
        '''
        return (datetime.datetime(year, month, 1) + relativedelta(months=1, days=-1)).day
    
    def is_future(year:int, month:int):
        '''
        指定年月の最終日を過ぎているか判定
        '''
        return DateUtils.today() <= DateUtils.lastdate(year, month)
    
    def split_period_to_str_yearmonth(period:str)->tuple[str, str]:
        '''
        指定した期間（を表す文字列）を、0埋めの年と月の文字列に分割
        '''
        str_year=period[:4]
        str_month=period[4:]
        return str_year, str_month
    
    def split_period_to_str_date(period:str)->tuple[str, str, str]:
        '''
        指定した期間（を表す文字列）を、0埋めの年と月の文字列に分割
        '''
        str_year=period[:4]
        str_month=period[4:6]
        str_date = period[6:]
        return str_year, str_month, str_date
    
    def get_four_weeks_ago(date:datetime.date)->datetime.date:
        '''
        指定した日付の4週前の日付を取得
        '''
        return date - datetime.timedelta(days=28)
    
    def get_yesterday(date:datetime.date)->datetime.date:
        '''
        指定した日付の前日を取得
        '''
        return date - datetime.timedelta(days=1)
    
    def period_to_num_yaermonth(period:str)->tuple[int, int]:
        '''
        指定した期間（を表す文字列）から、数値の年と月を取得
        '''
        str_yaer, str_month = DateUtils.split_period_to_str_yearmonth(period)
        return int(str_yaer), int(str_month)
    
    def format_date_to_japanese(date_str:str)->str:
        '''
        「yyyy/MM/dd（aa）」形式の日付文字列を「MM月dd日」形式に変換
        '''
        date_str_clean = date_str.split('(')[0]
        date_obj = datetime.datetime.strptime(date_str_clean, '%Y/%m/%d')
        return f"{date_obj.month}月{date_obj.day}日"
    
    def format_date(date:datetime.date)->str:
        '''
        日付を文字列として返す
        '''
        return date.strftime('%Y年%m月%d日')
    
    def format_period_date(date:datetime.date)->str:
        '''
        日付文字列を返す
        '''
        return f"{date.year}{date.month:02}{date.day:02}"
    
    def convert_to_japanese_era(date:datetime.date, is_output_kanji:bool=False):
        '''
        西暦→和暦の変換
        '''
        with open('./assets/era.json', 'r', encoding='utf-8') as file:
            data:EraData = json.load(file)
            WAREKI_START = {
                era:{
                    'start_date':datetime.datetime.strptime(info['start_date'], "%Y-%m-%d").date(),
                    'abbreviation': info['abbreviation']
                }
                for era, info in data.items()
            }
        y_m_d = date
        sotred_era_keys = sorted(WAREKI_START.keys(), key=lambda k: WAREKI_START[k]["start_date"], reverse=True)
        for era in sotred_era_keys:
            if WAREKI_START[era]['start_date'] <= y_m_d:
                era_year = y_m_d.year
                start_year = WAREKI_START[era]['start_date'].year
                year = (era_year - start_year) + 1
                era_str = era if is_output_kanji else WAREKI_START[era]['abbreviation']
                break
        else:
            return '昭和以前'
        
        if year == 1:
            year = '元'

        return era_str + str(year) + '年'
    
    def generate_calendar_with_weekdays(year:int, month:int):
        '''
        指定した年月に対応するカレンダーの曜日つき日付リストを取得
        '''
        calendar.setfirstweekday(calendar.SUNDAY)
        cal = calendar.monthcalendar(year, month)
        result = []

        for week in cal:
            for i, day in enumerate(week):
                if day != 0:
                    result.append((day, STR_WEEK_LIST[i]))
        return result
        
    def generete_calendar_days(year:int, month:int) -> List[int]:
        '''
        指定した年月に対応するカレンダーの日付リストを取得
        '''
        calendar.setfirstweekday(calendar.SUNDAY)
        flat = list(itertools.chain.from_iterable(calendar.monthcalendar(year, month)))
        # my_logger.info(flat)

        # 日付のゼロ埋め
        num_calendar_days = len(flat)
        if num_calendar_days != NUM_DAYS:
            num_other_month_days = NUM_DAYS - num_calendar_days
            flat.extend([0] * num_other_month_days)

        return flat
    
    def is_holiday(year:int, month:int, day:int):
        '''
        祝日判定
        '''
        date = DateUtils.selectdate(year, month, day)
        return jpholiday.is_holiday(date)
    
    def get_str_now():
        '''
        文字列で現在日付時刻を取得
        '''
        now:datetime.datetime = DateUtils.now()
        return now.strftime(f"%Y%m%d%H%M%S")