# Webスクレイピング

### 目的

本セミナーでは、[Webスクレイピング](https://ja.wikipedia.org/wiki/ウェブスクレイピング "LINK")とその視覚化を説明します。具体的には、指定のURLから、次のようにそのページの文章にある単語を散りばめた画像を生成するPythonスクリプトを作成します。

<img src="./Images/www_cutt_co_jp.png" width="400">  

*株式会社 カットシステムのトップページ`https://www.cutt.co.jp`より*

使用頻度が高い単語ほど大きく表示されます。これを[ワードクラウド](https://ja.wikipedia.org/wiki/タグクラウド "LINK")（word cloud）と呼びます。


### プログラム

90分お試し版は次のトピックを扱います。

- [概要](./00-Overview.md "INTERNAL")
- [インストール](./01-Install.md "INTERNAL")
- [ページの取得](./02-GetPage.md "INTERNAL")
- [テキストの取得](./03-ExtractTexts.md "INTERNAL")
- [単語への分解](./04-Tokenize.md "INTERNAL")
- [頻度のカウント](./05-CalcProbs.md "INTERNAL")
- [WordCloudの生成](./06-GenerateWc.md "INTERNAL")

<!---
フルバージョン（休み時間を入れて6時間）では上記に続いて次のトピックを説明します（TBD）。

- クローリング
- 選択単語の検討 ... janome の特定の品詞のフィルタリング
- アンカーの選択 ... bs4.find()
- 英文のスクレイピング ... NLTK
- janome、NLTK を用いた単語頻度計算
--->

### 使用言語

プログラミングにはPythonを用います。Webページアクセス、HTMLの解析、文章のまとめと語の頻度解析に次のパッケージを利用します。

- [requests](https://requests-docs-ja.readthedocs.io/en/latest/ "LINK") - Webアクセス（HTTPクライアント）
- [Beautiful Soup](http://kondou.com/BS4/ "LINK") - HTML解析（パーザー）。バージョン4は*bs4*と呼ばれる。
- [Janome](https://mocobeta.github.io/janome/ "LINK") - 文章解析（形態素解析）
- [WordCloud](http://amueller.github.io/word_cloud/ "LINK")（英のみ） - 単語リストからwordcloud画像を生成


### 環境

WindowsまたはUnix。UnixについてはWindowsから利用できる[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/ "LINK")も可です。

スクリプトの実行にはコンソール（Windowsならコマンドプロンプト）を使用します。


### 受講対象者

Python経験者

