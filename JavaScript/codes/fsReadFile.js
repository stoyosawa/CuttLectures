// JavaScript入門 - Node.js を用いたファイル入力
// 2021-10-30: ST

const fs = require('fs');

let file = process.argv[2];                                   // OS（シェル）からコマンドライン引数を読める
fs.readFile(file, function(err, data) {                       // ファイルが読める
  console.log(data.toString());
});