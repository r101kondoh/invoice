import tkinter as tk
import tkinter.messagebox as msgbox

class MyMsgBox():
    """
    メッセージボックス
    """
    def show_msgbox(title:str, msg:str):
        '''
        メッセージボックスを表示する
        '''
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        msgbox.showinfo(title, msg)
        root.destroy()

    def show_errmsgbox(title:str, msg:str):
        '''
        エラーメッセージボックスを表示する
        '''
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        msgbox.showerror(title, msg)
        root.destroy()
