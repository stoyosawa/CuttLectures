#!/usr/bin/env python
# 2024-11-09
# 設定を読む

import json
from pprint import pprint
import sys
from pymongo import MongoClient


def db_connect(file):
	with open(file) as fp:
		creds = json.load(fp)
		options = creds['Pymongo']['options']

	client = MongoClient(**options)
	return client


def db_get_collection(client, database_name, collection_name):
	db = client.get_database(database_name)
	collection = db.get_collection(collection_name)
	return collection


def db_select(collection):
	cursor = collection.find({})
	for doc in cursor:
		pprint(doc)


def db_insert(collection, doc):
	collection.insert_one(doc)



if __name__ == '__main__':
	client = db_connect(sys.argv[1])
	collection = db_get_collection(client, 'drink', 'sake')
	db_select(collection)
	db_insert(collection, {
	    "company": "石川酒造",
	    "yomi": "いしかわしゅぞう",
	    "alias": ["たまじまん"],
	    "location": "東京福生市",
    	"phone": "042-553-0100"
	  })
	client.close()
