#!/usr/bin/env python

import json
from pprint import pprint
import sys
from pymongo import MongoClient

def db_get_client(url, username, password):
	client = MongoClient(url, username=username, password=password)
	return client


def db_ping(client):
	ping = client.admin.command('ping')
	print('ping:', ping)


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


sample_data = {
	'たまじまん': {
	    'company': '石川酒造',
	    'location': '東京福生市',
	    'name': '多満自慢',
	    'phone': '042-553-0100'
	},
	'こうづる': {
		"name": "國府鶴",
		"company": "野口酒造店",
		"location": "東京都府中市",
		"url": "https://www.noguchi-brewery.co.jp/"
	}
}


if __name__ == '__main__':
	# 接続情報をファイルから読む
	cred_file = sys.argv[1]
	with open(cred_file) as fp:
		creds = json.load(fp)
		url = creds['MongoDB']['url']
		username = creds['MongoDB']['options']['user']
		password = creds['MongoDB']['options']['pass']

	client = db_get_client(url, username, password)
	db_ping(client)

	collection = db_get_collection(client, 'drink', 'sake')

	db_select(collection)
	db_insert(collection, sample_data['たまじまん'])
	db_delete(collection, {'name': '國府鶴'})
	db_update(collection, {'name': 'kaiun'}, { '$set': {'url': 'https://kaiunsake.com/'}})

	client.close()
