#!/usr/bin/env python
# 2024-11-09

import sys
from config import db_connect

def db_create_database(client, dbname, collection_name, doc):
    db = client[dbname]
    collection = db[collection_name]
    collection.insert_one(doc)


def db_drop_database(client, dbname):
    client.drop_database(dbname)


def db_drop_collection(client, dbname, collection_name):
    client[dbname][collection_name].drop()


if __name__ == '__main__':
    client = db_connect(sys.argv[1])
    print(client.list_database_names())
    db_create_database(client, 'food', 'sushi', {"name": "本マグロ赤身", "price": 270, "type": "にぎり"})
    # db_drop_collection(client, 'food', 'sushi')
    # db_drop_database(client, 'food')
    client.close()
