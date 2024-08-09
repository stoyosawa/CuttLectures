## 3. 画像サイズを決める

#### 画像サイズを得る

`Image`オブジェクトにはサイズなど画像の属性を収容したプロパティがいくつかあります。とくに重要なもののみを次に示します（それ以外は公式リファレンスの「[Image Attributes](https://pillow.readthedocs.io/en/stable/reference/Image.html#image-attributes)」を参照）。

プロパティ | データ型 | 意味
---|---|---
`filename` | 文字列 | ファイル名
`size` | 整数のタプル | 画像のサイズ（幅, 高さ）
`width` | 整数 | 画像の横幅
`height` | 整数 | 画像の高さ
`is_animated` | 真偽値 | 画像がアニメーションなら`True`。アニメーションでなければプロパティは存在しない。
`n_frames` | 整数 | 画像がアニメーションならその枚数。アニメーションでなければプロパティは存在しない。

こんな感じです。

```python
>>> imgs[0].width
640
>>> imgs[0].height
425

>>> imgs[0].is_animated                    # ないのでエラー
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>

>>> getattr(imgs[0], 'is_animated', False) # このほうが安全
False
```

全部取ってくるならこうです。

```python
>>> [img.width for img in imgs]
[640, 640, 640, 640, 640, 425, 640]

>>> [img.height for img in imgs]
[425, 427, 427, 427, 427, 640, 427]
>>>
```


#### 最適なサイズを決める

サイズがまちまちだと正しくアニメーションが作成できません。そこで画像をすべて同じサイズにリサイズするのですが、問題は、どの大きさにしたらよいかです。

上記のサイズのデータの[代表値](https://www.stat.go.jp/naruhodo/5_tokucho/chushin.html)あるいはその他の統計的指標から決定することになりますが、どれを使うかは悩ましいところです。平均値、最頻値、中央値、幾何平均値、最大、最小。いろいろあります。

> 総務省統計局、やるじゃん。

上記の横幅の結果からすると、外れ値が1つだけと考えて、640にするのがよさそうです。なら、最頻値です。しかし、このパターンだとそうかもしれませんが、次のように微妙にサイズが異なっていたりすると、外れ値のはずの425が選択されてしまいます。

```python
[642, 641, 640, 639, 638, 425, 425]
```

ここでは「えいや」っと、中央値を使うことにします。Pythonには統計関数のモジュール[`statistics`](https://docs.python.org/ja/3/library/statistics.html#averages-and-measures-of-central-location)があり、その`median`から簡単に計算できます。

```python
>>> import statistics
>>> size = (statistics.median([img.width for img in imgs]),  statistics.median([img.height for img in imgs]))
>>> size
(640, 427)
```

というわけで、`(640, 427)`にします。
