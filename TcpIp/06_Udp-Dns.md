## UDPとDNS

本章ではDNS（Domain Name System）を通じて、UDPの挙動を観察します。

DNSは主として`www.cutt.co.jp`のようなドメイン名を対応するIPアドレスに変換するときに用いられる、システム寄りのアプリケーション層（L7）プロトコルです。高頻度でDNS要求を受け取るDNSサーバーには負荷が高い半面、途中で要求あるいは応答が消えたら何度でおなじことを実行でき（回復不能なデータではない）るので搬送路に信頼性はさほど必要ないので、トランスポート層にはあえてUDPが用いられています。

フラグメント化されるとオーバーヘッドが大きくなるので、DNSは絶対フラグメント化されない、TCP/IPで保証されている最小MTUよりも小さいデータサイズになるように設計されています。つまり、512バイトです。

システム系のサービスであるためにバイナリ志向のプロトコルですが、Wiresharkが解釈してくれるので、読むのに問題はありません。


### 仕様・参考文献

- UDP
	- [IETF RFC 768](https://www.ietf.org/rfc/rfc768.txt "LINK") - TCPと比べていかにコンパクトでシンプルかは、長くなりがちな公式仕様がたった3ページしかないことからもわかります。	
	- [ネットワークエンジニアとして：TCP/IP - UDP](https://www.infraexpert.com/study/tcpip12.html "LINK") - セグメント構造と各種パラメータだけならこちら。
    - [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.txt "LINK") - TCP/UDPウェルノウンポート番号の一覧。
	- [TechMAGAZINE: TCPとUDPの主な特徴6つ｜代表的なポート番号や使い分ける方法も紹介](https://www.fenet.jp/infla/column/network/tcpとudpの主な特徴6つ｜代表的なポート番号や使い分 "LINK") - TCP/UDPの差異を解説。
- DNS
	- [IETF RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035 "LINK") - 仕様です。
	- [@IT DNSパケットフォーマットと、DNSパケットの作り方](https://atmarkit.itmedia.co.jp/ait/articles/1601/29/news014.html "LINK") - DNSメッセージフォーマット
	- [JPNIC インターネット10分講座：DNS](https://www.nic.ad.jp/ja/newsletter/No22/080.html "LINK") - ドメイン名解決のメカニズムの概説。JPNICは日本のインターネットを管理する組織ですので、信頼ある情報源です。
- ツール
    - [Microsoft Docs: nslookup](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup "LINK") - Unixでも同名です。Unixにはほぼ同機能の`dig`もあります。

まずはUDPデータグラムとDNSメッセージのフォーマットを見てみましょう。


### AおよびAAAAレコードの要求

Wiresharkのフィルタを`dns`または`udp.port == 53`に設定して以下を実行します。

```
C:\temp> nslookup www.cutt.co.jp
```

#### UDPデータグラム

UDPもトランスポート層（L4）プロトコルなので、L3のIPのペイロードに載せられて搬送されます。IP側ではProtocolフィールド値が17であることから、積み荷がUDPであることを理解しています。

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 192.168.1.254
    0100 .... = Version: 4
    .... 0101 = Header Length: 20 bytes (5)
    Differentiated Services Field: 0x00 (DSCP: CS0, ECN: Not-ECT)
    Total Length: 60
    Identification: 0xd3f8 (54264)
    Flags: 0x00
    Fragment Offset: 0
    Time to Live: 128
    Protocol: UDP (17)
    Header Checksum: 0x0000 [validation disabled]
    [Header checksum status: Unverified]
    Source Address: 192.168.1.80
    Destination Address: 192.168.1.254
```

なかのUDPはあっさりとしたもので、送信元と宛先のポート番号、そのサイズぐらいしか見るものはありません。ヘッダは固定長の8バイトなので、ペイロードは`40 - 8 = 32`バイトです。

```
User Datagram Protocol, Src Port: 59700, Dst Port: 53
    Source Port: 59700
    Destination Port: 53
    Length: 40
    Checksum: 0x84d8 [unverified]
```

#### DNS要求と応答のシーケンス

この`nslookup`はデフォルトでDNSサーバの名前（IPアドレスからの逆引き）、A（IPv4アドレス）、AAAA（IPv6アドレス）を3回にわたって送受するようです。

```
No.	Time		Source			SrcPort	Destination	DstPort	Protocol	Length	Info
469	9.722443	192.168.1.80	59699	192.168.1.254	53		DNS	86	Standard query 0x0001 PTR 254.1.168.192.in-addr.arpa
470	9.723550	192.168.1.254	53		192.168.1.80	59699	DNS	112	Standard query response 0x0001 PTR 254.1.168.192.in-addr.arpa PTR VRV9517-D652
471	9.724516	192.168.1.80	59700	192.168.1.254	53		DNS	74	Standard query 0x0002 A www.cutt.co.jp
473	10.077264	192.168.1.254	53		192.168.1.80	59700	DNS	104	Standard query response 0x0002 A www.cutt.co.jp CNAME cutt.co.jp A 49.212.180.206
474	10.081612	192.168.1.80	59701	192.168.1.254	53		DNS	74	Standard query 0x0003 AAAA www.cutt.co.jp
477	10.230550	192.168.1.254	53		192.168.1.80	59701	DNS	153	Standard query response 0x0003 AAAA www.cutt.co.jp CNAME cutt.co.jp SOA master.dns.ne.jp
```

#### DNS要求

NO. 471のDNSメッセージを見てみましょう。

```
Domain Name System (query)
    Transaction ID: 0x0002
    Flags: 0x0100 Standard query
    Questions: 1
    Answer RRs: 0
    Authority RRs: 0
    Additional RRs: 0
    Queries
        www.cutt.co.jp: type A, class IN
            Name: www.cutt.co.jp
            Type: A (Host Address) (1)
            Class: IN (0x0001)
```

- UDPはコネクションを持たない「ヒット・アンド・ゴー」なプロトコルです。そのため、送信したUDPデータグラムとそれへの返信を対応付けることができません。Transaction IDはこの対応付けを行うためにDNSが加えています。
- 問い合わせは1個だけです（Questions）。
- そして、その問い合わせは、ドメイン名に対応するIPアドレスです。これはQueriesセクションのtypeに示された`A`からわかります。

#### DNS応答

```
Domain Name System (response)
    Transaction ID: 0x0002
    Flags: 0x8180 Standard query response, No error
    Questions: 1
    Answer RRs: 2
    Authority RRs: 0
    Additional RRs: 0
    Queries
        www.cutt.co.jp: type A, class IN
            Name: www.cutt.co.jp
            Type: A (Host Address) (1)
            Class: IN (0x0001)
    Answers
        www.cutt.co.jp: type CNAME, class IN, cname cutt.co.jp
            Name: www.cutt.co.jp
            Type: CNAME (Canonical NAME for an alias) (5)
            Class: IN (0x0001)
            Time to live: 3600 (1 hour)
            Data length: 2
            CNAME: cutt.co.jp
        cutt.co.jp: type A, class IN, addr 49.212.180.206
            Name: cutt.co.jp
            Type: A (Host Address) (1)
            Class: IN (0x0001)
            Time to live: 3600 (1 hour)
            Data length: 4
            Address: 49.212.180.206
```

- Transaction IDが`0x0002`と要求のそれとマッチするので、これが上記の要求への回答であることがわかります。
- Questionsセクションは質問が1個あるといっています。Queriesセクションには要求に書かれたものがそのままコピーされています。
- Answersセクションは回答が2個あるといっています。
	- 一方はCNAMEです。つまり、`www.cutt.co.jp`は別名であることをつたえています。本名は`cutt.co.jp`です。
	- 他方はこの`cutt.co.jp`に対するAレコードです。
	- どちらもTime to Liveが1時間だといっています。つまり、この`www.cutt.co.jp = cutt.co.jp = 49.212.180.206`の対応情報は今から1時間は有効で、何回も使いまわせます。しかし、1時間経過したら、再度問い合わせをしなければなりません。


### DNSキャッシュの操作

Windowsは、DNSを通じて取得したレコードを再利用するためにキャッシュしています。表示には`ipconfig`コマンドを用います。

```
C:\temp> ipconfig/displaydns
```

DNSキャッシュをクリアするには`ipconfig/flushdns`です。

```
C:\temp> ipconfig/flushdns
```

DNSキャッシュをクリアし、`http://www.cutt.co.jp/about/index.html`にアクセスすると、当該URLに対するDNS要求/応答が発生します。しかし、その後画面をリフレッシュしても、DNS通信は発生しません。キャッシュが用いられるからです。

