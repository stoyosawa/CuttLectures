# Webスクレイピング

### 目的

本セミナーでは、[Webスクレイピング](https://ja.wikipedia.org/wiki/ウェブスクレイピング "LINK")とその視覚化を説明します。具体的には、指定のURLのページにある単語を、出現頻度に応じたサイズで散りばめた画像を生成します。

<img src="./Images/www_cutt_co_jp.png" width="400">  

これを[ワードクラウド](https://ja.wikipedia.org/wiki/タグクラウド "LINK")（word cloud）と言います。


### 使用言語

プログラミングには[Python](https://www.python.org/ "LINK")を用います。Webページアクセス、HTMLの解析、文章のまとめと語の頻度解析に次のパッケージを利用します。

- [requests](https://requests-docs-ja.readthedocs.io/en/latest/ "LINK") - Webアクセス（HTTPクライアント）
- [Beautiful Soup](http://kondou.com/BS4/ "LINK") - HTML解析（パーザー）。バージョン4は*bs4*と呼ばれる。
- [Janome](https://mocobeta.github.io/janome/ "LINK") - 文章解析（形態素解析）
- [WordCloud](http://amueller.github.io/word_cloud/ "LINK")（英のみ） - 単語リストからwordcloud画像を生成


### 環境

WindowsまたはUnix。UnixについてはWindowsから利用できる[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/ "LINK")も可です。

スクリプトの実行にはコンソール（Windowsならコマンドプロンプト）を使用します。

オンラインのPython環境（Google Colabや`replit.com`など）でも構いませんが、1）外部パッケージをインストールできる、2）生成した画像を表示できる、あるいはダウンロードできる、ものでなければなりません。


### 受講対象者

Python経験者。

本セミナーで用いるやや凝ったテクニックにリスト内包表記、辞書内包表記、正規表現がありますが、前者2つについてはループの簡易表記、後者についてはパターンによる文字列操作だと思って読み飛ばしてください。
