#!/usr/bin/env python

import string
import sys
from janome.tokenizer import Tokenizer

from get_page import get_page                            # 自作
from extract_texts import extract_texts                  # 自作

'''
入力されたテキストのリストを単語（形態素）に分解し、そこから名詞だけを抜き出す。
'''

def tokenize_texts(texts):
    token_objs = []                                      # Tokenオブジェクト収容用

    t = Tokenizer()
    for text in texts:
        objs = t.tokenize(text)
        token_objs.extend(objs)    

    # 名詞の単語だけを抜き出す
    tokens = [token.surface for token in token_objs if token.part_of_speech.startswith('名詞')]

    # 1文字しかない語は除く
    tokens = [token for token in tokens if len(token) > 1]

    # 数字は抜く
    tokens = [token for token in tokens if token.isnumeric() is False]

    return tokens


if __name__ == '__main__':
    url = sys.argv[1]
    html = get_page(url)
    texts = extract_texts(html)
    tokens = tokenize_texts(texts)
    print(tokens)
