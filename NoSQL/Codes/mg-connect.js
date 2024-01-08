#!/usr/bin/env node

const fs = require('node:fs');
const mongoose = require('mongoose');
mongoose.pluralize(null);


async function connect(url, options) {
	// データベース接続
	await mongoose.connect(url, options);
	console.log('Connected.');

	// スキーマの設定
	let schema = mongoose.Schema({
		name: String,
		company: String,
		location: String,
		url: String,
		phone: String
	});
	let Sake = mongoose.model('sake', schema);

	// Find (=select)
	let results = await Sake.find({}).exec();
 console.log('Find: ', results);

	// 切断
	await mongoose.disconnect();
	console.log('disconnected.');
}


if (require.main === module) {
	let credential = JSON.parse(fs.readFileSync(process.argv[2], {encoding: 'utf-8'}));
	connect(credential.url, credential.options);
}
