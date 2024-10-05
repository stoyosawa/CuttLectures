#!/usr/bin/env python
# 2024-08-08: Created. (c) 2024 S. Toyosawa

import os
from pathlib import PurePath
import statistics
from PIL import Image, ImageOps

DIRECTORY = 'Data'
EXTENSIONS = ['.png', '.jpg']
OUTFILE = 'cats.gif'


def get_filenames(dir=DIRECTORY):
    files = [entry.path for entry in os.scandir(dir)]
    files = [f for f in files if PurePath(f).suffix.lower() in EXTENSIONS]
    return files


def get_images(paths):
    return [Image.open(path) for path in paths]


def get_optimal_size(imgs):
    width = statistics.median([img.width for img in imgs])
    height = statistics.median([img.height for img in imgs])
    return (width, height)


def resize_images(imgs, size, color):
    return [ImageOps.pad(img, size=size, color=color) for img in imgs]


def generate_apng(imgs, filename=OUTFILE, duration=500):
    imgs[0].save(
        fp=OUTFILE,                        # ファイル名
        append_images=imgs[1:],            # 以降の画像
        save_all=True,                     # アニメーションにする
        duration=duration,                  # 間隔（ミリ秒）
        loop=0
    )



if __name__ == '__main__':
    filenames = get_filenames()
    print(f'{len(filenames)} files found.')

    images = get_images(filenames)
    size = get_optimal_size(images)
    print(f'Resize to {size}')

    images = resize_images(images, size, (0, 0, 0))
    generate_apng(images)
