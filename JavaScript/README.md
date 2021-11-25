# JavaScript入門

Version 2021-11-26.  
Satoshi Toyosawa

> 質問はチャットウィンドウから適宜受け付けます。口頭で質問したいときは、単に「質問」や🙋と書いてください。タイミングのよいところで指名します。

### 本セミナーの目標

初学者を対象に*言語としての*JavaScriptを学びます。

- [現代の JavaScript チュートリアル](https://ja.javascript.info/)をベースに用います。
- Webページそのもの（HTML）、Webページのスタイル情報（CSS）、WebページをJavaScriptから操作するインタフェース（DOM）は扱いません。

JavaScriptはWebおよびアプリ開発者にお勧めです。言語のポピュラリティについては次を参考にしてください。

- オープンソース系のプログラマの利用頻度 - [Github](https://madnight.github.io/githut/)
- プログラマコミュニティでの投票 - [Stack Overflow](https://insights.stackoverflow.com/survey/2021)
- 求人ベース - [TechRepublic](https://www.techrepublic.com/article/the-essential-10-programming-languages-developers-need-to-know-this-year/)


### 本セミナーの実習環境

長いコードはほとんど扱わないので、JavaScriptをエディタで書き、実行することができれば、お好みの環境を用いてくださってけっこうです。

JavaScriptプログラムの実行環境はいくつあります。

1. ブラウザ上で、JavaScriptを含んだHTMLページを表示する。
2. ブラウザの開発者コンソールに直接書き込み、実行する。
3. オンライン開発環境を利用する。
4. [Node.js](https://nodejs.org/ja/)など、OSから直接起動できる独立したアプリケーション（JavaScriptエンジン）から実行する。

本セミナーでは主として開発者コンソールを利用します。

#### エディタ

テキストエディタを使います。デフォルトではWindowsでは**メモ帳**、Macでは**テキストエディット**、Unixでは**vi**です。Wordなどの文書作成祖ソフトは使いません。

ファイルを保存するときには`UTF-8`を推奨します。

ファイルの拡張子はHTML（Webページ）なら`.html`、JavaScriptなら`.js`です。

#### 開発環境その1 - HTMLページ

[template.html](./codes/template.html)に示すHTMLファイルの`<script>`と`</script>`で囲まれた部分がJavaScriptのコードです。ファイルとして保存し、適宜変更してはブラウザをリロードすることで結果を確認します。

このテンプレートでは以下の5つのJavaScriptの命令から入出力を行っています。最初の`console.log`以外はブラウザ専用です（言語としてのJavaScriptの一部ではない）。

- 開発者コンソールへの出力 `console.log`
- ページ上への出力 `document.writeln`
- ポップアップウィンドウ `alert`
- ユーザ入力 `prompt`
- 確認入力（yes/no) `confirm`

#### 開発環境その2 - 開発者コンソール

ブラウザに備わっている「開発者コンソール」（ブラウザによって名称は異なります）から、JavaScriptの命令を書き込み、実行することができます。このように、逐次的に入力した命令を実行し表示する環境を*REPL*といいます。`Read-Evaluate-Print Loop`（読み込み-評価（実行）-出力の繰り返し）の略です。

開発者コンソールは次の方法から開けます。

ブラウザ | 開き方 | ショートカットキー
------|-----|-----
Chrome | ⁝ > その他のツール > デベロッパー ツール > コンソール | Ctrl-Shift-I, F12
Edge | ⋯ > その他のツール > 開発者ツール > コンソール | Ctrl-Shift-I
Firefox | ☰ > その他のツール > ウェブ開発ツール > コンソール | Ctrl-Shift-I, F12

打ち間違いの修正、あるいは過去に入力した行を再利用（ヒストリ機能）したいときは次の矢印キーを用います。あとはOSの通常のキーバインドが利用できます（Ctrl-Aですべて選択、Ctrl-Cでコピーなど）

キー | 機能
----|-----
↑ | 前に実行したコマンドを呼び出す
↓ | 次に実行したコマンドを呼び出す
→ | 呼び出したコマンドの文字を変更するために右にカーソルを動かす（ENDで右端）
← | 呼び出したコマンドの文字を変更するために左にカーソルを動かす（HOMEで左端）

試しに次の1文（命令）をコンソールに入力、実行（Enter）してください。

```JavaScript
console.log('Hello World');
```

複数行のコードも一気に実行できます。[sum.js](./codes/sum/js)を試してください。

> REPL環境で上記のように戻り値のない文を評価（実行）すると`undefined`と（やや怪しげに）表示されますが、これは正常な動作です。  
`≫ console.log('hello world');                                 // 実行`  
`> hello world                                                    // 文が実行した結果（文字列の出力）`  
`← undefined                                                    // 文そのものの評価結果`  

#### 開発環境その3 - オンライン開発ツール

いろいろありますが、次のサイトが最もポピュラーでしょう。

- [repl.it](https://replit.com/)
- [jsfiddle](https://jsfiddle.net/)

#### 開発環境その4 - 独立したエンジン

JavaScriptプログラムは、独立した処理エンジンからも実行できます。そのなかでもポピュラーなのは[Node.js](https://nodejs.org/ja/)だと思います。

OSを問わず、WindowsでもLinuxでもMacでも実行できます。実行はコンソール（コマンドプロンプト等）から行います。

JavaScriptにはローカルファイルを開けない、外部と通信ができないといった制約があることはよく知られていますが、これらは安全性の確保のための**ブラウザの制約**です。言語としてのJavaScriptの制限ではありません。したがって、[fsReadFile.js](./codes/fsReadFile.js)のようなファイルを読んで出力するプログラムも書けます。


### オンラインマニュアル

JavaScriptのクラスや関数を検索すると、たいてい次のサイトがトップに出てきます。講師はMDNのほうが好みです。

 - [MDN](https://developer.mozilla.org/ja/docs/Web/JavaScript)（Mozilla Developer's Network)
 - [W3 Schools](https://www.w3schools.com/jsref) - 後者は英語ですが、ワンタッチでGoogle翻訳から日本語に訳せます。
