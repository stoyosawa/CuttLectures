# 作業中


### 指定のタグを抽出する

Beautiful Soupオブジェクトから指定のタグすべてを抽出するには、`bs4.BeautifulSoup`オブジェクトの`find_all()`メソッドを使います。このメソッドはHTMLタグがどこでどのようにネストされていても、ピンポイントにその部分を抽出してくれます。

アンカーの`a`タグを抽出するには次のように、引数にタグ名を指定します。

```Python
>>> a_tag = soup.find_all('a')
```

メソッドの戻り値は`bs4.element.ResultSet`というオブジェクトですが、詳細は気にしなくて結構です。

```Python
>>> type(a_tag)
<class 'bs4.element.ResultSet'>
```

`len()`から抽出したタグの数を知ることができます。

```Python
>>> len(a_tag)
107
```

同様に、`p`タグのオブジェクトも抽出できます。戻り値は先ほど同様`bs4.element.ResultSet`オブジェクトです。

```Python
>>> p_tag = soup.find_all('p')
>>> type(p_tag)
<class 'bs4.element.ResultSet'>
>>> len(p_tag)
56
```

[マニュアル](http://kondou.com/BS4/ "LINK")冒頭が「この文書のクイックスタートと`find_all()`を読めば、それなりに用は足りると思います」とあるように、これだけでたいてい片が付きます。


### 個々のタグを抽出する

`bs4.element.ResultSet`オブジェクトはリストのようにループしたり、`[index]`を介した単一のタグだけの抽出ができます。

`p_tag`の1つ（ここでは1番目）を見てみます。

```Python
>>> p_tag[1]
<p class="oshirase"><img src="toppage/osirase.png" width="80px"/>
<a href="https://seminar.cutt.co.jp/">セミナーをリニューアルしました。</a><br/>
<img height="auto" src="toppage/scr2019-10.png" width="140px"/>
</p>
```

`bs4.element.ResultSet`リストの要素は`bs4.element.Tag`というオブジェクトです。このオブジェクトは`<a href="XXX">云々</a>`のように開きと閉じのタグ、タグに`href`などがあればその属性値、そしてタグに挟まれた文字列を表現しています。

```Python
>>> type(p_tag[1])
<class 'bs4.element.Tag'>
>>> type(a_tag[1])
<class 'bs4.element.Tag'>
```


### リンクを抜き出す

では、`bs4.element.Tag`から必要な情報を抜き出します。

これは、`a`では`href`属性値です。属性値を得るには、`bs4.element.Tag`の`get()`メソッドを用います。引数には属性名を指定します。

```Python
>>> a_tag[1].get('href')
'book/index.html'
```

すべての`a`について`href`属性値を抜き出すなら、次のようにリスト内包表記が使えます（読みやすいように手で改行を入れています）。

```Python
>>> [tag.get('href') for tag in a_tag]
['https://seminar.cutt.co.jp/', 'book/index.html', 'catalog_kenpon/catalog_kenpon.html',
 'direct/index.html', 'about/index.html','shoplist/index.html', ... 以下略]
```

`p`では`<p>...</p>`のように間にある文字列を抜き出します。これには、`bs4.element.Tag`の`text`属性を用います。

```Python
>>> p_tag[2].text
'\n書籍の直販が金融機関への振込に対応しました。\n'
```

こちらも内包表記ですべて取得できます。長いので先頭10文字だけ（途中まで）示します。

```Python
>>> [tag.text[:10] for tag in p_tag]
['\n著者が講演する読者', '\nセミナーをリニュー', '\n書籍の直販が金融機', '5月26日発売', ...以下略]
```

なお、指定のタグ属性が存在しないとき、`get()`は`None`を返します。たとえば、`<a name="internal_link">云々</a>`から`href`を取得したときです。

```Python
>>> no_href = bs('<a name="sat">xxx</a>')                # hrefのない<a>
>>> no_href.find_all('a')[0].get('href')
>>> type(no_href.find_all('a')[0].get('href'))
<class 'NoneType'>
```

`<p></p>`のように間に文字列がないときは、空文字を返します。

```Python
>>> no_p = bs('<p></p>')
>>> no_p.find_all('p')[0].text
''
```

### リンクの整形

ここでターゲットHTMLページに描き込まれたハイパーリンクには、


##### ハイパーリンク

`a`タグの`href`属性で示されたリンク先。

まず、トップページにアクセスし、そこに収容されたローカルなリンクを抽出します。リンクがローカルかは、`href`が`<a href='/top/sub/page1.html></a>`のようにパスだけを参照しているかで判定します。

これらを再度`downloader.py`にかければ、ウェブサイト上の他のページも取得できるようになります。



ただし、そのウェブサイト上のページだけがターゲットなので、`<a href="https://www.google.com">`のように外部にアクセスしているリンクは除外します。

##### 文字列コンテナ

Webページに記述されている言葉はたいてい`p`および`h1`から`h6`のタグに囲まれています。他にもありますが（たとえば`<a></a>`に囲まれた文字列）、ここでは割愛します。言葉が埋め込まれている他のタグがあっても、同じ方法で抽出できます。



### ローカルリンクの抽出

トップページから張られているローカルなリンクを抽出することで、そのサイトを構成するURLを準備します。

ページに埋め込まれたリンク先（URL）は、`<a href="xxxx"></a>`で記述されたアンカータグを抽出し、その`href`属性値を抜き出すことで行えます。これには、`bs4`パッケージ（Beautiful Soup version 4）を用います。

続いて、`href`属性を`reuqests`で利用できるようにフルなURLに変換します。URLの構成は次の通りです。

```
   foo://example.com:8042/over/there?name=ferret#nose
   \_/   \______________/\_________/ \_________/ \__/
    |           |            |            |        |
 scheme     authority       path        query   fragment
```
*["Uniform Resource Identifier (URI): Generic Syntax", RFC 3986 (2005)](https://datatracker.ietf.org/doc/html/rfc3986#section-3 "LINK")第3章より*

同じサイト内へのリンクだけがターゲットなので、パス要素（`path`）以下だけで記述されたリンクを抽出します。クエリ文字列（query）やページ内リンクのフラグメント（fragment）は不要なので、これらは除去します。

パスは`/books/index.html`のような絶対パス、あるいは`../index.html`のような相対パスで記述されているので、これらはトップページのURLを用いて、フルなURLに変換します。たとえば、トップページのURLが`https://www.cutt.co.jp/`で、埋め込まれたリンクが`/books/index.html`なら、`https://www.cutt.co.jp/books/index.html`を構築します。

URLの操作には、Python標準ライブラリの[`urllib.parse`](https://docs.python.org/ja/3/library/urllib.parse.html "LINK")を用います。

さらに、登場したリンクから重複を省きます。これには、Python標準ライブラリの[`set`](https://docs.python.org/ja/3/library/stdtypes.html#set-types-set-frozenset "LINK")を用います。


### ローカルページの取得

上記で得られたURLリストからそれぞれHTMLテキストを取得します。方法は[トップページの取得](#トップページの取得 "INTERNAL")と同じです。

なお、得られるのは、トップページとそこに記載されているローカルリンクのページだけで、そのサイト全体ではありません。

> サイト全体を網羅するには、サブページ内のハイパーリンクも抽出する、別名ドメインを認識する、といった対応が必要ですが、ややこしくなるので、ここでは扱いません。



