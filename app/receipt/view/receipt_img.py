from typing import Callable
import flet as ft
from logging import getLogger

from utils.error_handlers import handle_errors
from utils.file_utils import FileUtils
my_logger = getLogger()

class ReceiptImage(ft.Column):
    """
    レシート画像
    """
    def __init__(self, path:str, row_images:ft.Ref[ft.Row], idx:int, upd_imgs:Callable[[], None]):
        super().__init__()
        self.idx = idx
        self.path = path
        self.upd_imgs = upd_imgs
        self.row_images = row_images
        self.lbl_file_name = ft.Ref[ft.Text]()
        self.txt_file_name = ft.Ref[ft.TextField]()
        self.btn_edit = ft.Ref[ft.IconButton]()
        self.btn_delete = ft.Ref[ft.IconButton]()
        self.img = ft.Ref[ft.Image]()
        self.controls=[
            ft.Text(path.split('\\')[1], ref=self.lbl_file_name),
            ft.TextField(path.split('\\')[1].replace(".png", ""), suffix_text=".png", visible=False, ref=self.txt_file_name, text_size=14, width=160, height=20, content_padding=4),
            ft.Image(
                src=path,
                ref=self.img,
                width=150,
                height=300,
                fit=ft.ImageFit.FILL,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.EDIT, ref=self.btn_edit, on_click= lambda _ :self.edit()),
                    ft.IconButton(icon=ft.Icons.DELETE, ref=self.btn_delete, on_click= lambda _ :self.delete()),
                ]
            )
        ]
    
    @handle_errors
    def edit(self):
        '''
        編集
        '''            
        self.lbl_file_name.current.visible = not self.lbl_file_name.current.visible
        self.txt_file_name.current.visible = not self.txt_file_name.current.visible
        self.btn_delete.current.disabled = not self.btn_delete.current.disabled
        if not self.txt_file_name.current.visible:
            new_file_name = f"{self.txt_file_name.current.value}{self.txt_file_name.current.suffix_text}"
            new_path = self.path.replace(self.lbl_file_name.current.value, new_file_name)
            FileUtils.rename(self.path, new_path)
            self.lbl_file_name.current.value = new_file_name
            self.path = new_path
            self.img.current.src = new_path
            self.img.current.update()

        self.lbl_file_name.current.update()
        self.txt_file_name.current.update()
        self.btn_delete.current.update()

        for img in self.row_images.current.controls:
            img: "ReceiptImage"
            if img.idx != self.idx:
                img.btn_edit.current.disabled = not self.lbl_file_name.current.visible
                img.btn_edit.current.update()
                img.btn_delete.current.disabled = not img.btn_delete.current.disabled
                img.btn_delete.current.update()

    @handle_errors
    def delete(self):
        '''
        削除処理
        '''
        FileUtils.del_file(self.path)
        self.upd_imgs()
        


