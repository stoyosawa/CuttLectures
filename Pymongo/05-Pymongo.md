## 5. Pymongoの使い方

データベースのベーシックな[CRUD](https://ja.wikipedia.org/wiki/CRUD "LINK")操作（Create, Read, Update, Delete）の方法を示します。

対象はデータベース`drink`のコレクション`sake`です。


### コード

コード全体を示します。ファイルは本リポジトリの[`Codes`](./Codes "INTERNAL")ディレクトリにあります。

説明はあとから順にします。

<details>
  <summary>▸ mg.py</summary>
  <pre>[File] mg.py
  1  import json
  2  from pprint import pprint
  3  import sys
  4  from pymongo import MongoClient
  5
  6  def db_get_client(url, username, password):
  7    client = MongoClient(url, username=username, password=password)
  8    return client
  9
 10
 11  def db_ping(client):
 12    ping = client.admin.command('ping')
 13    print('ping:', ping)
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
 32  def db_delete(colction, query_filter):
 33    collection.delete_one(query_filter)
 34
 35
 36  def db_update(collection, query_filter, update_operation):
 37    collection.update_one(query_filter, update_operation)
 38
 39
 40  sample_data = {
 41    'たまじまん': {
 42        'company': '石川酒造',
 43        'location': '東京福生市',
 44        'name': '多満自慢',
 45        'phone': '042-553-0100'
 46    },
 47    'こうづる': {
 48      "name": "國府鶴",
 49      "company": "野口酒造店",
 50      "location": "東京都府中市",
 51      "url": "https://www.noguchi-brewery.co.jp/"
 52    }
 53  }
 54
 55
 56  if __name__ == '__main__':
 57    # 接続情報をファイルから読む
 58    cred_file = sys.argv[1]
 59    with open(cred_file) as fp:
 60      creds = json.load(fp)
 61      url = creds['MongoDB']['url']
 62      username = creds['MongoDB']['options']['user']
 63      password = creds['MongoDB']['options']['pass']
 64
 65    client = db_get_client(url, username, password)
 66    db_ping(client)
 67
 68    collection = db_get_collection(client, 'drink', 'sake')
 69
 70    db_select(collection)
 71    db_insert(collection, sample_data['たまじまん'])
 72    db_delete(collection, {'name': '國府鶴'})
 73    db_update(collection, {'name': 'kaiun'}, { '$set': {'url': 'https://kaiunsake.com/'}})
 74
 75    client.close()
</pre>
</details>

認証情報は、次のようなJSON形式で別ファイルに用意してあるとしています（58～63行目）。

```json
{
  "MongoDB": {
    "options": {
      "user": "username",
      "pass": "mysecret",
    },
    "url": "mongodb+srv://cluster0.vklbtaf.mongodb.net/"
  }
```


### インポートする

```python
  4  from pymongo import MongoClient
```

`pymongo`モジュールには3つのクラスがありますが、`MongoClient`があればたいていのことはこなせます。


### 接続する

Atlasに接続するには、URL、ユーザ名、パスワードを指定して[`MongoClient`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/mongo_client.html "LINK")コンストラクタを呼び出します。

```python
  6  def db_get_client(url, username, password):
  7    client = MongoClient(url, username=username, password=password)
  8    return client
 ︙
 65    client = db_get_client(url, username, password)
```

URLにユーザ名とパスワードが埋め込んであれば、2つのキーワード引数は必要ありません。

接続できなければ例外が上がります。

接続できているかを、通信テストの`ping`（MongoDBのコマンド）から確認します。

```python
 11  def db_ping(client):
 12    ping = client.admin.command('ping')
 13    print('ping:', ping)
 ︙
 66    db_ping(client)
```

`MongoClient.admin.commanad()`はMongoDBのコマンドを直接叩くメソッドです。`ping`コマンドは次のようにJSONで返事を返します。

```
ping: {'ok': 1}
```


### データベースのコレクションを準備する

接続が完了したら、どのデータベースのどのコレクションを使うかを決めます。

```python
 16  def db_get_collection(client, database_name, collection_name):
 17    db = client.get_database(database_name)
 18    collection = db.get_collection(collection_name)
 19    return collection
 ︙
 68    collection = db_get_collection(client, 'drink', 'sake') 
```

データベースを示すオブジェクト（[`Database`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/database.html#pymongo.database.Database "LINK")インスタンス）を取得するには、[`MongoClient.get_database()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient.get_database "LINK")メソッドです。ここでは`drink`データベースのオブジェクトを用意しています。

データベースが得られたら、[`Database.get_collection()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/database.html#pymongo.database.Database.get_collection "LINK")でその中のコレクションオブジェクト（[`Collection`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection "LINK")インスタンス）を取得します。ます。ここでは、`drink.sake`です。


### ドキュメントの取得（Read）

コレクションのオブジェクトが用意できれば、読み書き変更削除が可能になります。

コレクションからドキュメントを抽出するには、[`Collection.find()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.find "LINK")です。引数にはWebインタフェースの［Filter］に記述するのと同じフィルタを辞書形式で指定します。

「すべて」なら、カラの辞書`{}`を指定します。

```python
 22  def db_select(collection):
 23    cursor = collection.find({})
 24    for doc in cursor:
 25      pprint(doc)
 ︙
 70    db_select(collection) 
```

`Collection.find()`はカーソルオブジェクトを返します（PL/SQLのようなリレーショナルデータベースプログラミングで出てくるカーソルと同じようなものです）。あとは、そのカーソルをループするだけで、ドキュメントが逐次的に得られます。


### ドキュメントの挿入

同様に、ドキュメントを1つだけ挿入するなら[`Collection.insert_one()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.insert_one "LINK")です。引数には挿入するドキュメントを辞書形式で指定します。

```python
 28  def db_insert(collection, doc):
 29    collection.insert_one(doc)
 ︙
 71    db_insert(collection, sample_data['たまじまん'])
```

一気に複数個のドキュメントを挿入するには`Collection.insert_many()`を使います。


### ドキュメントの削除

フィルタに該当するドキュメントを削除するには、[`Collection.delete_one()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.delete_one "LINK")です。引数にはフィルタ（`find()`で使うのと同じもの）を指定します。

```python
 32  def db_delete(colction, query_filter):
 33    collection.delete_one(query_filter)
 ︙
 72    db_delete(collection, {'name': '國府鶴'})
```

削除されるのは、コレクション中で該当する「最初」のドキュメントです。MongoDBでは、ドキュメントは「たいてい」挿入順に並べられていますが、そうでないこともあります。確実に狙ったドキュメントを削除したいなら、`_id`を使います。

一気にすべてのドキュメントを削除するには`Collection.delete_many()`を使います。


### ドキュメントの更新

フィルタに該当するドキュメントを更新するには、[`Collection.update_oneone()`](https://pymongo.readthedocs.io/en/4.10.1/api/pymongo/collection.html#pymongo.collection.Collection.update_one "LINK")です。第1引数にはフィルタを、第2引数には変更をするフィールドを指定します。

```python
 36  def db_update(collection, query_filter, update_operation):
 37    collection.update_one(query_filter, update_operation)
 ︙
 73    db_update(collection, {'name': 'kaiun'}, { '$set': {'url': 'https://kaiunsake.com/'}})
```

第2引数の辞書のキーは[演算子](https://www.mongodb.com/docs/manual/reference/operator/update/ "LINK")になっていて、ここでは値をセットする`$set`（`$`はリテラル）を指定しています。値には、セットする内容の辞書です。


### コネクションの切断

データベースサーバとの接続を切断するには、`MongoClient.close()`です。
