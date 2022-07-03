#!/usr/bin/env python

import sys

from get_page import get_page                            # 自作
from extract_texts import extract_texts                  # 自作
from tokenize_texts import tokenize_texts                # 自作

'''
入力された単語のリストから、それらの頻度を計算し、(単語, 頻度) タプルのリストを返す。
'''

def calc_probs(tokens):
    # リストのサイズ
    size = len(tokens)

    # 単語の重複のないリストを作成
    unique_tokens = list(set(tokens))

    # 単語:頻度 の辞書を作成
    prob = {key:tokens.count(key)/size for key in unique_tokens}

    return prob


if __name__ == '__main__':
    url = sys.argv[1]
    html = get_page(url)
    texts = extract_texts(html)
    tokens = tokenize_texts(texts)
    probs = calc_probs(tokens)
    print(probs)
