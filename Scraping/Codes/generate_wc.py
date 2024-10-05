#!/usr/bin/env python

import sys
import wordcloud

from get_page import get_page                            # 自作
from extract_texts import extract_texts                  # 自作
from tokenize_texts import tokenize_texts                # 自作
from calc_probs import calc_probs                        # 自作

'''
(単語, 頻度) のタプルを収容したリストからワードクラウドを作成する。
ワードクラウド画像は URL のドメイン名部分のドット（.）をアンダースコア（_）に変えた名称をファイル名にして保存する。
'''

def generate_wc(probs, filename='img.png'):
    # ワードクラウドの生成
    wc = wordcloud.WordCloud(
            width=1024,
            height=768,
            font_path='/mnt/c/Windows/Fonts/UDDigiKyokashoN-R.ttc'
    )
    img = wc.fit_words(probs)
    img.to_file(filename)


if __name__ == '__main__':
    url = sys.argv[1]
    html = get_page(url)
    texts = extract_texts(html)
    tokens = tokenize_texts(texts)
    prob = calc_probs(tokens)
    generate_wc(prob)
