## 1. 導入

JavaScriptプログラム（スクリプト）を書く上で必要な方法や環境を説明します。

- [1.1 JavaScript入門](https://ja.javascript.info/intro)
- [1.2 マニュアルと仕様](https://ja.javascript.info/manuals-specifications)
- [1.3 コードエディタ](https://ja.javascript.info/code-editors)
- [1.4 開発者コンソール](https://ja.javascript.info/devtools) + [2.1 Hello, world!](https://ja.javascript.info/hello-world) + [2.2 コード構造](https://ja.javascript.info/structure) + [2.6 インタラクション](https://ja.javascript.info/alert-prompt-confirm)
- 演習

### 1.1 JavaScript入門

Webおよびアプリ開発者にお勧め!

- オープンソース系のプログラマの利用頻度 - [Github](https://madnight.github.io/githut/)
- プログラマコミュニティでの投票 - [Stack Overflow](https://insights.stackoverflow.com/survey/2021)
- 求人ベース - [TechRepublic](https://www.techrepublic.com/article/the-essential-10-programming-languages-developers-need-to-know-this-year/)

#### ブラウザ内のJavaScriptで出来ないことは？

外部との連絡ができないのはブラウザの制約であり、言語としてのJavaScriptの制限ではありません。たとえば、おなじJavaScriptを用いる[バックエンド](https://school.dhw.co.jp/course/web/contents/w_backend.html)向けの[Node.js](https://nodejs.org/ja/)ではファイル入出力やOSへのアクセスが可能です。

例: [fsReadFile.js](./codes/fsReadFile.js)

```JavaScript
const fs = require('fs');

let file = process.argv[2];                                   // OS（シェル）からコマンドライン引数を読める
fs.readFile(file, function(err, data) {                       // ファイルが読める
  console.log(data.toString());
});
```

#### JavaScriptを“覆う”言語

たとえば、TypeScriptで書かれたプログラムを*コンパイル*（*トランスパイル*）することでJavaScriptに変換できます。

例: [helloWorld-ts.ts](./codes/helloWorld-ts.ts)

```JavaScript
let message: string = 'Hello, World!';                        // この変数は文字列しか扱いません
console.log(message);
```

変換後

```JavaScript
var message = 'Hello, World!'; // この変数は文字列しか扱いません
console.log(message);
```


### 1.2 マニュアルと仕様

JavaScriptのクラスや関数を検索すると、たいてい[MDN](https://developer.mozilla.org/ja/docs/Web/JavaScript)（Mozilla Developer's Network)か[W3 Schools](https://www.w3schools.com/jsref)のページがヒットします。後者は英語ですが、ワンタッチでGoogle翻訳から日本語に訳せます。


### 1.3 コードエディタ

Windowsユーザなら「メモ帳」（notepad.exe）でとりあえずは充分です。


### 1.4 開発者コンソール

作成したJavaScriptのプログラムの実行には、いくつか方法があります。

- ブラウザ上で、JavaScriptを含んだHTMLページを表示する。
- ブラウザの開発者コンソールに直接書き込み、実行する。
- オンライン開発環境を利用する。
- [Node.js](https://nodejs.org/ja/)など、OSから直接起動できるアプリケーション（JavaScriptエンジン）から実行する。

本セミナーでは主として開発者コンソールを利用します。

##### HTMLページ

HTMLでは

- 開発者コンソールへの出力 `console.log`
- ページ上への出力 `document.writeln`
- ポップアップウィンドウ `alert`
- ユーザ入力 `prompt`
- 確認入力（yes/no) `confirm`

で文字の入出力ができます。`console.log`以外はブラウザ専用です（[2.6 インタラクション](https://ja.javascript.info/alert-prompt-confirm)参照）。

> `console`（これはオブジェクト）には各種のコンソール出力メソッド（関数、コマンド）が用意されています。たとえば、エラー出力用の`console.error`があります。利用可能な全リストは[MDN console](https://developer.mozilla.org/ja/docs/Web/API/console)から参照できます。

例: [template.html](./codes/template.html)

```html
<html>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
 <head>
  <title>JavaScript入門 HTML テンプレート</title>
 </head>

<body>
 <!-- ここからJavaScript ---------------------------------> 
 <script>
  console.log('テスト');                                        // ブラウザコンソールへの出力
  document.writeln('<p>テスト</p>');                            // ブラウザページへの出力
  alert('テスト');                                              // アラート（ポップアップウィンドウ）
  promptMe = prompt('わたしに入力して');                          // プロンプト（入力）
  console.log(promptMe);                                      // その出力
  confirmMe = confirm('わたしを確認して');                        // 確認（入力）
  console.log(confirmMe);                                     // その出力
 </script>
 <!-- ここまで ---------------------------------> 
 </body>
</html>
```

> 和文字を含んだファイルの保存にはUTF-8を用います。Shift-JISやiso-2022-jpでもたいてい別状ありませんが、文字化けの原因になりがちです。

##### 開発者コンソール

ブラウザ | 開き方 | ショートカットキー
------|-----|-----
Chrome | ⁝ > その他のツール > デベロッパー ツール > コンソール | Ctrl-Shift-I, F12
Edge | ⋯ > その他のツール > 開発者ツール > コンソール | Ctrl-Shift-I
Firefox | ☰ > その他のツール > ウェブ開発ツール > コンソール | Ctrl-Shift-I, F12

例: コンソール出力

```javascript
console.log('Hello World');
```

キーバインド

キー | 機能
----|-----
↑ | 前に実行したコマンドを呼び出す
↓ | 次に実行したコマンドを呼び出す
→ | 呼び出したコマンドの文字を変更するために右にカーソルを動かす（ENDで右端）
← | 呼び出したコマンドの文字を変更するために左にカーソルを動かす（HOMEで左端）

あとはOSの通常のキーバインドが利用できます（Ctrl-Aですべて選択、Ctrl-Cでコピーなど）

> インタラクティブに行単位で入力－実行－結果表示の繰り返しをREPL（Read-Evaluation-Print loop）といいます。

例：コンソール出力（エラー）

```javascript
consoLe.log('Hello World');
```

エラーの意味は検索すればわかります（たとえばMDNの[JavaScript エラーリファレンス](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Errors)）。

例: 複数行

```javascript
/* 1から10の和（55）を求める */
x = new Array(10);                                       // 10個の要素を収容する配列を生成（最初は空っぽ）
x.fill(1);                                               // 10個の要素をすべて1にする（空っぽでは計算できない）
x = x.map((elem, idx) => idx+1)                          // 上記の要素を1から10に変更する
let sum = x.reduce((prev, curr) => prev + curr);         // すべて足す
console.log(sum);                                        // 結果の表示
```

> プログラムの複雑さは言語に依ります。たとえば、Pythonなら上記は`sum(range(1, 11))`だけです。しかし、別にPythonが常に偉いわけではなく、JavaScriptの方が手早く書けるものもあります。

上記で用いられている**文**、**セミコロン**、**コメント**の説明は[2.2 コード構造](https://ja.javascript.info/structure)を参照してください。

[2.2 コード構造ーコメント](https://ja.javascript.info/structure#comments)の末尾で、「より良いコメントの書き方」を説明する[3.2 コーディングスタイル](https://ja.javascript.info/coding-style)への参照があります。これは、他人が読みやすいコードを書くためのガイドラインです。書き方の作法なので、いろいろなやり方があります。なかでももっとも著名なのは、Googleが自社開発で採用している[Google JavaScriptコーディングガイドライン](https://google.github.io/styleguide/jsguide.html)（英文）です。

##### オンライン開発ツール

repl.it

- [repl.it](https://replit.com/)にアクセス。
- ページ下の*Langauages*から*JavaScript*を選択。
- 左のパネルにコードをペースト。
- ▷ Run から実行。
- 右のパネルに結果が表示される。

jsfiddle

- [jsfiddle](https://jsfiddle.net/)にアクセス。
- *JavaScript+No-Library (pure JS)*（左下）にコードをペースト。
- ▷ Run（上端のメニューバー左端）から実行。
- *Result*（右下）の*Console (beta)*に結果が表示される。

##### Node.js

- Node.js（ノード・ジェイエス）はChromeからJavaScriptの処理メカニズムを抽出して、PCコンソールから実行できるようにした実行環境です。
- [Node.js](https://nodejs.org/)からインストール。
- デモ（Windows Subsystem for Linux）


### 演習

1. [template.html](./codes/template.html)をローカルにコピーし、ウェブブラウザで開き、三か所に表示される*Hello World*を確認しなさい。
2. 1のJavaScript文のどれかひとつから、末尾のセミコロンを外して実行しなさい。違いはありますか?
3. 2のJavaScript文のどれかひとつをコピペして実行しなさい。どうなりましたか?
4. 3のJavaScript文のどれかひとつにわざと誤りを入れて、実行しなさい。3のときとの違いはなんですか?
5. 開発者コンソールから`console.log('Hello World');`を実行しなさい。
6. 4にわざと誤りを入れて、実行します。表示されたエラーの意味を調べなさい。
