## 単語への分解

ワードクラウドを生成するには、文章を単語単位に分解しなければなりません。これには、[`janome`](https://mocobeta.github.io/janome/ "LINK")パッケージを利用します。ちなみにミシンではなく、[「蛇（パイソン）の眼」](https://mocobeta.github.io/janome/#id17 "LINK")という意味です。

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

ここでは、名詞の単語だけを抽出します。また、そのうち2文字未満のものや数字は取り除きます。


### とりあえず試そう

スクリプトは[`tokenize_texts.py`](./Codes/tokenize_texts.py "CODE")です。次のように、コマンドラインからURLを指定して実行すれば、標準出力にHTMLから抽出した単語のリストを表示します。

```
C:\temp>python tokenize_texts.py https://www.cutt.co.jp/
['株式会社', 'カット', 'システム', '先端', '技術', 'Academy', '出版', '書籍', '一覧', '教科書',
 '教材', 'カタログ', '直販', '案内', 'カット', 'システム', '小社', '書籍', '取り扱い', '書店',
 '一覧', '書店', '著者', '講演', '読者', '特典' ... ]
```


### パッケージのインポート

利用に際しては、まずパッケージをインポートします。`janome`にはいくつかモジュールがありますが、ここでは分解を司る`tokenizer`モジュールの`Tokenizer`クラスしか用いないので、次のようにインポートします。

```Python
>>> from janome.tokenizer import Tokenizer
```

tokenizeは、文を単語（形態素）単位に分解する処理です。


### Tokenierオブジェクトの生成

まず、`janome.tokenizer.Tokenizer`クラスをインスタンス化します。引数には何も指定しません。

```Python
>>> t = Tokenizer()                                      # 初期化
```

得られるのは、初期化され、テキストを受け付ける準備のできた`janome.tokenizer.Tokenizer`オブジェクトです。

```Python
>>> type(t)
<class 'janome.tokenizer.Tokenizer'>
```


### テキストの分解

続いて、`janome.tokenizer.Tokenizer`オブジェクトの`tokenize()`メソッドを用いて、テキストを分解します。引数にはテキストを指定します。

前段で得られたのは行単位のテキストのリストだったので、これはループ処理です。

```Python
>>> token_objs = []                                      # 単語オブジェクトの収容用
>>> for text in texts:
...     objs = t.tokenize(text)
...     token_objs.extend(objs)
```

`tokenize()`は分解後の単語オブジェクトのリストを返します（正確にはそれらを返すジェネレータ）。リストを要素にばらしてリストに加えるには、[`list.extends()`](https://docs.python.org/ja/3/library/stdtypes.html#mutable-sequence-types "LINK")を使います。

ここでは、すべてのテキスト（行）から2,775単語が得られました。

```Python
>>> len(token_objs)                                      # 全単語数
2775
```

1つ中身を確認します。

```Python
>>> token_objs[13]
<janome.tokenizer.Token object at 0x7f3858f4f8e0>
```

`tokenize()`の返す個々の要素は、上で示されたように`janome.tokenizer.Token`というオブジェクト（以下`Token`）です。


### Tokenオブジェクト

13番目の`Token`の中身（文字列表現）を確認します。

```Python
>>> str(token_list[13])
'直販\t名詞,一般,*,*,*,*,直販,チョクハン,チョクハン'
```

このフォーマットは、`janome`が依拠している[`MeCab`](http://taku910.github.io/mecab/ "LINK")（和布蕪）の次のものと同じです。

```
表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
```

先頭の「表層系」が単語です。`Token`オブジェクトの`surface`属性からアクセスできます。

```Python
>>> token_list[13].surface
'直販'
```

タブ（`\t`）に続くのが品詞情報で、`part_of_speech`属性からアクセスできます。カンマ区切りで

```Python
>>> token_list[13].part_of_speech
'名詞,一般,*,*'
```


### フィルタリング

単語のリストには、ワードクラウドに入れる意味のないものも散見されます。たとえば、助詞の「が」や句読点の「。」などが大量に含まれていることでしょうが、それらがワードクラウドに現れても役に立ちません。

そこで、ここでは名詞の単語だけを抽出します。名詞なら、`part_of_speech`属性の最初が「名詞」になっているので、[`str.startswith()`](https://docs.python.org/ja/3/library/stdtypes.html#str.startswith "LINK")からチェックできます。

```Python
>>> tokens = [token.surface for token in token_objs if token.part_of_speech.startswith('名詞')]
```

ここでは1,693単語が得られました。

```Python
>>> len(tokens)
1693
```

最初の数語をチェックします。

```Python
>>> tokens[:10]
['株式会社', 'カット', 'システム', '先端', '技術', 'Academy', '出版', '書籍', '一覧', '教科書']
```

名詞の中には、「方」など1文字だけからなるものもあり、たいてい、これだけでは意味が取れません（ちなみに、もとの文は「書店の方へ」などです）。そこで、2文字以上だけの単語に限ります。

```Python
>>> tokens = [token for token in tokens if len(token) > 1]
>>> len(tokens)
1153
```

だいぶ減りました。

続いて、数字も削除します。たとえば「4月20日」の一部である「4」だけ出てきても、もとの意味は失われています。これには、[`str.isnumeric()`](https://docs.python.org/ja/3/library/stdtypes.html#str.isnumeric "LINK")が使えます。

```Python
>>> tokens = [token for token in tokens if token.isnumeric() is False]
>>> len(tokens)
898
```

もっと減りました。


### 次号へ続く

[`tokenize_texts.py`](./Codes/tokenize_texts.py "CODE")は、引数に指定したテキスト文のリストから名詞単語を抽出する`tokenize_texts()`関数と、それをテストする`main`関数で構成されています。以降でこの関数を利用するには、次のようにインポートします。

```Python
from tokenize_texts import tokenize_texts
```
