<img src="https://pillow.readthedocs.io/en/stable/_static/pillow-logo-dark-text.png" width="200">

### 目的

本セミナーでは、Python [Pillow](https://pillow.readthedocs.io/)を使ってアニメーションPNG画像を生成します。

<img src="Images/cats.png" width="200">

アニメーション画像というとGIFが定番です。実際、ネット上にいくつもあるアニメーション画像生成サービスは、ほとんどすべてがGIFを対象にしています。しかし、最大256色しか使えないという制約のあるGIFの表現力は高くありません。アニメーション機能は魅力的ですが、計算機能力の低かった1989年生まれの仕様では、昨今ではさすがに見劣りがします。

これに対し、2004年に発表された[Animation PNG（APNG）](https://ja.wikipedia.org/wiki/Animated_Portable_Network_Graphics)ならフルカラーのままアニメーションが作れます。残念ながら正式なPNGの仕様には含まれないことになりましたが、たいていのブラウザがサポートしてます。

> <img src="https://upload.wikimedia.org/wikipedia/commons/6/68/ISO_7001_PI_PF_001.svg" width="30"> アニメーションのできる画像は他にも[Webp](https://ja.wikipedia.org/wiki/WebP)と[AVIF](https://ja.wikipedia.org/wiki/AVIF)があります。Pillowは前者をサポートしています。

生成スクリプトはPythonで書きます。汎用的でありながら手軽に使え、利用者も情報も多く、実行環境を問わないPythonは昨今ではスタンダードと呼んでもよいくらいのプログラミング環境です（エンジニアが使っている言語のランキングが[Stack Overflow Developer Survey](https://survey.stackoverflow.co/2023/#technology-most-popular-technologies)から調べられます）。

本セミナーを修了することで、Python+Pillowによる画像処理にストレスなく付き合えるようになります。


### プログラム

APNG画像は次の要領で作成します。

- 指定のディレクトリ配下にある画像ファイルのリストを得る。
- 上記のすべての画像を読み込む。
- すべての画像サイズから、最適なAPNG画像サイズを決定する。
- 画像サイズを揃える。
- APNGを生成する。

ちなみに、サイズ不揃いのまま強引に作製すると、適切に表示されなくなります（挙動はビューワー依存。左がGIF、右がPNGのもの）。

<img src="Images/not-resized.gif" width="200"> <img src="Images/not-resized.png" width="200">


### 受講対象者

主な対象はWebデザイナ、あるいは簡単なところから画像処理を学ぼうと考える学生さんやソフトウェアエンジニアです。

受講者はPythonの基本、たとえば基本データ型、ループ、関数などは理解しているとして話を進めます。

内包表記（`[x**2 for x in range(10)]`の類）などちょっと凝った言語仕様やあまり使わない標準ライブラリは、必要に応じてその都度説明します。


### 実習環境

レクチャーと歩調を合わせて実際に試してもらえれば、理解が進みます。環境は、Pythonが実行可能ならなんでもかまいません。講師は[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)を利用します。

次のようにインタラクティブモードで1行ずつ試しながら進行します。

```Python
$ python
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x = 'hello world'
>>> x
'hello world'
```

本ワークショップでは、外部パッケージのPillowを使います。用意がなければ、次の要領でインストールしてください。

```bash
$ pip install pillow
```


### 参考資料

- [Pillowホームページ](https://pillow.readthedocs.io/)。APIリファレンスなどはこちらから。
- [Python標準ライブラリ](https://docs.python.org/ja/3/library/index.html)。Pythonのリファレンスマニュアル。
- 豊沢聡: 『[Python + Pillow/PIL―画像の加工・補正・編集とその自動化 ](https://www.yodobashi.com/product/100000009003620044/)』, カットシステム（2022年9月）。

<img src="https://www.cutt.co.jp/book/images/978-4-87783-525-5.png" width="200">
