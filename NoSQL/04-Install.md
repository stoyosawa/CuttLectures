## インストール

Node.js（JavaScriptエンジン）と、Node.jsからMongoDBにアクセスするMongooseライブラリをインストールします。

ここではJavaScriptを用いますが、MongoDBライブラリはC++やPythonやJavaにもあります。だいたいどれも同じような使いかたなので、自分の好みの言語で同じようなことを試してください。


### Node.jsの導入

Node.jsの最新版は、[トップページ](https://nodejs.org/ "LINK")のボタンからダウンロードできます。LTS（左）とCurrent（右）の2つのオプションがありますが、最新版を追いかけているのでなければ、LTSのほうを選びます。

LTSは「Long Term Support」（長期サポート版）の略で、他のソフトウェアの「安定版」に該当します。メジャー番号（ここでは20）が偶数のものがこの長期サポートの対象で、致命的なバグの修正やセキュリティパッチが30か月間提供されます。奇数番は開発版です。どのバージョンがいつリリースされて、いつまでサポートされているかは、[Node.js Release Working Group](https://github.com/nodejs/Release "LINK")から確認できます。

インストールはWindowsなら自己解凍形式のMSI、LinuxやMac OSならtarから好みのディレクトリを指定して展開するだけです。Linuxへのソフトウェアインストールには`yum`や`rpm`などのパッケージマネージャがよく用いられますが、バージョンが古いこともあるので、Linux用の`tar.xz`を入手したほうがよいでしょう。

コンソール（コマンドプロンプト等）から実行できるようにするには、ファイルサーチパスの`PATH`環境変数を設定します（MSIには設定オプションがあります）。

導入済みのNode.jsのバージョンは、コマンドオプションの`--version`から調べられます。

```bash
$ node --version
v20.9.0
```


### パッケージの作成

複数のコードを扱うNode.js開発では、それらファイルをパッケージとしてまとめて管理します。特段難しい話ではなく、所定のディレクトリ配下にコード、Mongooseなどの外部パッケージを置き、管理ファイル`package.json`を作成するだけです。

まず、パッケージを収容するディレクトリを作成し、そこに移動します。

```bash
$ mkdir Codes2
$ cd Codes2
```

続いて、パッケージ管理ファイルの`package.json`をパッケージマネージャである`npm`（Node Package Manager）から作成します。サブコマンドは`init`です。

```bash
$ npm init -y
Wrote to /mnt/c/Home/Codes2/package.json:

{
  "name": "codes2",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

`-y`オプション抜きだと、それぞれのプロパティ値をインタラクティブに入力できるようにプロンプトが現れます。変わったことをするのでなければ、すべてデフォルトのままでかまわないので、`-y`を付けたほうが簡単です。変更したくなったら、エディタで編集すればよいだけです。

`npm`の詳細はマニュアルページの[npm CLI](https://docs.npmjs.com/cli/ "LINK")を参照してください。

パッケージの外枠が容易できたら、Mongooseを`npm install`から導入します。

```bash
$ npm install mongoose
```

`npm install`はデフォルトで、カレントディレクトリに`node_modules`サブディレクトリを生成し、そこに外部パッケージをインストールします。`./node_modules`はNode.jsのライブラリサーチパスに含まれているので、なにもせずとも`require()`がファイルを見つけてくれます。

`npm install`はまた、このパッケージがRestifyに依存していることを`package.json`に書き込みます。

このようにパッケージを管理することで、第3者が使うときに必要な外部パッケージも含めて再構築ができるようになります。



### 実行

Unix系では、スクリプトファイル先頭に次のように`#!`（シェバン）を書き込みます。その上でファイルパーミッションに実行可（`chmod +x`）を加えれば、ファイル名単体で実行できます。

```bash
#!/usr/bin/env node
```

Windowsではこの手は使えないので、コマンド名とそれに引き渡すファイル名を指定します。

```dos
C:\temp>node script.js
```
