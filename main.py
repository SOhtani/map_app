import os
import random
import numpy as np
from PIL import Image
from skimage import io
import streamlit as st

# タイトルと説明
st.title('Google mapの航空写真をスクリーンショットしてアップロードしてみよう！')
st.write('このアプリは、アップロードされた航空写真を分割して、海、山、平地の画像をクラスタリングし、それぞれの割合を表示します。')

# 入力画像アップロード
st.write('## 入力画像をアップロード')
input_image = st.file_uploader('画像ファイルをアップロードしてください', type=['png', 'jpg', 'jpeg'])

# タイル数設定
st.write('## タイル数を設定')
st.write('推奨は1000ですが、結果に応じて調整してください')
num_tiles = st.slider('分割するタイルの数を設定してください', min_value=1, max_value=5000, value=1000)

# 緑色の閾値設定
st.write('## 緑色の閾値を設定')
st.write('推奨は70ですが、結果に応じて調整してください')
green_threshold = st.slider('緑色の閾値を設定してください', min_value=0, max_value=255, value=70)

# 入力画像の表示
if input_image is not None:
    st.write('### 入力画像')
    img = Image.open(input_image)
    st.image(img, use_column_width=True)

    # 入力画像を読み込み
    img_array = np.array(img)

    # アルファチャンネルが存在する場合、削除
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]


    # 入力画像のサイズ
    height, width, channels = img_array.shape

    # 1タイルあたりのサイズ
    tile_height = height // int(np.sqrt(num_tiles))
    tile_width = width // int(np.sqrt(num_tiles))

    # タイルを分類して保存
    sea_tiles = 0
    mountain_tiles = 0
    plain_tiles = 0
    mask_array = np.zeros((height, width, channels), dtype=np.uint8)
    for i in range(int(np.sqrt(num_tiles))):
        for j in range(int(np.sqrt(num_tiles))):
            x = j * tile_width
            y = i * tile_height
            tile = img_array[y:y+tile_height, x:x+tile_width]
            if np.mean(tile[:,:,0]) < np.mean(tile[:,:,1]) < np.mean(tile[:,:,2]):
                sea_tiles += 1
                mask_array[y:y+tile_height, x:x+tile_width] = [0, 0, 255]  # Blue for sea
            else:
                if np.mean(tile[:,:,1]) > green_threshold:
                    plain_tiles += 1
                    mask_array[y:y+tile_height, x:x+tile_width] = [255, 0, 0] # Green for plain
                else:
                    mountain_tiles += 1
                    mask_array[y:y+tile_height, x:x+tile_width] = [0, 255, 0] # Red for mountain

    # 各クラスターに分類されたタイル画像数の総タイル数における割合を表示
    total_tiles = sea_tiles + mountain_tiles + plain_tiles
    sea_ratio = sea_tiles / total_tiles * 100
    mountain_ratio = mountain_tiles / total_tiles * 100
    plain_ratio = plain_tiles / total_tiles * 100
    st.write('## 結果')
    st.markdown(f'アップロードされた写真の中に...')
    st.write(f'## 海は **{sea_ratio:.1f}%**、山は **{mountain_ratio:.1f}%**、平地は **{plain_ratio:.1f}%** 含まれます。')

    # 可視化された分類画像を表示
    st.write('### 分類されたタイルの可視化')
    alpha = 0.5  # 透明度を設定 (0: 完全に透明, 1: 完全に不透明)
    overlay_array = img_array.copy()
    overlay_array[mask_array != 0] = (alpha * img_array + (1 - alpha) * mask_array)[mask_array != 0]
    overlay_img = Image.fromarray(overlay_array)
    st.image(overlay_img, use_column_width=True)


else:
    st.warning('画像ファイルをアップロードしてください')
