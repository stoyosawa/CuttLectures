# オープンデータの活用～GeoJSON + Python Plotly

### 目的

本ワークショップでは、[東京都 オープンデータカタログサイト](https://portal.data.metro.tokyo.lg.jp/)掲載の[オープンデータ](https://ja.wikipedia.org/wiki/オープンデータ)から地理情報（対象の緯度経度）を取得し、これを[Python Plotly](https://plotly.com/python/)を用いて地図上にマーキングします。

ワークショップでは、まず例を挙げながらデータ取得、解析、地図へのマーキングの方法を説明します。そのあと、受講者には好みの東京都GeoJSONデータを選んで、地図を作成してもらいます。

現在、東京都のデータセットには地理情報を収容した[GeoJSON](https://ja.wikipedia.org/wiki/GeoJSON)フォーマットのデータセットが41あります（提供元は港区、品川区、目黒区くらいだけですが）。

出力結果のサンプルは、書籍[『Webスクレイピング～Pythonによるインターネット情報活用術』](https://github.com/stoyosawa/ScrapingBook-public)（2023年8月）用に公開されている［出力例］の第11、12章から見ることができます。

> JSON形式のオープンデータを`jq`を使ってコマンドラインでカジュアルに確認したい方は、[オープンデータの活用～JSON + jqパーザ](../OpenData-Jq)を参照してください。



### 受講対象者

位置情報のオープンデータで何かできないかと考えている方。


### 前提

Pythonの基本、たとえば基本データ型、ループ、関数などは理解しているとして話を進めます。

内包表記（`[x**2 for x in range(10)]`の類）などちょっと凝った言語仕様やあまり使わない標準ライブラリは、必要に応じてその都度説明します。


### 使用するライブラリ

本ワークショップでは、次の2つの外部のパッケージを利用します。

1. Webアクセス用の[Requests](https://requests.readthedocs.io/en/latest/)。
2. グラフ描画の[Plotly Express](https://plotly.com/python/)。

自分の環境に用意がなければ、以下の要領でインストールしてください。

```
python -m pip install -U pip
pip install requests
pip install plotly
```

> PandasあるいはGeoPandasを使った方が楽なこともありますが、ここでは通常の操作でデータを整形します。

### 実習環境

Pythonが実行可能ならなんでもかまいません。講師は[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)を利用します。

```Python
$ python
Python 3.8.5 (default, Jul 28 2020, 12:59:40)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x = 'hello world'
>>> x
'hello world'
```

オンライン環境でもかまいませんが、前記の2つの外部パッケージが利用可能で、生成するHTMLをダウンロードあるいは表示できなければなりません。たとえば、[Google Colab](https://colab.google/)なら問題なく実行できます。


### 参考書籍

- 豊沢聡: 『[Webスクレイピング～Pythonによるインターネット情報活用術](https://www.cutt.co.jp/book/978-4-87783-541-5.html)』, カットシステム（2021年8月）

<img src="https://www.cutt.co.jp/book/images/978-4-87783-541-5.png" width="200">
