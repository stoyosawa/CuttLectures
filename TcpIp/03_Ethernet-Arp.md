## EthernetとARP

本章ではARP（Address Resolution Protocol: アドレス解決プロトコル）を通じて、Ethernetの挙動を観察します。

ARPは、データリンク層（L2）のMACアドレスとネットワーク層（L3）のIPアドレスを対応付けるメカニズムです。ARPパケット（メッセージ）はEthernetフレームのペイロードに直接書き込まれるので、L2（データリンク層）のプロトコルです。

Ethernetは書き込まれたデータがなんであるかを、Ethernetヘッダにある2バイトのEtherTypeフィールドから判定します。`0x0800`ならIPデータグラムが搭載されています。`0x0806`ならARPです。

> ネットワーク設定を含むシステム関係のコマンドは管理者特権が必要なので、コマンドプロンプトは「管理者として実行」します。


### 仕様・参考文献

- Ethernet
    - [IEEE 802.3-2018](https://ieeexplore.ieee.org/document/8457469/ "LINK") - 公式な仕様書ですが、あまりに大部なため読んだことのある人は少ないと噂されています。
    - [詳説 イーサネット 第2版](https://www.oreilly.co.jp/books/9784873117171/ "LINK") - オライリーの書籍。ハード系のネットワークエンジニアには必携かもしれませんが、カジュアルユーザには不要かな。
    - [ネットワークエンジニアとして：Ethernet LAN - DIX / IEEE](https://www.infraexpert.com/study/ethernet4.html "LINK") - イーサネットフレームのフォーマット。
    - [UIC MACアドレス検索](https://uic.jp/mac/ "LINK") - MACアドレスのOUI（Organizationally Unique Identifier)と製造会社の対応検索ツール。
    - [IEEE OUI/MA-L](http://standards-oui.ieee.org/oui/oui.txt "LINK") - IEEEの公式ドキュメントです。
- ARP
    - [IETF RFC 826](https://datatracker.ietf.org/doc/html/rfc826 "LINK") - 仕様です。
    - [@IT 第11回　MACアドレスを解決するARPプロトコル](https://atmarkit.itmedia.co.jp/ait/articles/0305/09/news003_2.html "LINK") - ARPメッセージのフォーマット。RARP/GARP共通。
    - [IANA Address Resolution Protocol (ARP) Parameters](https://www.iana.org/assignments/arp-parameters/arp-parameters.xhtml "LINK") - ARPの各種パラメータの値の公式文書。
    - [IETF RFC 5227](https://datatracker.ietf.org/doc/html/rfc5227.txt "LINK") - パケットキャプチャには大量のARPが観察されますが、これはIPアドレスの衝突を検出するためのものです。このRFCはその仕様です。
- ツール
    - [Microsoft Docs: arp](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/arp "LINK") - Unixでも同名です。
    - [Microsoft Docs: getmac](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/getmac "LINK") - Unixにはありまん。`ifconfig`を使います。
    - [Microsoft Docs: ipconfig](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig "LINK") - Unixでは`ifconfig`です。
    - [Microsoft Docs: ping](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/pin "LINK") - Unixでもおなじコマンド名ですが、オプションが激しく異なるので混乱します。

まずはイーサネットフレームとARPメッセージのフォーマットを見てみましょう。


### 自機のMACアドレス

自機に装備されているすべてネットワークインタフェースカード（NIC: Network Interface Card）のMACアドレスは、`getmac`から取得します。

```
C:\temp> getmac/v                                              # /vは詳細情報表示オプション
```

> MACアドレスは二桁の16進数を6個（6×8=48バイト分）を連結して表現されますが、アルファベットの`a-f`は大文字小文字のどちらでもよく、また間の記号は`-`でも`:`でもかまいません。講師は小文字と`:`が好きです。
>
> MACアドレスはNICに製造時に刻印されたものなので、手動で変更することはまずありません（できるものもありますが）。しかし、[VMware](https://www.vmware.com/products/workstation-player.html "LINK")などの仮想環境は仮想ネットワークの仮想NICを作成するので、自分で勝手に作成することもできます。

IPアドレスとの対応も知りたいなら、`ipconfig`が便利です。

```
C:\temp> ipconfig/all                                          # /allは詳細情報表示オプション
```


### ARPテーブルの操作

現在、自機に収容されているIPアドレス-MACアドレス対応表は`arp`から操作します。この対応表をARPテーブル（ARP table）、それぞれの対応情報をエントリ（entry）といいます。

まず、現在収容されているARPテーブルを確認します。

```
C:\temp arp -a                                                 # -aはARPテーブルすべてのエントリを表示
```

- 動的: ローカルのIPアドレスを使用したときに起動したARPプロトコルが取得した情報。再起動すれば消えます。稼働中に対応が変更されるのは、NICを入れ替えた、あるいはIPアドレスを変更したときくらいです。
- 静的: あらかじめ定められた（あるいは算出できる）IPアドレス-MACアドレス対応。`arp -s`から設定することもできますが、デフォルトで見られるはシステムが自動的に生成したものです。

続いて、すべてのエントリを消去します。これで、次にローカルネットワーク上のホストにアクセスすれば、ARPの動作が見られます（ARPテーブルに対応がすでにあればその情報が使われるのでARPは起動しません）。

```
C:\temp> arp -d *                                              # すべてのエントリを削除
C:\temp> arp -a                                                # すべて消去されたかを確認
```

ここで、Wiresharkのフィルタに`arp`または`eth.type == 0x0806`を指定し、キャプチャを開始します。ARPテーブルに存在しないデフォルトゲートウェイに`ping`を送ると、そのMACアドレスを調べるために、ARP要求と応答が往来します。

```
C:\temp> ping 192.168.1.254                                    # arp -aあるいはipconfigの情報を使います
```

再度、テーブルを確認するとデフォルトゲートウェイのIPアドレスとMACアドレスの組が再生されていることが確認できます。

```
C:\temp> arp -a                                                # 再生を確認
```


### EthernetとARPプロトコル

#### ARP要求

PCからローカルネットワークにブロードキャストしたフレームです。

```
Ethernet II, Src: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8), Dst: Broadcast (ff:ff:ff:ff:ff:ff)
    Destination: Broadcast (ff:ff:ff:ff:ff:ff)
        Address: Broadcast (ff:ff:ff:ff:ff:ff)
        .... ..1. .... .... .... .... = LG bit: Locally administered address (this is NOT the factory default)
        .... ...1 .... .... .... .... = IG bit: Group address (multicast/broadcast)
    Source: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
        Address: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Type: ARP (0x0806)
```

- これはIEEE 802.3基本フレームの形式です（普通に使われているもの）。VLANではQ-tag（IEEE 802.1Q）が含まれるのでやや形式が異なります。
- 宛先は`ff:ff:ff:ff:ff:ff`なのでローカルネットワークへのブロードキャストです。
- 送信元はこのPCのMACアドレスです。先頭3バイトが文字列表記（IntelCor_）なのは、WiresharkがOUIを製造会社名に変換しているからです。
- G/Lビット: MACアドレスの先頭バイトの2ビット目（右から2番目）のビット。Global/Localの区別。0ならグローバル（登録済み）、1ならローカル（未登録）。Wiresharkはひっくり返してLGという理由は不明。
- I/Gビット: MACアドレスの先頭バイトの1ビット目（右から1番目。LSB）のビット。Individual/Group区別。0なら個別（ユニキャスト）、1ならグループ（マルチキャスト）。
- EthernetヘッダのEtherTypeフィールドの2バイト値が`0x8006`なので、Wiresharkが解釈した通りに、これはARPパケットです。IPv4パケットなら`0x8000`です。

こちらは、そのフレームのペイロードに収容されているARPメッセージです。

```
Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
    Sender IP address: 192.168.1.80
    Target MAC address: 00:00:00_00:00:00 (00:00:00:00:00:00)
    Target IP address: 192.168.1.254
```

- 最初の5行がARPヘッダです。
    - ハードウェアの形式（ここではEthernet）とアドレス長が含まれているのは、ARPをEthernet以外のネットワークハードウェアでも動作させるためです。たとえば、その昔Apple製品で使っていたLocalTalk（AppleTalk）なら11番です。
    - 上位層（ここではIP）も同様で、他のネットワーク層プロトコルを利用するためです。値は上記のEthettypeとおなじものが流用されます。
    - Opcodeが1なので、これは「このIPアドレスのMACアドレスを教えてください」というARP要求です。
- 残りはデータです。ハードウェアとプロトコルのアドレス長さがそれぞれ6、4バイトなので、送信元と宛先の分で`(6 + 4) * 2`で20バイトです。
    - 宛先IPアドレスフィールドに指定されている`192.168.1.254`が、対応するMACアドレスを知りたいIPアドレスです。

#### ARP応答

要求に応えてルータがPCに直接返送したフレームです。Sender MAC addressからMACアドレスがわかります。

```
Ethernet II, Src: Arcadyan_46:d6:52 (f0:86:20:46:d6:52), Dst: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
    Destination: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
        Address: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Source: Arcadyan_46:d6:52 (f0:86:20:46:d6:52)
        Address: Arcadyan_46:d6:52 (f0:86:20:46:d6:52)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Type: ARP (0x0806)
    Padding: 000000000000000000000000000000000000
Address Resolution Protocol (reply)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: reply (2)
    Sender MAC address: Arcadyan_46:d6:52 (f0:86:20:46:d6:52)
    Sender IP address: 192.168.1.254
    Target MAC address: IntelCor_80:4b:e8 (8c:c6:81:80:4b:e8)
    Target IP address: 192.168.1.80
```

- EthernetフレームのPaddingはフレーム長を、Ethernet規格で定められている最小長の64バイトにするために送信元のNICが加えたものです。Wiresharkは60バイトだといっていますが、これは末尾にあるFCSという4バイトのフィールドを除いて報告しているからです。Intelのチップがこの最小長を守っていない理由はわかりません（短いフレームrunt frameと呼ばれて嫌われています）。


### 特殊アドレス

`arp`の実行で表示される各種の特殊アドレスを以下に示します。

IPアドレス | MACアドレス | 意味
---|---|---
169.254.255.255 | ff:ff:ff:ff:ff | APIPAブロードキャスト（Automatic Private IP Addressing）。[RFC 3927](https://datatracker.ietf.org/doc/html/rfc3927 "LINK")参照。
224.0.0.2 | 01:00:5e:00:00:02 | All Routers on this Subnet
224.0.0.22 | 01:00:5e:00:00:16 | IGMP（Interent Group Management Protocol）。[IGMP（Wikipedia）](https://ja.wikipedia.org/wiki/Internet_Group_Management_Protocol "LINK")参照。
224.0.0.251 | 01:00:5e:00:00:fb | mDNS（Multicast DNS）。[RFC 6762](https://www.rfc-editor.org/rfc/rfc6762.html "LINK")参照。
224.0.0.252 | 01:00:5e:00:00:fc | LLMNR（Link-local Multicast Name Resplution）。[RFC 4795](https://www.rfc-editor.org/rfc/rfc4795.html "LINK")参照。
239.255.255.250 | 01:00:5e:7f:ff:fa | SSDP（Simple Service Discovery Protocol）。1999年に提案されたがまだドラフト段階<sup>\*</sup>。
255.255.255.255 | ff:ff:ff:ff:ff:ff | リミテッドブロードキャスト

- リンクローカルIPアドレス（169.254.0.0~169.254.255.255あるいは169.254.0.0/16）は、そのリンク（ローカルネットワーク）でしか使用できないIPアドレスです（プライベートIPアドレスのようなもの）。
- IPマルチキャストアドレス（224.0.0.0~239.255.255.255あるいは224.0.0.0/4）は、「登録」している複数の相手にひとつのアドレスで同報ができるメカニズムです。マルチキャストの仕様は[RFC 1112](https://www.rfc-editor.org/rfc/rfc1112.html "LINK")参照。
- IANA/IETFに登録されているマルチキャストIPアドレス一覧は、[IANA IPv4 Multicast Address Space Registry](https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml "LINK")参照。
- マルチキャストIPアドレスからマルチキャストMACアドレスを得る方法は、[Multicast MAC Address](https://www.infraexpert.com/study/multicastz04.html "LINK")参照。

<sup>\*</sup> インターネットの仕様書であるRFCはたいてい、ドラフト（draft）として試案が提出され、議論（comments）を経て正式な仕様（RFC）となる。なかには、ドラフトのまま使われているものもある。
