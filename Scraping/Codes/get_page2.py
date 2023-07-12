#!/usr/bin/env python

import sys
import requests

'''
指定の URL の HTML テキスト (str) を取得する。
HTTP のレスポンスコードが 200 OK でなければ None を返す。
'''

print(__name__)

def get_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'                     # Content-Type: がないときのため
    if response.status_code != 200:
    	return None

    return response.text

'''
if __name__ == '__main__':
    url = sys.argv[1]                               # コマンドライン引数から URL を指定
    html = get_page(url)
    print(html)
'''