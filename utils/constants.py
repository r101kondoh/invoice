import flet as ft

URL_GENERATE_INVOICE = "/invoice_automation"
URL_GENERATE_CUSTOMER_LIST = "/customer_list_automation"
URL_MNG_STAFF = "/mng_staff"
URL_MNG_ATTENDANCE = "/attendance"
URL_STAFF_DETAIL = "/staff_detail/:id"
URL_LUNCH = "/lunch"
URL_DAILY_REPORT = "/daily_report"
URL_MNG_TASK = "/mng_task"

DEFAULT_NUM_ROW = 3                 # 標準の行数（請求書、明細書ともに3行）

IDX_INVOICE_FIRST_ROW = 27          # 請求書先頭行
IDX_INVOICE_STANDARD_ROW = 28       # 請求書標準行（行を増やす際のコピー元になる）
IDX_INVOICE_INSERT_TARGET_ROW = 29  # 請求書行挿入位置（行を増やす際のコピー先になる）
IDX_INVOICE_SUM_ROW = 30            # 請求書合計行

IDX_DETAIL_TITLE = 41               # 明細行見出し行
IDX_DETAIL_RATE_FIRST_ROW = 44      # 明細（請求率型）先頭行
IDX_DETAIL_RATE_STANDARD_ROW = 45   # 明細（請求率型）標準業（行を増やす際のコピー元になる）
IDX_DETAIL_RATE_INSERT_TARGET_ROW = 46  # 明細（請求率型）行挿入位置（行を増やす際のコピー先になる）
IDX_DETAIL_RATE_SUM_ROW = 47        # 明細（請求率型）合計行
IDX_DETAIL_SALARY_FIRST_ROW = 50    # 明細（給与型）先頭行
IDX_DETAIL_SALARY_STANDARD_ROW = 51 # 明細（給与型）標準業（行を増やす際のコピー元になる）
IDX_DETAIL_SALARY_INSERT_TARGET_ROW = 52    # 明細（給与型）行挿入位置（行を増やす際のコピー先になる）
IDX_DETAIL_SALARY_SUM_ROW = 53      # 明細（給与型）合計行
IDX_TOTAL_ROW = 56                  # 総計行

HEIGHT_INVOICE_ROW = 32.50          # 請求書行の高さ
HEIGHT_DETAIL_ROW = 25              # 明細行高さ
HEIGHT_SUM_ROW = 30                 # 合計行の高さ

MOBILE_PETTERN = r"^(0[789]0|0800)-?\d{4}-?\d{4}$"
MOBILE_PETTERN_NON_HYPHEN = r"^(0[789]0|0800)?\d{8}$"


CONDITION_ICONS = [
    ft.Icons.SENTIMENT_VERY_DISSATISFIED_SHARP,
    ft.Icons.SENTIMENT_DISSATISFIED_SHARP,
    ft.Icons.SENTIMENT_SATISFIED,
    ft.Icons.SENTIMENT_SATISFIED_SHARP,
    ft.Icons.SENTIMENT_VERY_SATISFIED_SHARP
]