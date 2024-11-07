## 概要～NoSQLデータベース

### データベースの種類

データベースはリレーショナル型（Relational Database Management System）とそれ以外に分けられます。

使用言語から区別すると、前者はデータの操作に`SELECT * FROM table WHERE type="relational";`のようなSQL言語を用いるのに対し、後者はSQLを使わないので[NoSQL](https://ja.wikipedia.org/wiki/NoSQL "LINK")と総称されます。

データ構造から区別すると、前者は2次元に広がる表形式でデータをまとめるのに対し、NoSQLは目的に応じて各種のデータ構造が採用されています。

<!-- 〃 := U+3003 DITTO MARK -->
分類 | データ構造 | データベース例 | 特徴
---|---|---|---
リレーショナル | 表 | Oracle | データを表構造に並べ、表の間に関係性（リレーション）を設ける。
NoSQL | ドキュメント型 | MongoDB | JSONのような汎用的な方法でデータを表現する。
`〃` | キー／値型 | Redis | キー＝値の組だけを収容する。シンプルな反面、非常に高速。
`〃` | ワイドコラム型 | Cassandra | リレーショナルに似ているが、列（コラム）を事前に規定しなくてよく、しかも非常に多くの列を構成できる。
`〃` | グラフ型 | Neo4j | グラフ構造でデータを表現する。


### MongoDB

本セミナーで紹介する[MongoDB](https://www.mongodb.com/ja-jp "LINK")は[ドキュメント型](https://aws.amazon.com/jp/nosql/document/ "LINK")のNoSQLデータベースです。

「ドキュメント」と言いますが、テキスト文書やワードドキュメントとは関係ありません。端的にはJSONオブジェクトでデータを管理します（XMLやYAMLのものもあるが、MongoDBはバイナリ形式のJSONを使う）。

MongoDBはNoSQLの中でもトップクラスの人気を誇っています。データベースの人気ランキングは次の[DB-Engines](https://db-engines.com/en/ranking "LINK")から確認できます。

<img src="Images/DbEnginesRanking.png" width="600">


### MongoDB Atlas

MongoDBにはホストシステムにインストールして運用するタイプのものと、オンラインで使えるクラウドタイプのものがあります。ここで紹介するのは後者のクラウドタイプで、[MongoDB Atlas](https://www.mongodb.com/ja-jp/atlas/database "LINK")と呼ばれています。使い勝手はどちらも同じです。

MongoDB Atlasはリソースに制約はありますが、無償で利用できます（ストレージは最大512MBまで）。たいていのカジュアルな用途にはこれで十分です。

リソースをより必要とするシリアスな用途には、有償版もあります。[料金表](https://www.mongodb.com/pricing "LINK")によれば、M10はだいたい月8,000円くらいです。

<img src="Images/AtlasPricing.png" width="600">

[オンラインマニュアル](https://www.mongodb.com/docs/ "LINK")は`https://www.mongodb.com/docs/`にあります。


### MongoDBのデータ構造

MongoDBインスタンスには、複数の「**データベース**」を収容できます。

データベースには複数の「**コレクション**」を収容できます。これはリレーショナル型では「テーブル」（表）に、Excelのようなスプレッドシートアプリケーションでは「シート」に相当します。

コレクションには複数の「**ドキュメント**」が収容できます。テーブル上の各レコード（行）やExcelの1行に相当します。MongoDBでは、これは1つのJSONオブジェクトです。

テーブルコラム（表の列）は「**フィールド**」と呼ばれます。リレーショナル型では列はまんべんなく埋まっていなければなりませんが（該当する値がなければ`NULL`を使う）、MongoDBではフィールドの欠落が許されています。

データベースの構造を示す用語を次の表にまとめます。

リレーショナル | MongoDB | スプレッドシート
---|---|---
データベース | データベース | ファイル
テーブル（表） | コレクション | シート（タブ）
レコード（行） | ドキュメント | 行 | 
コラム（列） | フィールド | 列

ドキュメントを挿入すると、MongoDBはそれぞれのドキュメントに一意な`_id`というフィールドを自動的に挿入します。`_id`フィールドはリレーショナルデータべースのプライマリキーのような役割を果たします。`_id`は12バイト長の16進数文字列24個です。

データ例を次に示します。全体をくくる配列`[]`がコレクション、配列要素のJSONオブジェクト`{}`がレコード、`"name"`や`"company"`などのプロパティ名がフィールドです。レコードが不揃いなところがポイントです（國府鶴にあえて`"phone": null`を用意する必要はない）。

```json
[
  {
    "_id": {"$oid":"65a465076af72e7fe4e87bad"},
    "name": "kouzuru",
    "company": "野口酒造店",
    "location": "東京都府中市"
  },
  {
    "_id": {"$oid":"65750ace416aa0ccd9ce6931"},
    "name": "kaiun",
    "company": "土井酒造場",
    "location": "静岡県掛川市",
    "phone":"0537-74-2006"
  }
]
```


### JSON

JSONは、次のデータ型の組み合わせですべてのデータを表現します。

- 数値（number）
- 文字列（string）
- 真偽値（boolean。`true`または`false`）
- `null`
- 配列（array。要素はどのデータ型でもよい）
- オブジェクト（object）

これらはPythonの組み込みデータ型とおおむね一致しています。

JSONの数値には整数（`int`）や浮動小数点数（`float`）など細かい区別はありません。有効桁数やビット数にも仕様上は制限はありませんが、32ビット浮動小数点数（[IEEE 754](https://ja.wikipedia.org/wiki/IEEE_754 "LINK")）を超えた範囲は実装依存依存なので、使うべきではありません。JSONには複素数型（complex）はありません。

JSONの文字列は必ず二重引用符でくくらなければなりません。Pythonのように単一引用符は使えません。

真偽値はPythonでは`True`、`False`です。大文字小文字に注意します。

`null`は`None`です。

配列はリスト（`list`）です。pythonの`tuple`も区別なく配列扱いです。

オブジェクトは辞書（`dict`）です。

細かいことを確認したくなったら、公式の仕様である[RFC 8259 "The JavaScript Object Notation (JSON) Data Interchange Format"](https://www.rfc-editor.org/info/rfc8259 "LINK")を参照します。
