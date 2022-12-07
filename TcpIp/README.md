# TCP/IPネットワーキング & パケットキャプチャ

### 本セミナーの目標

中級以上を目指すネットワークエンジニアを対象に、インターネットの基盤技術であるTCP/IPの構造と挙動を、パケットキャプチャツール（Wireshark）を用いたパケット解析を通じて具体的に学びます。

セミナーでは、各自のPCに[Wireshark](https://www.wireshark.org/ "LINK")をインストールし、実際に利用してもらいます。対応している環境はWindowsまたはMac OSです。


### プログラム

> 短縮版（90分）は📚のみ扱います。

1. [TCP/IP概要](./01_Basics.md "INTERNAL")
	- [どうやってつながるの？](./01_Basics.md#どうやってつながるの？ "INTERNAL") 📚
	- [OSI参照モデル](./01_Basics.md#OSI参照モデル "INTERNAL")
2. [パケットキャプチャツール](./02_Wireshark.md "INTERNAL") 📚
	- [インストール](./02_Wireshark.md#インストール "INTERNAL") 📚
	- [リブート中](./02_Wireshark.md#リブート中 "INTERNAL") 📚
	- [お試し](./02_Wireshark.md#お試し "INTERNAL") 📚
3. [EthernetとARP](./03_Ethernet-Arp.md "INTERNAL")
	- [仕様・参考文献](./03_Ethernet-Arp.md#仕様・参考文献 "INTERNAL")
	- [自機のMACアドレス](./03_Ethernet-Arp.md#自機のMACアドレス "INTERNAL")
	- [ARPテーブルの操作](./03_Ethernet-Arp.md#ARPテーブルの操作 "INTERNAL")
	- [EthernetとARPプロトコル](./03_Ethernet-Arp.md#EthernetとARPプロトコル "INTERNAL")
	- [特殊アドレス](./03_Ethernet-Arp.md#特殊アドレス "INTERNAL")
4. [IPとICMP](./04_IP-ping.md "INTERNAL")
	- [仕様・参考文献](./04_IP-ping.md#仕様・参考文献 "INTERNAL")
	- [普通にpingを送る](./04_IP-ping.md#普通にpingを送る "INTERNAL")
	- [大きなpingを送る](./04_IP-ping.md#大きなpingを送る "INTERNAL")
	- [フラグメント禁止](./04_IP-ping.md#フラグメント禁止 "INTERNAL")
	- [時間超過](./04_IP-ping.md#時間超過 "INTERNAL")
5. [TCPとHTTP](./05_Tcp-Http.md "INTERNAL")
	- [仕様・参考文献](./05_Tcp-Http.md#仕様・参考文献 "INTERNAL")
	- [使用中のポート番号を調べる](./05_Tcp-Http.md#使用中のポート番号を調べる "INTERNAL")
	- [3Wayハンドシェイク](./05_Tcp-Http.md#3Wayハンドシェイク "INTERNAL")
	- [HTTP](./05_Tcp-Http.md#HTTP "INTERNAL") 📚
	- [TCPコネクションの切断](./06_Tcp-Http.md#TCPコネクションの切断 "INTERNAL")
6. [UDPとDNS](./06_Udp-Dns.md "INTERNAL")
	- [仕様・参考文献](./06_Udp-Dns.md#仕様・参考文献 "INTERNAL")
	- [AおよびAAAAレコードの要求](./06_Udp-Dns.md#AおよびAAAAレコードの要求 "INTERNAL")
	- [DNSキャッシュの操作](./06_Udp-Dns.md#DNSキャッシュの操作 "INTERNAL")


### 質問

質問はチャットウィンドウから適宜受け付けます。口頭で質問したいときは、単に「質問」や🙋と書き込んでください。切りのよいところで指名します。
