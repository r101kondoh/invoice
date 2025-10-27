import flet as ft
from logging import getLogger

from utils.file_utils import FileUtils
my_logger = getLogger()

class ReceiptImage(ft.Column):
    """
    レシート画像
    """
    def __init__(self, path:str, row_images:ft.Ref[ft.Row], idx:int):
        super().__init__()
        self.idx = idx
        self.path = path
        self.row_images = row_images
        self.lbl_file_name = ft.Ref[ft.Text]()
        self.txt_file_name = ft.Ref[ft.TextField]()
        self.btn_edit = ft.Ref[ft.IconButton]()
        self.img = ft.Ref[ft.Image]()
        self.controls=[
            ft.Text(path.split('\\')[1], ref=self.lbl_file_name),
            ft.TextField(path.split('\\')[1], visible=False, ref=self.txt_file_name, text_size=14, width=160, height=20, content_padding=4),
            ft.Image(
                src=path,
                ref=self.img,
                width=200,
                height=400,
                fit=ft.ImageFit.FILL,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            ft.IconButton(icon=ft.Icons.EDIT, ref=self.btn_edit, on_click= lambda _ :self.edit())
        ]
    
    def edit(self):
        '''
        編集
        '''            
        self.lbl_file_name.current.visible = not self.lbl_file_name.current.visible
        self.txt_file_name.current.visible = not self.txt_file_name.current.visible
        if not self.txt_file_name.current.visible:
            new_path = self.path.replace(self.lbl_file_name.current.value, self.txt_file_name.current.value)
            my_logger.info(new_path)
            FileUtils.rename(self.path, new_path)
            self.lbl_file_name.current.value = self.txt_file_name.current.value
            self.path = new_path
            self.img.current.src = new_path
            self.img.current.update()

        self.lbl_file_name.current.update()
        self.txt_file_name.current.update()

        for img in self.row_images.current.controls:
            img: "ReceiptImage"
            if img.idx != self.idx:
                img.btn_edit.current.disabled = not self.lbl_file_name.current.visible
                img.btn_edit.current.update()
