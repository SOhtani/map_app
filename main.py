import os
import random
import numpy as np
from PIL import Image
from skimage import io
import streamlit as st

# タイトル
st.title('航空写真タイル分類アプリ')

# 入力画像アップロード
st.write('## 入力画像をアップロード')
input_image = st.file_uploader('画像ファイルをアップロードしてください', type=['png', 'jpg', 'jpeg'])

# タイル数設定
st.write('## タイル数を設定')
num_tiles = st.slider('分割するタイルの数を設定してください', min_value=1, max_value=5000, value=1000)

# 緑色の閾値設定
st.write('## 緑色の閾値を設定')
green_threshold = st.slider('緑色の閾値を設定してください', min_value=0, max_value=255, value=70)

# 入力画像の表示
if input_image is not None:
    st.write('### 入力画像')
    img = Image.open(input_image)
    st.image(img, use_column_width=True)

    # 入力画像を読み込み
    img_array = np.array(img)

    # 入力画像のサイズ
    height, width, channels = img_array.shape

    # 1タイルあたりのサイズ
    tile_height = height // int(np.sqrt(num_tiles))
    tile_width = width // int(np.sqrt(num_tiles))

    # タイルを分類して保存
    sea_tiles = 0
    mountain_tiles = 0
    plain_tiles = 0
    for i in range(int(np.sqrt(num_tiles))):
        for j in range(int(np.sqrt(num_tiles))):
            x = j * tile_width
            y = i * tile_height
            tile = img_array[y:y+tile_height, x:x+tile_width]
            if np.mean(tile[:,:,0]) < np.mean(tile[:,:,1]) < np.mean(tile[:,:,2]):
                sea_tiles += 1
            else:
                if np.mean(tile[:,:,1]) > green_threshold:
                    plain_tiles += 1
                else:
                    mountain_tiles += 1

    # 各クラスターに分類されたタイル画像数の総タイル数における割合を表示
    total_tiles = sea_tiles + mountain_tiles + plain_tiles
    sea_ratio = sea_tiles / total_tiles * 100
    mountain_ratio = mountain_tiles / total_tiles * 100
    plain_ratio = plain_tiles / total_tiles * 100
    st.write(f"### 分類結果")
    st.write(f"Sea: {sea_ratio:.1f}%\nMountain: {mountain_ratio:.1f}%\nPlain: {plain_ratio:.1f}%")
else:
    st.warning('画像ファイルをアップロードしてください')
