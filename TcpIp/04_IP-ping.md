## IPとICMP

本章ではICMP（Internet Control Message Protocol: インターネット制御メッセージプロトコル）を通じて、IPの挙動を観察します。

ICMPはその名が示す通り、インターネットを通るIPデータグラムを制御するのに用いられます。たとえば、ルータが「自分にではなく、別のルータにこのパケットは転送してくれ」とアドバイスするICMP転送（Redirect）があります。転送回数が多すぎ、データグラムが迷子になった可能性があるのでデータグラムは廃棄したと通知するICMP時間超過（Time-to-live exceeded）もそうです。あるいは、宛先への到達可能性をチェックする`ping`でお馴染みのICMPエコー要求/応答（Echo request/reply）は利用したこともあるでしょう。

ICMPパケット（メッセージ）はIPデータグラムのペイロードに直接書き込まれるので、L3（ネットワーク層）のプロトコルです。どの層に属するかは、IPを制御するという目的からもわかります。

IPは、書き込まれたデータがなんであるかを、IPヘッダにある1バイトのProtocolフィールドから判定します。`1`ならICMP、`6`ならTCP、`17`ならUDPです。


### 仕様・参考文献

- Ethernet
	- [Wikipedia MTU（英語版）](https://en.wikipedia.org/wiki/Maximum_transmission_unit#MTUs_for_common_media "LINK") - メディア種別ごとのMTUサイズ。
- IP
	- [IETF RFC 791](https://datatracker.ietf.org/doc/html/rfc791 "LINK") - 仕様。
	- [ネットワークエンジニアとして：TCP/IP - IP](https://www.infraexpert.com/study/tcpip1.html "LINK") - IPデータグラムのフォーマット。
	- [@IT 第10回 IPパケットの構造とIPフラグメンテーション](https://atmarkit.itmedia.co.jp/ait/articles/0304/04/news001_3.html "LINK") - わかりやすい概要。
- ICMP
	- [IETF RFC 792](https://datatracker.ietf.org/doc/html/rfc792 "LINK") - 仕様。
    - [ネットワークエンジニアとして：TCP/IP - ICMP](https://www.infraexpert.com/study/tcpip4.html "LINK") - ICMPメッセージのフォーマット。  
 	- [@network: tracert/tracerouteの仕組み](http://atnetwork.info/tcpip/tcpip89.html "LINK") - tracerouteの原理
- ツール
    - [Microsoft Docs: ipconfig](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig "LINK") - Unixでは`ifconfig`です。
    - [Microsoft Docs: ping](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping "LINK") - Unixでもおなじコマンド名ですが、オプションが激しく異なるので混乱します。
    - [Microsoft Docs: tracert](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tracert "LINK") - Unixでは`traceroute`です。3文字くらいけちるなよ、ビル!!

まずはIPデータグラムとICMPメッセージのフォーマットを見てみましょう。


### 普通にpingを送る

Wiresharkのフィルタには`icmp`または`ip.proto == 1`を指定します。

```
C:\temp> ping -n 1 www.cutt.co.jp                              # pingを1個だけ送る（-nなしだと^cまで永遠に送る）

$ ping -c 1 www.cutt.co.jp                                     # Linuxでの個数制限は-cオプション
```

#### ICMPエコー要求

PCから`www.cutt.co.jp`（`49.212.180.206`）に送信したICMPエコー要求IPデータグラムです。

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 49.212.180.206
    0100 .... = Version: 4
    .... 0101 = Header Length: 20 bytes (5)
    Differentiated Services Field: 0x00 (DSCP: CS0, ECN: Not-ECT)
    Total Length: 60
    Identification: 0x0dac (3500)
    Flags: 0x00
        0... .... = Reserved bit: Not set
        .0.. .... = Don't fragment: Not set
        ..0. .... = More fragments: Not set
    Fragment Offset: 0
    Time to Live: 128
    Protocol: ICMP (1)
    Header Checksum: 0x0000 [validation disabled]
    Source Address: 192.168.1.80
    Destination Address: 49.212.180.206
```

- Total LengthフィールドがこのIPデータグラムのサイズを示しています。IPヘッダが20バイトなので、続くICMP部分が40バイトです。
- Time-to-Liveフィールドが128なので、このIPパケットは、宛先に届くまでにルータを128回ホップしてよいことになります（それを超えたときの話はあとで）。
- Protocolフィールドが1なので、ペイロードはICMPです。

こちらは、そのフレームのペイロードに収容されているICMPメッセージです。

```
Internet Control Message Protocol
    Type: 8 (Echo (ping) request)
    Code: 0
    Checksum: 0x4d19 [correct]
    Identifier (BE): 1 (0x0001)
    Identifier (LE): 256 (0x0100)
    Sequence Number (BE): 66 (0x0042)
    Sequence Number (LE): 16896 (0x4200)
    Data (32 bytes)
        Data: 6162636465666768696a6b6c6d6e6f7071727374757677616263646566676869
```

- 全長40バイトのうち、ICMPの共通ヘッダが4バイト、ICMPエコー要求のヘッダが4バイト、データ部分が32バイトです。
- Typeフィールドが8であることから、このICMPメッセージがICMPエコー要求であることがわかります。
- Sequence Numberフィールドは、送ったエコー要求と返信されるエコー応答を対応付けるためにあります。必ず指定しなければならないわけではないので、0（`0x0000`）のこともあります。BEとLEと二つのバリエーションで書かれているのは、[ビッグエンディアンとリトルエンディアン](https://rainbow-engine.com/little-endian-big-endian/ "LINK")というバイト列の順序を変えて表記しているからです（Wiresharkのサービスで、ICMPの仕様にはありません）。
- データ部分はなんでもかまいません。サイズもお好みで決められます。

#### ICMPエコー応答

受信したICMPエコー応答です。

```
Internet Control Message Protocol
    Type: 0 (Echo (ping) reply)
    Code: 0
    Checksum: 0x5519 [correct]
    Identifier (BE): 1 (0x0001)
    Identifier (LE): 256 (0x0100)
    Sequence Number (BE): 66 (0x0042)
    Sequence Number (LE): 16896 (0x4200)
    Data (32 bytes)
        Data: 6162636465666768696a6b6c6d6e6f7071727374757677616263646566676869
```

- Sequence Numberフィールドが要求で送った`0x4200`と一致するので、これが先ほどの要求とマッチすることがわかります。1個だけ送受するならマッチングは簡単ですが、複数がたくさんのアプリケーションから送受されると対応付けは困難です。
- エコー要求/応答では、受信側はデータ部分をコピーして返信します。ここから、搬送途中で壊れていないかを確認できます。


### 大きなpingを送る

ネットワークのMTUよりも大きなIPデータグラムを送信すると、フラグメント化します。

```
C:\temp> ping -n 1 -l 2000 www.cutt.co.jp                      # 2000バイトのデータを送る

$ ping -c 1 -s 2000 www.cutt.co.jp                             # Linuxでのサイズ指定は-sオプション
```

```
No.	    Time	    Source	            Destination	        Proto   Length	Info
76221	2221.934655	192.168.1.80		49.212.180.206      IPv4	1514	Fragmented IP protocol (proto=ICMP 1, off=0, ID=0dad) [Reassembled in #76222]
76222	2221.934655	192.168.1.80		49.212.180.206      ICMP	562	    Echo (ping) request  id=0x0001, seq=67/17152, ttl=128 (reply in 76228)
76227	2222.082081	49.212.180.206		192.168.1.80        IPv4	1514	Fragmented IP protocol (proto=ICMP 1, off=0, ID=c1f9) [Reassembled in #76228]
76228	2222.082081	49.212.180.206		192.168.1.80        ICMP	562     Echo (ping) reply    id=0x0001, seq=67/17152, ttl=51 (request in 76222)
```

- 最初の二つがICMPエコー要求です。先のものの全長は1,514バイトとありますが、これはEthernetフレームのサイズです。IPは1,500バイト、そのなかのICMPエコー要求のデータサイズは1,480バイトです。残りの部分（Ethernetフレーム562バイト）のデータサイズは520バイトです。ただし、Wiresharkはこれら二つのICMPデータを再構成して示すので、2,000バイトがフルに見えます。
- 残りの二つがICMPエコー応答です。こちらも途中でフラグメント化されたので、2個に分けられて届きます。

最初のデータグラムの中身を（一部）見てみましょう。

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 49.212.180.206
	....
    Flags: 0x20, More fragments
        0... .... = Reserved bit: Not set
        .0.. .... = Don't fragment: Not set
        ..1. .... = More fragments: Set
    Fragment Offset: 0
    ....
```

- フラグメント化されたとき、「これは一部だけで、まだ残りが来ます」ということを受信相手に知らせるためにMF（More Fragments）フラグにビットを立てます。
- Fragment Offsetフィールドは、ここに含まれるデータが全体のデータのどこに位置するかを示すのに使われます。0なので、ここにある1,480バイトのデータは2,000バイトの0～1,479バイト目のものです。

続くフラグメントを見てみます。

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 49.212.180.206
    ...
    Flags: 0x00
        0... .... = Reserved bit: Not set
        .0.. .... = Don't fragment: Not set
        ..0. .... = More fragments: Not set
    Fragment Offset: 1480
    ...
```

- MFビットが立っていないので、これは最後のフラグメントです。
- Fragment Offsetフィールドが1,480としているので、このデータは1480～最後までのバイトです。


### フラグメント禁止

IPには、フラグメント化しなければ宛先に送信できないサイズなのに、フラグメントしてはいけないと指定する「フラグメント禁止」（Don't fragment）フラグがあります。このようなデータグラムを送信すると、経路途上の、そこから先に転送できないルータはICM宛先到達不能（Destination unreachable）メッセージを返信し、受信したデータグラムを廃棄します。

フラグメント禁止機能は送信元と宛先の間の経路上でフラグメント化せずに済むパケットサイズを求めるときに使えますが、トライアンドエラーをしなければならないため、あまりその目的には使われません。

#### ローカルネットワークのMTUを調べる

PCからフラグメント化してはいけないIPデータグラムを送るには、最低でも、自分のネットワークのMTU以下でなければなりません（でなければ送らずあきらめる）。

```
C:\temp> netsh interface ipv4 show interface

$ ifconfig
```

フラグメント化してはならないIPデータグラムを送ります。

```
C:\temp> ping -n 1 -l 1470 -f www.cutt.co.jp                   # Don't fragmentをセット

$ ping -c 1 -s 1470 -M do www.cutt.co.jp                       # Linuxでは-M do
```

> 1,470バイトは講師の環境で、1）ローカルネットワークのMTUよりも小さいが（したがってpingは送れる）、2）ルータより先のMTUより大きい（そこから先はフラグメント化しなければ通れない）サイズです。環境依存なので値をいろいろ変えて試す必要があります。Windows Subsystem for Linuxを利用しているなら、`tracepath`コマンドが使えます（e.g., `$ tracepath -4 -n www.cutt.co.jp`）が、えらく時間がかかります。

#### ICMPエコー要求

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 49.212.180.206
	...
    Flags: 0x40, Don't fragment
        0... .... = Reserved bit: Not set
        .1.. .... = Don't fragment: Set
        ..0. .... = More fragments: Not set
    ...
```

- Dont' fragmentフラグにビットが立っています。

#### ICMP宛先到達不能（応答）

```
Internet Control Message Protocol
    Type: 3 (Destination unreachable)
    Code: 4 (Fragmentation needed)
    Checksum: 0x3d66 [correct]
    Unused: 0000
    MTU of next hop: 1492  
```

- ICMP宛先到達不能メッセージは、8バイトのヘッダと可変長のデータで構成されています。
- TypeフィールドはICMPのメッセージ種別を示し、ここでは3です。
- ICMP宛先到達不能メッセージには、「なぜ宛先に届けられないか」の理由が示されています。ここでは理由は4、データグラムが大きすぎる、です。


### 時間超過

IPデータグラムには寿命があります。寿命がないと、道に迷ったときにそのデータグラムは永遠におなじところをぐるぐるすることになります。

寿命は、送信元から宛先までの間に通過するルータの数で計られます。送信元は寿命をTime-to-live（TTL） IPヘッダフィールドにセットします。たとえば128です。このデータグラムを受信したルータは、値を一つ減じて（ここでは127）から次へ転送します。0になると寿命が尽きたと判断され、そのルータはパケットを廃棄し、ICMP時間超過メッセージを送信元に返送します。

```
C:\temp> ping -n 1 -i 5 www.cutt.co.jp

$ ping -c 1 -t 5 www.cutt.co.jp
```

#### ICMPエコー要求

```
Internet Protocol Version 4, Src: 192.168.1.80, Dst: 49.212.180.206
    ...
    Time to Live: 5
    Protocol: ICMP (1)
    ...
```

- `ping`で指定した通り、TTLフィールドが5に設定されています。

#### ICMP時間超過（応答）

```
Internet Control Message Protocol
    Type: 11 (Time-to-live exceeded)
    Code: 0 (Time to live exceeded in transit)
    Checksum: 0x9fa3 [correct]
    Unused: 00000000
    ...
```

- ICMPヘッダのTypeフィールドが11なので、これは時間超過です。
- 時間超過にも、理由を示すCodeフィールドがあります。もっとも、2種類しかありません。

#### 経路探索

普通に通信をしているときは、間にどんなルータが何個あるかはわかりません。しかし、TTLが0になった時点のルータがICMP時間超過を返信するという仕様を用いて、間のルータを検索することができます。Windowsでは`tracert`コマンドです。

```
C:\temp> tracert www.cutt.co.jp

$ traceroute www.cutt.co.jp
```
