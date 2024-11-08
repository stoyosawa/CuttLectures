## 1. MongoDBとは

### MongoDB

MongoDBは[ドキュメント型データベース](https://aws.amazon.com/jp/nosql/document/ "LINK")です。

ドキュメント型データベースは、データベースで一般的な表形式の構造を取らず、プログラミングで普通に用いられるデータ構造でデータを表現・収容するタイプのデータベースです。「ドキュメント」を名乗っていますが、普通のテキストやワードなどの文書ファイルとは関係はありませんし、それらを収容するものでもありません。

MongoDBはデータをJSONで表現します。JSONのフォーマットはPythonの辞書`dict`とほぼ同じなので、PythonとMongoDBは直接的にデータを交換できます。

SQLを使わないデータベースの総称である[NoSQL](https://ja.wikipedia.org/wiki/NoSQL "LINK")タイプの一種です。

MongoDBはNoSQLの中でもトップクラスの人気を誇っています（[DB-Engines](https://db-engines.com/en/ranking "LINK")より）。

<img src="Images/01-Introduction/db-engine-ranking.png">


### MongoDB Atlas

MongoDBには、一般のデータベースサーバ同様にホストシステムにインストールして運用するタイプと、オンラインで使えるクラウドタイプがあります。ユーザレベルでは、使い勝手に変わりはありません。ここで紹介するのは、[MongoDB Atlas](https://www.mongodb.com/ja-jp/atlas/database "LINK")と呼ばれる後者のクラウドタイプです。

MongoDB Atlasは無償で利用できます。ストレージサイズが小さくてシステムリソースが共有という制約はありますが、カジュアルな目的にはこれで十分です。シリアスな用途には[有償版](https://www.mongodb.com/pricing "LINK")もあります。

<img src="Images/01-Introduction/atlas-pricing.png">


### MongoDBのデータ構造

MongoDB Atlasでは、データベースインスタンスを「**クラスタ**」と呼びます。ホストシステムで稼働するプロセスなら「データベースサーバ」と呼ぶものです。クラスタは普通、1つだけ使います（複数あってもかまわないが）。

クラスタには複数の「**データベース**」を収容できます。これは、リレーショナル型でもデータベースと呼ばれるものに相当します。Excelならファイルです。

データベースには複数の「**コレクション**」を収容できます。これはリレーショナル型では「テーブル」（表）に、Excelのようなスプレッドシートアプリケーションでは「シート」に相当します。

コレクションには複数の「**ドキュメント**」が収容できます。テーブル上の各レコード（行）やExcelの1行に相当します。MongoDBでは、これは1つのJSONオブジェクトです。

テーブルコラム（表の列）は「**フィールド**」と呼ばれます。リレーショナル型では列はまんべんなく埋まっていなければなりませんが（該当する値がなければ`NULL`を使う）、MongoDBではフィールドの欠落が許されています。

データベースの構造を示す用語を次の表にまとめます。

リレーショナル | MongoDB | スプレッドシート
---|---|---
データベース | データベース | ファイル
テーブル（表） | コレクション | シート（タブ）
レコード（行） | ドキュメント（JSONテキスト） | 行
コラム（列） | （JSONオブジェクトの）フィールド | 列

ドキュメントを挿入すると、MongoDBはそれぞれのドキュメントに一意な`_id`というフィールドを自動的に挿入します。`_id`フィールドはリレーショナルデータべースのプライマリキーのような役割を果たします。

AWSの「ドキュメントデータベースとは」にある図がわかりやすいです（AWSのドキュメント型データベースはAmazon DocumentDBといいます）。

<img src="https://d1.awsstatic.com/AWS%20Databases/JSON%20document%20database.64fe2a382abc8ca2b8743f0e3b5af553a33f3fb0.png" width="600">


### JSON

JSONは、次のデータ型の組み合わせですべてのデータを表現します。

- 数値（number）
- 文字列（string）
- 真偽値（boolean。`true`または`false`）
- `null`
- 配列（array。要素はどのデータ型でもよい）
- オブジェクト（object）

これらはPythonの組み込みデータ型と**おおむね**一致しています。

JSONの数値には整数（`int`）や浮動小数点数（`float`）など細かい区別はありません。有効桁数やビット数にも仕様上は制限はありませんが、32ビット浮動小数点数（[IEEE 754](https://ja.wikipedia.org/wiki/IEEE_754 "LINK")）を超えた範囲は実装依存なので、使うべきではありません。JSONには複素数型（complex）はありません。

JSONの文字列は必ず二重引用符`"`でくくらなければなりません。Pythonの`str`は単一引用符`'`も使えますが、JSONでは文法違反です。

真偽値（`bool`）は、Pythonでは`True`、`False`です。大文字小文字に注意します。

`null`は`None`です。

配列はリスト（`list`）です。pythonの`tuple`も`set`も区別なく配列扱いです。JSONはバイナリを扱えないので（すべてテキストで記述される）、`bytes`や`bytesarray`はそのままでは記述できません。

オブジェクトは辞書（`dict`）です。

細かいことを確認したくなったら、公式の仕様である[RFC 8259 "The JavaScript Object Notation (JSON) Data Interchange Format"](https://www.rfc-editor.org/info/rfc8259 "LINK")を参照します。

> MongoDBのJSONはバイナリ版JSON（BSON）なので、`int`と`float`を区別したり、`bytes`や`dateTime.datetime`を直接扱うことができます。詳しくは[bson – BSON (Binary JSON) Encoding and Decoding](https://pymongo.readthedocs.io/en/stable/api/bson/index.html "LINK")を参照してください。
