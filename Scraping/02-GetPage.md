## ページの取得

指定のURLのHTMLデータ（text/html）を取得するには、`requests`パッケージを利用します。

`requests`は、HTTPアクセスに頻繁に利用されるパッケージです。Python本体に備わっている[`http.client`](https://docs.python.org/ja/3/library/http.html)や[`socket`](https://docs.python.org/ja/3/library/socket.html)でも同じ目的を達成できますが、`requests`の方が簡単にHTTPクライアントを構成できます。


### パッケージのインポート

利用に際しては、まずパッケージをインポートします。

```Python
>>> import requests
```

### Webアクセス

`requests`の`get()`メソッドの引数にURL文字列を指定するだけでWebデータがダウンロードできます。

```Python
>>> url = 'https://www.cutt.co.jp/'                 # カットシステムのホームページ
>>> response = requests.get(url)                    # request.Responseオブジェクトが返る
```

`requests`にはPUTやPOSTなどの[HTTPメソッド](https://developer.mozilla.org/ja/docs/Web/HTTP/Methods "LINK")（コマンド）もありますが、データを取り込むだけのスクレイピングでは`get()`しか使いません。

`requests.get()`は`request.Response`オブジェクトを返します。この中には目的とするHTMLデータの他、HTTPヘッダやレスポンスステータスコードなどの制御情報が収容されています。

### アクセスの成否の確認


HTTPサーバは、要求したHTMLデータと共に、その要求が成功したか否かを示す[ステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status "LINK")を返します。`200`なら成功です。

ステータスコードは`requests.Response`オブジェクトの`status_code`属性から確認できます。属性値は数値（`int`）です。

```Python
>>> response.status_code
200
```

200以外のケースでは（たいてい）目的のページが取得できていないので、（後述の）スクリプトでは（テキストではなく）`None`を返すようにします。

### HTML本体の取得

HTTPサーバが返すHTMLデータ本体（ボディ）は`requests.Response`オブジェクトの`text`属性から入手できます。属性値は文字列（`str`）です。

長いので、次の用例では最初の100文字だけを表示します。

```Python
>>> type(response.text)
<class 'str'>
>>> response.text[:100]
'<!DOCTYPE html>\n<html lang="ja">\n\n  <head>\n  <meta charset="utf-8">\n  <meta name="viewport" content='
```

### 文字化け対策

`requests`は、受信テキストデータ（バイトストリーム）の文字エンコーディング方式を[HTTPヘッダ](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers "LINK")（`Content-type`）から推測します。不在の場合、たいて[ISO-8859-1](https://ja.wikipedia.org/wiki/ISO/IEC_8859-1 "LINK")（Latin-1文字）と解釈します。

次に、`https://www.cutt.co.jp/`にアクセスしたときのHTTPヘッダと最初の数行のHTMLページを示します。中身は`<meta>`タグに書かれているように[UTF-8](https://ja.wikipedia.org/wiki/UTF-8 "LINK")のはずですが、ヘッダにはそのことは書かれていません。

```
$ curl -D - https://www.cutt.co.jp/                      # HTTPヘッダも表示
HTTP/2 200
server: nginx
date: Thu, 30 Jun 2022 02:31:58 GMT
content-type: text/html                                  # charset=utf-8 がない
content-length: 31715
last-modified: Wed, 29 Jun 2022 07:38:43 GMT
etag: "7be3-5e2913e1126c0"
accept-ranges: bytes

<!DOCTYPE html>
<html lang="ja">

  <head>
  <meta charset="utf-8">                                 # <meta> には UTF-8 とある
  <meta name="viewport" content="width=device-width, initial-scale=1">
⋮
```

> [`curl`](https://curl.se/ "LINK")はコマンドラインで使用できるHTTPクライアントです。NetOpsなどネットワーキング関連のエンジニアに好んで用いられています。

`requests`が受信テキストをどの文字エンコーディング方式で解釈したかは、`encoding`属性から知ることができます。

```Python
>>> response.encoding
'ISO-8859-1'
```

本来はUTF-8であるテキストをISO-8859-1で解釈するため、受信データは文字化けします。 本文のあるところ（1,000から1,050文字まで）を抜粋してみます。

```Python
>>> response.text[1000:1050]
'ut/index.html">ã\x82«ã\x83\x83ã\x83\x88ã\x82·ã\x82¹ã\x83\x86ã\x83\xa0ã\x81«ã\x81¤ã\x81\x84ã\x81¦</'
```

文字化けに対処するには、`requests`に読み込んだテキストがUTF-8であることを明示的に指示します。これには、`encoding`属性を次のようにオーバーライトします。

```Python
>>> response.encoding = 'utf-8'
```

これで正確に表示されます。

```Python
>>> response.text[1000:1050]
'i><a href="tobookstore/tobookstore.html">書店の方へ</a>'
```

> 同じ1,000～1,080でも中身が異なるのは、文字列スライスが文字単位だからです。ISO-88859-1は1文字1バイトなので、指定範囲の先頭は1,000バイト目を指示しています。これに対しUTF-8は、（おおむね）1文字3バイトなので、先頭のバイト位置はずっとうしろです。

Shift-JISやISO-2022-JPで書かれたウェブページを強制的にUTF-8として読むと、やはり文字化けします。ページがShift-JISなら、`response.encoding = 'shift_jis'`としなければなりません。


### まとめ

以上をスクリプトファイルにまとめたものは、[get_page.py](./Codes/short_version/get_page.py "INTERNAL")に収容しました。引数に指定したURLのHTMLデータを取得する`get_page()`関数と、それをテストする`main`関数で含まれています。

以降でこの関数を利用するには、次のようにインポートします。

```Python
from get_page import get_page
```

コマンドプロンプトから（`main`から）実行するなら、引数にURLを指定します。

```
C:\temp>python get_page.py https://www.cutt.co.jp/
<!DOCTYPE html>
<html lang="ja">
︙
```
