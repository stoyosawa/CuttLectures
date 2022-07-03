## 頻度のカウント

ワードクラウド生成ライブラリが受け付けるデータは単語をキー、その出現頻度を値とした辞書なので、前段で得た単語リストからこれを作成します。

いくつか手段がありますが、ここではまず重複のない単語のリストを用意し、それをベースに単語数をカウントします。

### 重複のないリスト

重複のあるリストから、重複のないリストを作成するには、標準ライブラリに備わっている集合型の[`set`](https://docs.python.org/ja/3/library/stdtypes.html#set-types-set-frozenset "LINK")を使います。

`set`も`list`のように要素を収容するコンテナ型ですが、同じ要素を含むことができないという制約があります。そのため、`list`から`set`を作成すると、自動的に重複が省かれます。

```Python
>>> len(tokens)                                          # もとのリスト
898
>>> s = set(tokens)                                      # set作成
>>> len(s)
308
```

上記のように、重複が省かれ、単語数が308に減少します。

`set`はそのまま用いてもよいのですが、手慣れた`list`に戻します。

```Python
>>> unique_tokens = list(s)
```

### 頻度計算

頻度は、「その単語の数」÷「すべての単語の数」です。

すべての単語の数は、元の重複のある単語リストのサイズです。

```Python
>>> size = len(tokens)
>>> size
898
```

リスト中の同一の要素の数は[`list.count()`](https://docs.python.org/ja/3/library/stdtypes.html#sequence-types-list-tuple-range "LINK")で得られます。165番目の単語から確認します。

```Python
>>> tokens[165]                                          # 165番目は「情報」
'情報'
>>> tokens.count('情報')                                 # 18個ある
18
```

頻度は従って、次の通りです。

```Python
>>> tokens.count('情報') / size                          # 2%くらい
0.0200445434298441
```

全体について得るなら、次のようにループを組みます。キーは単語、値は頻度です。

```Python
prob = {key:tokens.count(key)/size for key in unique_tokens}
```

確認のため、先ほどの「情報」キーを検索します。

```Python
>>> prob['情報']
0.0200445434298441
```

### まとめ

以上をスクリプトファイルにまとめたものは、[calc_probs.py](./Codes/short_version/calc_probs.py "INTERNAL")に収容しました。

以降でこの関数を利用するには、次のようにインポートします。

```Python
from calc_probs import calc_probs
```

コマンドプロンプトから（`main`から）実行するなら、引数にURLを指定します。`main`はこれまでの関数の順に呼び出すことで名詞単語リストを得、単語頻度を表示します。

```
C:\temp>python calc_probs.py https://www.cutt.co.jp/
{'作成': 0.0033407572383073497, '大塚': 0.0011135857461024498,
 'トピック': 0.0011135857461024498,  '組込み': 0.0011135857461024498, ...}
```


