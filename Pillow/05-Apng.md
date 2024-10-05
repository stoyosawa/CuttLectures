## 5. APNGを生成する

#### 保存オプション

アニメーションでも、保存には[`Image.save`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)を使います。

`Image.save`はインスタンスメソッドなので、`Image`オブジェクト1つにメソッドを作用させます。ここで用意しているのは画像のリストなので、先頭のものだけに作用させます。第1引数がファイル名なのは、シングルイメージのときと同じです。

```python
>>> resized[0].save(
...     'cat.png',	
```

残りは、`append_images`オプション引数からリストで指定します。ただし先頭は除外するので、`[1:]`でスライスします。

```python
...     append_images=resized[1:],
```

重要なのは`save_all`オプションに`True`指定するところです。これがないと、シングルイメージしか参照しないので、アニメーションになりません。

```python
...     save_all=True,
```

あと任意の設定事項です。`duration`は紙芝居のフリップの速度を示します（単位はミリ秒）。`loop`は終わりまで再生したらもとに何回戻るかをセットするオプションで、デフォルトの0だとエンドレスにループします。

画像フォーマット別の保存オプション（およびオブジェクト属性）は公式リファレンスの［Handbook > Appendices > Image file formats］に記載されています。アニメーションPNGの場合は「[APNG sequences](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#apng-sequences)」の「Saving」ところをチェックします（なぜか`save_all`の記載がないですが、それはGIFのところを見てください）。


#### まとめると

まとめれば、こうです。

```python
>>> resized[0].save(
    'cats.png',                        # ファイル名
    append_images=resized[1:],         # 以降の画像
    duration=600,                      # 間隔（ミリ秒）
    loop=0                             # ループ回数（エンドレス）
)
```

<img src="Images/cats.png" width="400">



#### 全部まとめると

以上、ファイル検索からAPNGの保存までのステップは本Githubの[`Codes/apng.py`](https://github.com/stoyosawa/CuttSeminars/blob/main/Pillow/Codes/apng.py)に収容しました。



#### Note

黒猫の画像は[Pixabay](https://pixabay.com/)から取ってきました。
