## 2. 画像をすべて読み込む

#### インポート

画像処理にはPillowを使います。公式リファレンスは[こちら](https://pillow.readthedocs.io/)です。

まずはモジュールのインポートです。Pillowはその昔、PIL（Python Image Library）と呼ばれていたので、パッケージの名称が`PIL`のままなところがポイントです。

```python
>>> from PIL import Image
```

`Image`はPillowの最も基本的なモジュールです。他に便利なモジュールはたくさんあり、たとえば`ImageDraw`は画像上に円や四角などの幾何学模様や文字を描き込むときに、`ImageOps`は`Image`がカバーしていない（どちらかというとニッチな）処理機能を必要とするときに使います。本セミナーではリサイズに`ImageOps`を使うので、ここでインポートしておきます。

```python
>>> from PIL import ImageOps
```

別々にやらずとも、一気に2つインポートしたほうが楽でしょう。

```python
>>> from PIL import Image, ImageOps
```


#### 画像を読む

画像の読み込みは[`Image.open`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open)関数です。

```python
>>> img = Image.open('Data/cat-8862636_640.png')
>>> type(img)
<class 'PIL.JpegImagePlugin.JpegImageFile'>
```

引数にはファイル名を指定します。他にもオプション引数がありますが、使うことはめったにありません。戻り値は`Image`オブジェクトです。`type`で調べるとメディアタイプ別のサブクラスが示されますが、そこまで細かいことが気になることはめったにありません。

Pillowで読むことのできる画像フォーマットは公式リファレンスの［[Handbook > Appendices > Image file formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#)］にあります。読み込みができるフォーマットであっても書き出しはできないのように非対称なところは注意が必要です。

コマンドラインからも調べられます。

```bash
$ python -m PIL
```


#### 画像を表示する

画像の表示は、`Image`のインスタンスメソッドの[`Image.show`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.show)です。

```python
>>> img.show()
```

引数はとくにありません。

WSLなどの仮想環境ではディスプレイがないのでエラーになります。注意してください。


#### 画像を保存する

画像の保存は[`Image.save`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)です。

```python
>>> img.save('cat.png')
```

引数にはファイル名を指定します。画像フォーマットは拡張子から自動的に判断されます（この場合はPNG）。


#### 全部読む

先ほど用意したファイルリスト`files`からすべて読み込み、画像のリストを生成します。

```python
>>> imgs = [Image.open(path) for path in files]
>>> len(imgs)
7
```

7つ読み込ました。
