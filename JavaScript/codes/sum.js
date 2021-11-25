/* JavaScript入門 - ちょっと長いコードのサンプル
	 Version 2021-11-26: ST

	 1から10の和（55）を求める
*/
x = new Array(10);                                       // 10個の要素を収容する配列を生成（最初は空っぽ）
x.fill(1);                                               // 10個の要素をすべて1にする（空っぽでは計算できない）
x = x.map((elem, idx) => idx+1)                          // 上記の要素を1から10に変更する
let sum = x.reduce((prev, curr) => prev + curr);         // すべて足す
console.log(sum);                                        // 結果の表示