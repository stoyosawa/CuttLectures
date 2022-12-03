## テキストの取得

HTMLデータには、`<body></body>`などHTMLタグやJavaScriptコードが混入しています。HTMLデータからHTMLタグなどを外し、テキスト（ブラウザ上に見える文章）だけを抽出するには、[`bs4`](https://beautiful-soup-4.readthedocs.io/en/latest/ "LINL")パッケージを用います。

また、得られたテキスト（巨大な1文字列）は行単位に分解し、空白だけの行や行前後にある空白は除きます。


### とりあえず試そう

スクリプトは[`extract_texts.html`](./Codes/short_version/extract_texts.py "CODE")です。次のように、コマンドラインからURLを指定して実行すれば、標準出力にHTMLから抽出したテキスト文を表示します。

```
C:\temp>python extract_texts.py https://www.cutt.co.jp/
株式会社カットシステム
先端技術Academy
出版書籍一覧
教科書・教材カタログ
直販案内
︙
```

以下、スクリプトの中身を説明します。


### パッケージのインポート

利用に際しては、まずパッケージをインポートします。

Beautiful Soupのパッケージ名は（バージョン4なので）`bs4`です。いろいろ機能がありますが、テキスト文を取り出すだけなら、使うのは`BeautifulSoup`クラスだけです。打ち間違えやすい長いクラス名なので、インポート時に別名も付けましょう。

```Python
>>> from bs4 import BeautifulSoup as bs
```


### BautifulSoupオブジェクトの生成

まず、BeatifulSoupコンストラクタ（別名`bs`）から、処理対象となるHTMLデータ（以下では変数`html`）を表現するオブジェクトを生成します。

```Python
>>> soup = bs(html, 'html.parser')
```

第1引数にはHTMLテキスト（変数`html`に代入されているとします）を、第2引数にはそのテキストの解析方法（パーザライブラリ）を指定します。`html.prarser`はHTMLを対象とした解析ライブラリです（他にXMLなどがある）。

戻り値は`bs4.BeautifulSoup`オブジェクトです。

```Python
>>> type(soup)
<class 'bs4.BeautifulSoup'>
```


### テキストの抽出

`bs4.BeautifulSoup`オブジェクトからテキストだけを抽出するには、`get_text()`メソッドを用います。

```Python
>>> html                                                 # HTMLタグ混じり
'<!DOCTYPE html>\n<html lang="ja">\n\n  <head>\n  <meta charset="utf-8">\n  <meta name="viewport" ...'

>>> text = soup.get_text()                               # テキストだけ
>>> text
'\n\n\n\n\n\n株式会社カットシステム\n\n\n\n\n\n\n\n\n\n\n先端技術Academy\n\n出版書籍一覧\n\n教科書・教材カタログ\n...'
```


### テキストの整形

テキストには空行（`\n`だけ）や余分なスペースが混入しています。読みやすくするため、次の3ステップで整形します。余分な記号は後述の単語分割等の処理には直接影響しませんが、出力チェック時に読みやすくなります。

##### 改行記号から行単位に分割

これには、標準ライブラリの[`str.splitlines()`](https://docs.python.org/ja/3/library/stdtypes.html#str.splitlines "LINK")を用います。文字列のリストが得られます。

```Python
>>> texts = text.splitlines()
```

確認のため、得られた行数と100番目の行の中身をチェックします。

```Python
>>> len(texts)                                           # 445行ある
445
>>> texts[100]                                           # 100行目
'3月28日発売'
```

##### 空行を省く

空行は何も書かれていない、あるいはスペースだけの行です。省くには、正規表現関数の[`re.search()`](https://docs.python.org/ja/3/library/re.html#re.search "LINK")を用います。

先頭（`^`）から末尾（`$`）までがすべて空白文字あるいは何もない（`\s*`）行を表現する正規表現は`^\s*$`です。これを`re.search()`から各行にあてはめ、`None`が返ってくれば（つまり、そのようなパターンが見当たらない）それが、保持しておくべき行です。

```Python
>>> import re                                            # 正規表現をインポート
>>> regexp = re.compile(r'^\s*$')                        # 正規表現を用意
>>> texts = [text for text in texts if regexp.search(text) is None]
>>> len(texts)
207
```

207行に減りました。

##### 前後の空白を除去

前後に余分な空白がある行もあります。

```Python
>>> texts[203]                                           # 先頭に余分な空白
'      C#ベクトルプログラミング入門」、新刊「統計処理に使うExcel 2021活用法」の案内を掲載しました。'
>>> texts[195]                                           # 後尾に余分な空白
'既刊書『HTML5 ＆ CSS3ワークブック 第2版』...（2020/04/13）                '
```

文字列の前後の空白を省くには[`str.strip()`](https://docs.python.org/ja/3/library/stdtypes.html#str.strip "LINK")を用います。

```Python
>>> texts = [text.strip() for text in texts]
>>> texts[203]
'C#ベクトルプログラミング入門」、新刊「統計処理に使うExcel 2021活用法」の案内を掲載しました。'
>>> texts[195]
'既刊書『HTML5 ＆ CSS3ワークブック 第2版』...（2020/04/13）'
```


### 次号へ続く

[extract_texts.py](./Codes/short_version/extract_texts.py "INTERNAL")は、引数に指定したHTMLデータ（`str`）を取得する`extract_texts()`関数と、それをテストする`main`関数で構成されています。以降でこの関数を利用するには、次のようにインポートします。

```Python
from extract_texts import extract_texts
```
