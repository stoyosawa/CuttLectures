#!/usr/bin/env python

import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs
from get_page import get_page                            # 「トップページの取得」より

'''
HTMLボディからアンカー <a> を抽出し、その href 属性を抜き出す。
対象はローカルリンクだけ。これらは、指定の URL を使って https:// から始まるフル URL に変換する。
'''

def extract_anchors(html, url):
    links = []
    soup = bs(html, 'html.parser')

    # <a>をすべて抜き出す
    a_tags = soup.find_all('a')

    # アンカーオブジェクトから href 属性を抜き出す
    anchors = [a.get('href') for a in a_tags]

    # href がないとき、a.get() は None を返すので、それらを除去する
    anchors = [a for a in anchors if type(a) == str]

    # scheme のある URL は外部リンクであるとして、それらは省く
    anchors = [a for a in anchors if urlparse(a).scheme == '']

    # 引数で指定したトップページの url からフル URL を構築する
    anchors = [urljoin(url, urlparse(a).path) for a in anchors]

    # 重複を取り除く
    anchors = sorted(list(set(anchors)))

    return anchors


if __name__ == '__main__':
    url = sys.argv[1]
    html = get_page(url)
    anchors = extract_anchors(html, url)
    print(f'{len(anchors)} links found.')
    print('\n'.join(anchors))

