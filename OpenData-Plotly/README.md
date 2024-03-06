# オープンデータの活用～Python Plotly

### 目的

本セミナーでは、[オープンデータ](https://ja.wikipedia.org/wiki/オープンデータ)から地理情報（対象の緯度経度）を取得し、これを[Python Plotly](https://plotly.com/python/)を用いて地図上にマーキングします。次の例は、東京都内のWiFiスポット位置データから生成した地図です。

<!-- 1034x779。「Webスクレイピング」本の第11章より。-->
<img src="Images/MapStyle_Watercolor.png" width="500">

◆お試し版セミナー（90分）ではデータ取得、解析、地図へのマーキングの方法を説明します。データ形式は、GeoJSONの`Point`タイプ形式だけを扱います。【[Sample](http://htmlpreview.github.io/?https://github.com/stoyosawa/CuttSeminars/blob/main/OpenData-Plotly/Samples/geo_points.html)】

◆ワークショップ（＋2時間）では続いてGeoJSONの`LineString`と`Polygon`を説明してから、好みの東京都GeoJSONデータを地図を作成してもらいます。


### 対象データ

[東京都 オープンデータカタログサイト](https://portal.data.metro.tokyo.lg.jp/)に掲載されている約6000件のデータのうち、地理情報（GeoJSONデータ）を収容した41件のデータセットを用います。


### 受講対象者

位置情報のオープンデータで何かできないかと考えている方。


### 前提

Pythonの基本、たとえば基本データ型、ループ、関数などは理解しているとして話を進めます。

内包表記（`[x**2 for x in range(10)]`の類）などちょっと凝った言語仕様やあまり使わない標準ライブラリは、必要に応じてその都度説明します。


### 使用するライブラリ

本ワークショップでは、次の2つの外部のパッケージを利用します。

1. Webアクセス用の[Requests](https://requests.readthedocs.io/en/latest/)。
2. グラフ描画の[Plotly Express](https://plotly.com/python/)。

用意がなければ、以下の要領でインストールしてください。

```
python -m pip install -U pip
pip install requests
pip install plotly
pip install pandas                          # Plotlyに必要
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


### 類似のセミナー

- 『[オープンデータの活用～JSON＋jqパーザ](../OpenData-Jq)』では、JSONデータ形式のオープンデータを対象に、コマンドラインからカジュアルにデータの中身をチェックする方法を示します。
- 『[Webスクレイピング～Python＋Janome＋Worldcloud](./Scraping/README.md)』では、インターネット上のHTMLページを対象に、PythonとWordcloudを使って、ページ中の単語を抽出したワードクラウドを作成します。


### 参考書籍

- 豊沢聡: 『[Webスクレイピング～Pythonによるインターネット情報活用術](https://www.cutt.co.jp/book/978-4-87783-541-5.html)』, カットシステム（2023年8月）。

<img src="https://www.cutt.co.jp/book/images/978-4-87783-541-5.png" width="200">
