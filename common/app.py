class App:
    """
    配置するアプリ
    """
    def __init__(self, app, url:str, title:str, icon, icon_outlined, hidden_flg=False):
        self.app = app
        self.url = url
        self.title = title
        self.icon = icon
        self.icon_outlined = icon_outlined
        self.hidden_flg = hidden_flg