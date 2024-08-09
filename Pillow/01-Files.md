## 1. ファイルのリストを得る

#### ターゲットのディレクトリ

ターゲットのファイルは`Data`ディレクトリにあるとします。

```bash
$ ls Data/
cat-1977416_640.jpg*  cat-3739702_640.jpg*  cat-7866716_640.jpg*  cats-eyes-2944820_640.jpg*
cat-3169476_640.jpg*  cat-4541889_640.jpg*  cat-8862636_640.png*  links.json*
```

`.jpg`と`.png`が混在しています。画像ではないファイルもあります。


#### ファイルリストを得る

指定のディレクトリからファイルのリストを得るには、[`os.scandir`](https://docs.python.org/ja/3/library/os.html#os.scandir)です。引数にディレクトリ名を指定すれば、[`os.DirEntry`](https://docs.python.org/ja/3/library/os.html#os.DirEntry)オブジェクトを生成するイテレータ（反復可能なオブジェクト）を返します。

```python
>>> import os
>>> dir_iter = os.scandir('Data')
>>> type(dir_iter)
<class 'posix.ScandirIterator'>
```

ファイル名（文字列）は`os.DirEntry`の`path`プロパティに収容されています。`dir_iter`はイテレータなので、すべて取り出して文字列のリストに置き換えます（そのほうがここでは使いやすいから）。

```python
>>> files_dir = [entry.path for entry in dir_iter]
>>> files_dir
[
    'Data/cat-1977416_640.jpg', 'Data/cat-3169476_640.jpg', 'Data/cat-3739702_640.jpg',
    'Data/cat-4541889_640.jpg', 'Data/cat-7866716_640.jpg', 'Data/cat-8862636_640.png',
    'Data/cats-eyes-2944820_640.jpg', 'Data/links.json'
]
```


#### 所定の拡張子のファイルだけ抽出する

リストには不要なものが含まれているので、拡張子が`.jpg`または`.png`のもののみを抽出します。

パス文字列を拡張子やディレクトリなどに分解してチェックするなら、[`pathlib.PurePath`](https://docs.python.org/ja/3/library/pathlib.html#pathlib.PurePath)が便利です。コンストラクタにパス文字列を指定すれば、オブジェクトが生成できます。

```python
>>> from pathlib import PurePath
>>> pp = PurePath('Data/cat-1977416_640.jpg')
>>> type(pp)
<class 'pathlib.PurePosixPath'>
```

拡張子だけを抜き出すなら、`suffix`プロパティです。

```python
>>> pp.suffix
'.jpg'
```

ターゲットの拡張子を収容したリストを用意し、ファイルの拡張子がそれに含まれているか否かで（`in`演算子）、ファイルを抽出します。念のため、拡張子は小文字に変換してからチェックします。

```python
>>> EXTENSIONS = ['.png', '.jpg']
>>> pp.suffix.lower() in EXTENSIONS
True

>>> files = [f for f in files_dir if PurePath(f).suffix.lower() in EXTENSIONS]
>>> files
[
    'Data/cat-1977416_640.jpg', 'Data/cat-3169476_640.jpg', 'Data/cat-3739702_640.jpg',
    'Data/cat-4541889_640.jpg', 'Data/cat-7866716_640.jpg', 'Data/cat-8862636_640.png',
    'Data/cats-eyes-2944820_640.jpg'
]
```


#### 拡張子以外の基準

拡張子ではなく、ファイル名のパターンなどでファイルを抽出するなら、[正規表現](https://docs.python.org/ja/3/library/re.html)です。

たとえば、ファイル名にアンダースコア`_`とそれに続く3文字か4文字の数字が含まれているものものだけを抽出するなら、こうします。

```python
>>> import re
>>> regexp = re.compile(r'_\d[3,4]')
>>> [f for f in files_dir if regexp.search(f)]
[
    'Data/cat-1977416_640.jpg', 'Data/cat-3169476_640.jpg', 'Data/cat-3739702_640.jpg',
    'Data/cat-4541889_640.jpg', 'Data/cat-7866716_640.jpg', 'Data/cat-8862636_640.png',
    'Data/cats-eyes-2944820_640.jpg'
]
```

先度と同じように、ファイル名末尾が大文字小文字を問わず`.jpg`か`.png`のものを抜き出すならこう書きます。

```python
>>> [f for f in files if re.search(r'\.(jpg|png)', f, re.IGNORECASE)]
[
    'Data/cat-1977416_640.jpg', 'Data/cat-3169476_640.jpg', 'Data/cat-3739702_640.jpg',
    'Data/cat-4541889_640.jpg', 'Data/cat-7866716_640.jpg', 'Data/cat-8862636_640.png',
    'Data/cats-eyes-2944820_640.jpg'
]
```

別の手段があるときでも正規表現を使うか使わないかは好み次第です。一般に、正規表現はパッと見てわかりにくいところがあるので、簡単なやり方があるのなら、そちらを使うというのも一案でしょう。
