## ファイル名の生成

ファイル名を指定したURLのドメイン名から生成します。

### URLの分解

URLを[理解、分解、再構築](https://www.hagaren.jp/ "LINK")するには、標準ライブラリの[`urllib`の`parse`モジュール](https://docs.python.org/ja/3/library/urllib.parse.html "LINK")を用います。ここでは分解だけなので、その中から`urlparse`クラスを用います。インポートは次のように行います。

```Python
>>> from urllib.parse import urlparse
```

URLを分解するには、この`urlparse`クラスの引数にその文字列を指定するだけです。

```Python
>>> urlparse(url)
ParseResult(scheme='https', netloc='www.cutt.co.jp', path='/', params='', query='', fragment='')
```

ドメイン部分は`ParseResult`オブジェクトの`netloc`属性から得られます。

```Python
>>> domain = urlparse(url).netloc
>>> domain
'www.cutt.co.jp'
```

### 整形

ファイル名には、拡張子の区切り文字以外では`.`は使わない方が好ましいので、これをアンダースコア`_`に置き換えます。これには[`str.replace()`](https://docs.python.org/ja/3/library/stdtypes.html#string-methods "LINK")メソッドを使います。あとは、末尾に`.png`を加えるだけです。。

```Python
>>> domain = domain.replace('.', '_') + '.png'
>>> domain
'www_cutt_co_jp.png'
```
