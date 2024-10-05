#!/usr/bin/env python

import re
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs

from get_page import get_page                       # 自作

'''
HTMLテキストデータから文章だけを抜き出し、行単位にばらす。
空白行や前後にある余分なスペースは除く。
'''

def extract_texts(html):
    texts = []
    soup = bs(html, 'html.parser')
    text = soup.get_text()

    # 行単位でリストにばらす
    texts = text.splitlines()

    # カラあるいは空白だけの要素は除く
    regexp = re.compile(r'^\s*$')
    texts = [text for text in texts if regexp.search(text) is None]

    # 行の前後にあるスペースも除く
    texts = [text.strip() for text in texts] 

    return texts


if __name__ == '__main__':
    url = sys.argv[1]
    html = get_page(url)
    texts = extract_texts(html)
    print('\n'.join(texts))
