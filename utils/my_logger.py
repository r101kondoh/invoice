from logging import getLogger, handlers, Formatter, StreamHandler, INFO, WARNING
import coloredlogs

def set_logger():
    '''
    全体のログ設定
    '''
    fmt = '%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s'
    root_logger = getLogger()
    coloredlogs.install(level="DEBUG",fmt=fmt)
    root_logger.setLevel(INFO)

    # ログをファイルに書き出す
    # ログが100KB溜まったらバックアップにして新しいファイルを作る
    rotating_handler= handlers.RotatingFileHandler(
        r'./assets/logs/app.log',
        mode="a",
        backupCount=3,
        encoding="utf-8"
    )
    
    rotating_handler.setFormatter(Formatter(fmt))
    rotating_handler.setLevel(WARNING)
    root_logger.addHandler(rotating_handler)

    # コンソールにログを表示
    # console_handler = StreamHandler()
    # console_handler.setFormatter(Formatter(fmt))
    # console_handler.setLevel(INFO)
    # root_logger.addHandler(console_handler)
