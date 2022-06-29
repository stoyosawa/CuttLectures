#!/usr/bin/env python

#!/usr/bin/env python
# 2022-06-08: The crawler part separated from the other code.
# 2022-06-27: Bug fixed (soup may return None when extracting a.href)

import sys
import requests


def load_body(url):
    '''指定のurlのHTMLボディを取得する。200 OK でなければ例外を上げる。'''
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
    	return None

    return response.text


if __name__ == '__main__':
    url = sys.argv[1]
    texts = load_body(url)
    print(f'{len(texts)} charactes loaded. {texts[:100]}')