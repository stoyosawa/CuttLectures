## 5. Pymongoの使い方

データベース`drink`にコレクション`sake`があるとして、そのドキュメントを取得、アップデートする操作を説明します。


### コード

コード全体を示します。ファイルは本リポジトリの[`Codes`](./Codes "INTERNAL")ディレクトリにあります。

<details>
  <summary>mg.py</summary>
  <pre>[File] mg.py
  1  import json
  2  from pprint import pprint
  3  import sys
  4  from pymongo import MongoClient
  5
  6
  7  def db_connect(file):
  8    with open(file) as fp:
  9      creds = json.load(fp)
 10      options = creds['Pymongo']['options']
 11
 12    client = MongoClient(**options)
 13    return client
 14
 15
 16  def db_get_collection(client, database_name, collection_name):
 17    db = client.get_database(database_name)
 18    collection = db.get_collection(collection_name)
 19    return collection
 20
 21
 22  def db_select(collection):
 23    cursor = collection.find({})
 24    for doc in cursor:
 25      pprint(doc)
 26
 27
 28  def db_insert(collection, doc):
 29    collection.insert_one(doc)
 30
 31
 32
 33  if __name__ == '__main__':
 34    client = db_connect(sys.argv[1])
 35    collection = db_get_collection(client, 'drink', 'sake')
 36    db_select(collection)
 37    db_insert(collection, {
 38        "company": "石川酒造",
 39        "yomi": "いしかわしゅぞう",
 40        "alias": ["たまじまん"],
 41        "location": "東京福生市",
 42        "phone": "042-553-0100"
 43      })
 44    client.close()
</pre>
</details>


### インポートする

```python
  4  from pymongo import MongoClient
```

`pymongo`モジュールには3つのクラスがありますが、`MongoClient`があればたいていのことはこなせます。


### 接続する

Atlasに接続するには、[`MongoClient`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/mongo_client.html "LINK")コンストラクタを呼び出します。

```python
  7  def db_connect(file):
  8    with open(file) as fp:
  9      creds = json.load(fp)
 10      options = creds['Pymongo']['options']
 11
 12    client = MongoClient(**options)
 13    return client
 ︙
 34    client = db_connect(sys.argv[1])
```

引数には接続先URL（キーワード引数名は`host`）、ユーザ名（`username`）、パスワード（`password`）を指定します。ここでは、これら情報はJSONフォーマットでファイル（8行目）に収容されているとしています。

```json
{
  "options": {
    "host": "mongodb+srv://...",
    "username": "ユーザー名",
    "password": "パスワード"
  }
}
```


### データベースのコレクションを準備する

接続が完了したら、どのデータベース（`drink`）のどのコレクション（`sake`）を使うかを決めます。

```python
 16  def db_get_collection(client, database_name, collection_name):
 17    db = client.get_database(database_name)
 18    collection = db.get_collection(collection_name)
 19    return collection
 ︙
 35    collection = db_get_collection(client, 'drink', 'sake')
```

データベースを示すオブジェクト（[`Database`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/database.html#pymongo.database.Database "LINK")インスタンス）を取得するには、[`MongoClient.get_database()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient.get_database "LINK")メソッドです。

データベースが得られたら、[`Database.get_collection()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/database.html#pymongo.database.Database.get_collection "LINK")でその中のコレクションオブジェクト（[`Collection`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection "LINK")インスタンス）を取得します。


### ドキュメントの取得

コレクションのオブジェクトが用意できれば、読み書き変更削除が可能になります。

コレクションからドキュメントを抽出するには、[`Collection.find()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.find "LINK")です。引数にはWebインタフェースの［Filter］に記述するのと同じフィルタを辞書形式で指定します。

「すべて」なら、カラの辞書`{}`を指定します。

```python
 22  def db_select(collection):
 23    cursor = collection.find({})
 24    for doc in cursor:
 25      pprint(doc)
 ︙
 36    db_select(collection)
```

`Collection.find()`は、コレクション中のドキュメントの位置を示すカーソルオブジェクトを返します。イテレータなので、あとはループをすることでドキュメントを逐次的に取得するだけです。


### ドキュメントの挿入

ドキュメントを1つだけ挿入するなら[`Collection.insert_one()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.insert_one "LINK")です。引数には挿入するドキュメントを辞書形式で指定します。

```python
 28  def db_insert(collection, doc):
 29    collection.insert_one(doc)
 ︙
 37    db_insert(collection, {
 38        "company": "石川酒造",
 39        "yomi": "いしかわしゅぞう",
 40        "alias": ["たまじまん"],
 41        "location": "東京福生市",
 42        "phone": "042-553-0100"
 43      })
```

Atlasを見れば、新しいドキュメントが作成されていることを確認できます。

一気に複数個のドキュメントを挿入するには`Collection.insert_many()`を使います。


### 切断

データベースサーバとの接続を切断するには、`MongoClient.close()`です。
