<img src="https://stedolan.github.io/jq/jq.png" width="200">

### 目的

本セミナーでは、[`jq`](https://stedolan.github.io/jq/)を用いたJSONテキスト解析を説明します。最も簡単なものなら`.`だけ、難しいものなら次のようなものくらいをカバーしたいと考えています。

```
($value | ascii_downcase) as $value |
.[] |
.name = (.Name | ascii_downcase) |
select(contains({"name": $value})) |
del(.name)
```



### プログラム

90分お試し版には、とくに決まったプログラムはありません。最初に`jq`の使い方を簡単に説明したあとは、参加者の持ち寄ったJSONテキストを、好みの方法で解析していくという演示形式を取ります（難しいのを持ってこられるとその場では対応できないかもしれません。その際は、ご容赦のほどを）。

> 共有されるので、パスワードなどセンシティブな情報はあらかじめ取り除いておいてください。


### 環境とツール

`jq`は依存関係のない単一実行形式ファイルなので、設定せずとも[ダウンロード](https://stedolan.github.io/jq/download/)するだけで利用できます。最新版（2018年11月）のバージョンは1.6です。必須ではありませんが、あらかじめ自機にインストールしておくと、話を聞きながら試すことができて便利です。

Linix、OS X、Windows、FreeBSD、Solarisで利用可能です。ただし、コマンドプロンプトだと特殊文字の記述（エスケープ）が複雑になりがちなので、[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)をお勧めします。

セミナーでは、`jq`の実行には[jq play](https://jqplay.org/)を用います。

共有エディタには、[MeetingWords](http://meetingwords.com/)を利用します。解析したいJSONテキストがあれば、こちらにペーストしてください。リンクはセミナー開始時にZoomチャットに張り付けます。

（認証なしでアクセスできる）RESTインタフェースへのアクセスには[`curl`](https://curl.se/)を使います。


### 受講対象者

どなたでも。


### リファレンス

- [`jq` 1.6 マニュアル](https://stedolan.github.io/jq/manual/v1.6/)
- [The JavaScript Object Notation (JSON) Data Interchange Format](https://tools.ietf.org/html/rfc8259"), RFC 8259。JSONテキストの仕様です。
- [jqDoc-public](https://github.com/stoyosawa/jqDoc-public)。講師のGithubサイトです。サンプルJSONテキストはここからダウンロードします。
- [`jq`ハンドブックーNetOps/DevOps 必携のJSONパーザ](http://www.cutt.co.jp/book/978-4-87783-491-3.html), 2021年。本セミナーのベースとなっている書籍です。
- [Stack overflow - Questions tagged [jq]](https://stackoverflow.com/questions/tagged/jq)
- [Qiita - ./jq タグ](https://qiita.com/tags/jq)
