## Webページのダウンロード

所定のURLのHTMLデータ（text/html）を取得するには`requests`パッケージを利用します。

`requests`はデフォルトで本体に組み込むべきだとの語論のあるくらい、広範囲に用いられるポピュラーなパッケージです。Python本体に備わっている[`http.client`](https://docs.python.org/ja/3/library/http.html)や[`socket`](https://docs.python.org/ja/3/library/socket.html)で同じことを達成できないこともありませんが、`requests`を用いた方が簡単にHTTPクライアントを構成できます。

[オンラインマニュアル](https://requests.readthedocs.io/ "LINK")は`https://requests.readthedocs.io/`にあります。

利用に際しては、まずモジュールをインポートします。

```Python
>>> import requests
```

### Webアクセス

`get()`メソッドの引数にURL文字列を指定して、その中身をダウンロードします。

```Python
>>> url = 'https://www.cutt.co.jp/'                      # カットシステムのホームページ
>>> response = requests.get(url)
```

`requests`にはPUTやPOSTなどの[HTTPメソッド](https://developer.mozilla.org/ja/docs/Web/HTTP/Methods "LINK")（コマンド）が用意されていますが、データを取り込むだけのスクレイピングでは`get()`しか使いません。

`requests.get()`は`request.Response`オブジェクトを返します。この中には目的とするHTMLデータの他にも、HTTPヘッダやレスポンスステータスコードなどの制御情報が収容されています。

### アクセスの成否の確認


HTTPサーバは、要求したHTMLデータと共に、その要求が成功したか否かを示す[レスポンスステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status "LINK")を返します。`200`なら成功です。それ以外のケースでは目的のページが取得できていません。

レスポンスステータスコードは`requests.Response`オブジェクトの`status_code`属性から確認できます。属性値は数値（`int`）です。

```Python
>>> response.status_code
200
```

### HTML本体（ボディ）の取得

HTTPサーバが返すHTMLデータ本体は`requests.Response`オブジェクトの`text`属性から入手できます。属性値は文字列（`str`）です。

長いので、スライスで最初の100文字だけを表示します。

```Python
>>> type(response.text)
<class 'str'>
>>> response.text[:100]
'<!DOCTYPE html>\n<html lang="ja">\n\n  <head>\n  <meta charset="utf-8">\n  <meta name="viewport" content='
```

### 文字化けするときは

受信したテキストデータの実際の文字エンコーディングが、`requests`あるいはPythonが想定したものと異なるときは、文字化けが生じます。

たとえば、ShiftJISで書かれたHTMLファイルを読み込み、それを`requests`がutf-8と勘違いして解釈すると次のようになります。

```Python
>>> url_sjis = 'https://raw.githubusercontent.com/stoyosawa/CuttSeminars/main/Scraping/Codes/shift_jis.html'
>>> sjis = requests.get(url_sjis)
>>> sjis.text
'<html>\n<meta http-equiv="content-type" content="text/html; charset=shift_jis">\n<body bagcolor="aquamarine">\n<p>���{�ꂪ Shift-JIS �ŏ�����Ă��܂��B</p>\n</body>\n</html>'
```

`request`が読み込んだデータをどのように解釈しているかは、`requests.Response`オブジェクトの`encoding`属性から知ることができます。

```Python
>>> sjis.encoding
'utf-8'
```

ここでは、utf-8と勘違いしているようです。

そこで、`encoding`をオーバーライトすることで、データがShiftJISであることを伝えます。

```Python
>>> sjis.encoding = 'shift_jis'
>>> sjis.text
'<html>\n<meta http-equiv="content-type" content="text/html; charset=shift_jis">\n<body bagcolor="aquamarine">\n<p>日本語が Shift-JIS で書かれています。</p>\n</body>\n</html>'
```

### まとめ

以上、URLからWebページを取得する操作を関数にまとめ、1本のスクリプトファイルにすると[downloader.py](./Codes/downloader.py "INTERNAL")のようになります（文字化け対処部分はUTF-8を想定しているので加えてありません）。


