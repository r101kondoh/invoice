import os
import numpy as np
import cv2
from logging import getLogger

from utils.error_handlers import handle_errors
my_logger = getLogger()


class ReceiptExtracter():
    """
    レシート領域検出器
    """
    def __init__(self):
        # 赤色範囲（赤は2つの範囲に分かれる）
        self.lower_red1 = np.array([0, 100, 100])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([160, 100, 100])
        self.upper_red2 = np.array([179, 255, 255])

    @handle_errors
    def template_matching(self, input_path:str, template_path:str):
        '''
        テンプレートマッチング
        '''
        template = cv2.imread(template_path, 0)
        
        threshold = 0.8

        for file_name in os.listdir(input_path):
            found = False
            if file_name.endswith('.png'):
                my_logger.info(f"{file_name}の処理実行中...")
                
                img_path = os.path.join(input_path, file_name)
                my_logger.info(img_path)
                success_path = os.path.join("./output/receipt/img/matching/success", file_name)
                failed_path = os.path.join("./output/receipt/img/matching/failed", file_name)

                # 画像ファイルの読み込み
                img_rgb_orig = cv2.imread(img_path)
                # 0°, 90°, 180°, 270° の4回ループ

                for i in range(4):
                    angle = i * 90
                    # 画像を回転
                    if i == 0:
                        img_rgb = img_rgb_orig.copy()
                    else:
                        # cv2.rotate で簡単に90°単位で回転可能
                        img_rgb = cv2.rotate(img_rgb, cv2.ROTATE_90_CLOCKWISE)

                    # グレースケール化
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

                    # # エッジ検出（テンプレートと同条件で）
                    # img_edge = cv2.Canny(img_gray, 50, 150)
                    # template_edge = cv2.Canny(template, 50, 150)

                    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
                    template_blur = cv2.GaussianBlur(template, (3, 3), 0)

                    # テンプレートマッチング
                    res = cv2.matchTemplate(img_blur, template_blur, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)

                    if len(loc[0]) > 0:
                        my_logger.info(f"✅ テンプレートが検出されました（回転 {angle}°）")
                        t_w, t_h = template.shape[::-1]
                        
                        # 検出枠を描画
                        for pt in zip(*loc[::-1]):
                            cv2.rectangle(img_rgb, (pt[0] - int(0.5*t_w), pt[1] - t_h*6), (pt[0] + int(6.5*t_w), pt[1] + 14*t_h), (0, 0, 255), 2)

                        # BGR → HSV変換
                        hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

                        # 赤色マスク
                        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
                        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
                        mask_red = cv2.bitwise_or(mask1, mask2)

                        # 輪郭抽出
                        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        # 最大輪郭を選ぶ（面積で判定）
                        if contours:
                            c = max(contours, key=cv2.contourArea)
                            x, y, w, h = cv2.boundingRect(c)
                            my_logger.info(f"トリミング座標: x={x}, y={y}, w={w}, h={h}")

                            # トリミング
                            cropped = img_rgb[y:y+h, x:x+w]

                            # 保存
                            cv2.imwrite(success_path, cropped)
                            my_logger.info("✅ トリミング画像を保存しました")

                        else:
                            # 結果を保存
                            cv2.imwrite(success_path, img_rgb)
                            my_logger.info(f"🔹 マッチした画像を保存しました")
                        found = True
                        break  # マッチしたらループ終了

                if not found:
                    my_logger.error("⚠ テンプレートは4方向とも検出されませんでした")
                    cv2.imwrite(failed_path, img_rgb)