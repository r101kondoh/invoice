import pandas as pd
import os


def generate_dir():
    '''
    店舗一覧エクセルファイルのデータを基に、
    フォルダを自動で作成する関数
    '''

    # 1. 「店舗一覧」という親フォルダを作る
    #    exist_ok=True にすると、すでにフォルダがあってもエラーにならない
    base_dir = "./assets/店舗一覧"
    os.makedirs(base_dir, exist_ok=True)

    # 2. Excelファイルを読み込む
    #    pandas というライブラリを使って、表のデータをそのまま扱える
    df = pd.read_excel("./assets/店舗一覧.xlsx")
    
    # 3. Excel の各行（1店舗ごと）を順番に処理する
    for _, row in df.iterrows():

        # 3-1. フォルダ名を「ID_店舗名」という形で作る
        #      IDはゼロ埋めして4桁にする（例: 1 → 0001）
        folder_name = f"{row['ID']:04}_{row['店舗名']}"

        # 3-2. Excelに「店舗種別」が書かれている場合は、その名前でさらに階層を作る
        sub_dir = row["店舗種別"]
        if type(sub_dir) != str:  # 文字列じゃない場合はスキップ
            continue

        # 3-3. 実際に作るフォルダのパスを決める
        #      例: ./assets/店舗一覧/自社店舗/0007_薬院
        folder_path = os.path.join(base_dir, sub_dir, folder_name)

        # 3-4. フォルダを作成する（すでにあってもOK）
        os.makedirs(folder_path, exist_ok=True)
        print(f"作成完了: {folder_path}")


# Pythonファイルを直接実行したときだけ、generate_dir() を呼び出す
if __name__ == "__main__": 
    generate_dir()
