from PIL import Image, ImageDraw, ImageFont


def generate_stamp(text: str, filename:str, font_path="C:/Windows/Fonts/msgothic.ttc"):
    '''
    電子員画像ファイルを作成する
    '''
    # 画像サイズと色
    size = 75
    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)


    # 円を描く（赤い丸）
    border_width = 4
    draw.ellipse((border_width, border_width, size - border_width, size - border_width), outline="red", width=border_width)


    # フォント設定
    font_size = 18
    font = ImageFont.truetype(font_path, font_size)

    text_height_total = font_size * len(text)
    start_y = (size - text_height_total) * 0.5
    x = size * 0.5

    for i, char in enumerate(text):
        y = start_y + i * font_size

        # テキストサイズを取得
        bbbox = draw.textbbox(xy=(0, 0), text=char, font=font)
        w = bbbox[2] - bbbox[0]
        h = bbbox[3] - bbbox[1]


        # 文字を描く（赤）
        draw.text((x-w*0.5, y), char, fill="red", font=font)

    # 保存
    image.save(filename)