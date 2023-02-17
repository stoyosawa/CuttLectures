## ページの取得

指定のURLのHTMLデータ（text/html）を取得するには、[`requests`](https://requests.readthedocs.io/)パッケージを利用します。

`requests`は、HTTPアクセスに頻繁に利用されるパッケージです。Python本体に備わっている[`http.client`](https://docs.python.org/ja/3/library/http.html)や[`socket`](https://docs.python.org/ja/3/library/socket.html)でも同じ目的を達成できますが、`requests`の方が簡単にHTTPクライアントを構成できます。


### とりあえず試そう

スクリプトは[`get_page.py`](./Codes/get_page.py "CODE")です。次のように、コマンドラインからURLを指定して実行すれば、標準出力にHTMLテキストを表示します。

```
C:\temp>python get_page.py https://www.cutt.co.jp/
<!DOCTYPE html>
<html lang="ja">

  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="keywords" content="CUTT System,カットシステム,コンピュータ書,出版,新刊案内">
  <title>株式会社カットシステム</title>
  <link rel="stylesheet" href="CSS/1807toppage.css" type="text/css">
  <script src="showprice.js"></script>
</head>
︙
```

以下、スクリプトの中身を説明します。


### パッケージのインポート

利用に際しては、まずパッケージをインポートします。

```Python
>>> import requests
```


### Webアクセス

`requests`の`get()`メソッドの引数にURL文字列を指定するだけでWebデータがダウンロードできます。

```Python
>>> response = requests.get('https://www.cutt.co.jp')    # request.Responseオブジェクトが返る
```

`requests.get()`は`requests.Response`オブジェクトを返します。この中には目的とするHTMLデータの他、HTTPヘッダやレスポンスステータスコードなどの制御情報が収容されています。


### 文字化け対策

`requests`が文字コードを検出できないときのため、UTF-8を強制しておきます（詳細は割愛）。

```Python
>>> response.encoding = 'utf-8'
```


### アクセスの成否の確認

HTTPサーバは、要求したHTMLデータと共に、その要求が成功したか否かを示す[ステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status "LINK")を返します。`200`なら成功です。

ステータスコードは`requests.Response`オブジェクトの`status_code`属性から確認できます。属性値は数値（`int`）です。

```Python
>>> response.status_code
200
```

200以外のケースでは（たいてい）目的のページが取得できていないので、（テキストではなく）`None`を返すようにします。


### HTML本体の取得

HTTPサーバが返すHTMLデータ本体（ボディ）は`requests.Response`オブジェクトの`text`属性から入手できます。属性値は文字列（`str`）です。

長いので、次の用例では最初の100文字だけを表示します。

```Python
>>> type(response.text)
<class 'str'>
>>> response.text[:100]
'<!DOCTYPE html>\n<html lang="ja">\n\n  <head>\n  <meta charset="utf-8">\n  <meta name="viewport" content='
```


### 次号へ続く

[`get_page.py`](./Codes/get_page.py "CODE")は、引数に指定したURLのHTMLデータを取得する`get_page()`関数と、それをテストする`main`関数で構成されています。以降でこの関数を利用するには、次のようにインポートします。

```Python
from get_page import get_page
```
