## はじめに

本セミナーでは、それぞれのタスクにスクリプトを用意し、これらを連係することで指定のURLからワードクラウド画像を生成します。タスクとその手順は次の通りです。

<img src="./Images/procedure.png" width="500">

括弧に示したのは、それぞれのステップで利用するパッケージ名と作成するスクリプト名です。

矢印で示したのは、それぞれのスクリプトの入力と出力です。たとえば、ページを取得する`get_page.py`はURL（文字列）を受け、HTMLデータ（文字列）を返します。そして、次段の`extract_texts.py`はHTMLデータ（文字列）を受け、テキスト（画面上に現れるヒトが読む文章）のリストを返します。最後のスクリプトが、ワードクラウド画像をファイルとして（`img.png`）を保存します。


### Pythonパッケージのインストール

Pythonはすでにインストールしてあるとして、本セミナーで利用する4つのパッケージを以下の要領でインストールします。

```
python -m pip install -U pip
pip install requests
pip install beautifulsoup4
pip install janome
pip install wordcloud
```

インストールの詳細は[付録A](./A-Install.md "LINK")を参照してください。


### 本セミナーのスクリプトのダウンロード

5本のスクリプトは[./Codes/short_version/wc.zip](./Codes/short_version/wc.zip "CODE")にZIPでまとめてあります。ダウンロードして、展開してください。


### とりあえず試そう

では、スクリプトを試してみましょう。次の要領で実行します。

```
$ python generate_wc.py https://www.cutt.co.jp/
```

非常にシンプルなスクリプトなので、URLによっては思ったように動作しないかもしれません。


### 頻度のカウント

ワードクラウド生成ライブラリが受け付けるデータは単語をキー、その出現頻度を値とした辞書なので、それを生成します。頻度は［単語の個数］÷［全語数］です（0＜p＜1）。単語リストから要素をカウントするだけなので、Pythonの標準機能だけで達成できます。

![Deliverable](./Images/deliverable.png)  
・{単語: 頻度}の辞書（`{'word1':p1, 'word2':p2, ..., 'wordN':pN}}`）です。  
・スクリプトは[`calc_probs.py`](./Codes/short_version/calc_probs.py "CODE")です。


### WordCloudの生成

上記で得た単語頻度辞書をもとにワードクラウド画像を生成します。これには、`wordcloud`パッケージを用います。

画像ファイル名は指定のURLのドメイン名のドットをアンダースコアに変えたものとします（e.g., `https://www.cutt.co.jp/` > `www_cutt_co_jp.png`）。

![Deliverable](./Images/deliverable.png)  
・このステップで得られるのは、最初のステップで指定したURLのページの中身のワードクラウド画像です。  
・スクリプトは[`generate_wc.py`](./Codes/short_version/generate_wc.py "CODE")です。
