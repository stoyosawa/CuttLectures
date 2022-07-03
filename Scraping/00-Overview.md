## 概要

作業手順は次の通りです。括弧は使用するパッケージを示します。

<img src="./Images/procedure.png" width="300">

それぞれのステップは1本のスクリプトで構成します。


### ページの取得

指定のURL（たとえば`https://www.cutt.co.jp/`）にアクセスし、ページのHTMLデータを取得します。これには、`requests`パッケージを用います。

![Deliverable](./Images/deliverable.png)  
・このステップで得られるのは、UTF-8でエンコードされたHTMLデータ（`str`）です。  
・スクリプトは[`get_pege.html`](./Codes/short_version/get_page.py "CODE")です。


### テキストの取得

HTMLデータからHTMLタグなどを外し、テキスト（ブラウザ上に見える文章）だけを抽出します。これには`bs4`パッケージを用います。

得られたテキスト（巨大な1文字列）は行単位に分解し、空白だけの行や行前後にある空白は除きます。

![Deliverable](./Images/deliverable.png)  
・このステップで得られるのは、行単位のテキストのリスト（`['text1', 'text2', ..., 'textN']`）です。  
・スクリプトは[`extract_texts.py`](./Codes/short_version/extract_texts.py "CODE")です。


### 単語への分解

得られた文はそれぞれ単語（正確には形態素）に分解します。これには、[`janome`](https://mocobeta.github.io/janome/ "LINK")を用います。

`janome`は、たとえば「すもももももももものうち」を「すもも・も・もも・も・もも・の・うち」のように分解してくれます。また、それぞれに名詞や助詞といった品詞情報も加えてくれます。

```
>>> from janome.tokenizer import Tokenizer
>>> t = Tokenizer()
>>> for token in t.tokenize('すもももももももものうち'):
...     print(token)
...
すもも 名詞,一般,*,*,*,*,すもも,スモモ,スモモ
も    助詞,係助詞,*,*,*,*,も,モ,モ
もも  名詞,一般,*,*,*,*,もも,モモ,モモ
も    助詞,係助詞,*,*,*,*,も,モ,モ
もも  名詞,一般,*,*,*,*,もも,モモ,モモ
の    助詞,連体化,*,*,*,*,の,ノ,ノ
うち  名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
```
*[Janomeホームページ](https://mocobeta.github.io/janome/ "LINK")より*

ここでは、これら単語のうち名詞のもの、かつその単語長が2つ以上のものだけを抽出します。

![Deliverable](./Images/deliverable.png)  
・このステップで得られるのは、単語のリスト（`['word1', 'word2', ..., 'wordN']`）です。
・スクリプトは[`tokenize_texts.py`](./Codes/short_version/tokenize_texts.py "CODE")です。


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
