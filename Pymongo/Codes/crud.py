#!/usr/bin/env python

from pprint import pprint
import sys
from config import db_connect


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


def db_delete(colction, query_filter):
	collection.delete_one(query_filter)


def db_update(collection, query_filter, update_operation):
	collection.update_one(query_filter, update_operation)


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
	db_delete(collection, {'company': '野口酒造店'})
	db_update(collection, {'yomi': 'しだいずみしゅぞう'}, { '$set': {'url': 'http://shidaizumi.com/'}})

	client.close()
