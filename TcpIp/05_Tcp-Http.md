## TCPとHTTP

本章ではHTTP（Hypertext Transfer Protocol）を通じて、TCPの挙動を観察します。

HTTPはハイパーテキスト（たいていはHMTL）を搬送するアプリケーション層（L7）のプロトコルです。信頼性のある通信路で搬送されることが想定されているのでトランスポート層（L4）のプロトコルにはTCPを使います。


### 仕様・参考文献

- TCP
	- [IETF RFC 9293](https://datatracker.ietf.org/doc/html/rfc9293 "LINK") - 仕様。つい最近、RFC 791が無効化されました！
	- [Network Sorcery: TCP](http://www.networksorcery.com/enp/protocol/tcp.htm) - セグメント構造と各種パラメータだけならこちら。
	- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.txt "LINK") - TCP/UDPウェルノウンポート番号の一覧。	
	- [ネットワークエンジニアとして：TCP/IP - TCP three-way handshaking](https://www.infraexpert.com/study/tcpip9.html "LINK") - 3Wayハンドシェイクのわかりやすい概要。
	- [@Network TCPの制御（スリーウェイハンドシェイクの手順）](http://atnetwork.info/tcpip/tcpip101.html "LINK") - TCP 3-wayハンドシェイクの仕組み。
- HTTP/1.1
	- [IETF RFC 2616](https://datatracker.ietf.org/doc/html/rfc2616 "LINK") - 仕様。本当はRFC 9110～9112によって無効化（旧式化）されたのですが、本筋は変わらないので、えらく細かいところを気にしないのであればこちらで充分です。
    - [MDN HTTPレスポンスステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status "LINK") - 「200 OK」や「404 Not Found」など、ご存じのHTTPレスポンスコードの一覧です。
- ツール
    - [Microsoft Docs: netstat](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/netstat "LINK") - Unixでも同名です。

まずはTCPセグメントのフォーマットを見てみましょう。


### 使用中のポート番号を調べる

コマンドプロンプトから`netstat`を次の要領で実行し、返す刀で即座にWebブラウザから`http://www.cutt.co.jp`にアクセスします。

> HTTPはデータが取得されると即座にTCPコネクションを切断するので、ブラウザの読み込みとコマンドの実行がシンクロしていないとアソシエーションは表示されません。

```
C:\temp> netstat -n

アクティブな接続

  プロトコル  ローカル アドレス      外部アドレス           状態
  TCP         127.0.0.1:51004        127.0.0.1:51173        ESTABLISHED
...  
  TCP         192.168.1.80:51306     49.212.180.206:80      TIME_WAIT
...
```

ポート番号は16ビット長なので、値の範囲は0～65535です。

- 0~1023: ウェルノウンポート（あるいはシステムポート）。HTTPやSMTPなど一般的なサービスにあらかじめ割り当てられている番号。IANAが厳密に管理しています。
- 1024～49151: 登録済みポート（あるいはユーザポート）。一応IANAが管理してはいるものの、勝手に使ったからといって（たぶん）お目玉は食らわない番号。
- 49152～65535: 動的ポート。クライアント側のポート番号のように一時的（ephemeral）に用いるのに用いられます。


### 3Wayハンドシェイク

Wiresharkのフィルタを`http`または`tcp.port == 80`を指定し、ブラウザから`http://www.cutt.co.jp/about/index.html`にアクセスします。まっさらな状態での通信を観察したいので、ブラウザのキャッシュはクリアしておきます。

#### SYN

TCPコネクションを確立するクライアントは、サーバに対しTCP SYNパケットを送ります。

```
Transmission Control Protocol, Src Port: 54976, Dst Port: 80, Seq: 0, Len: 0
    Source Port: 54976
    Destination Port: 80
    Sequence Number: 0    (relative sequence number)
    Sequence Number (raw): 2648756644
    Acknowledgment Number: 0
    Acknowledgment number (raw): 0
    1000 .... = Header Length: 32 bytes (8)
    Flags: 0x002 (SYN)
    Window: 64240
    Checksum: 0xa8c1 [unverified]
    Urgent Pointer: 0
    Options: (12 bytes), Maximum segment size, No-Operation (NOP), Window scale, No-Operation (NOP), No-Operation (NOP), SACK permitted
```

- 送信元と宛先のポートはそれぞれ54928と80です。80はHTTPのウェルノウンポートです。
- Flagsフィールド（仕様ではControl bits）から、このセグメントに制御的なタスクが課せられているかわかります。ここでは最初のコネクション確立のSYNビットが立っています。
- TCPではセグメントの各バイトに番号を付けて、TCP Sequence Numberフィールドで管理しています（これで、どこか欠けたり重複したりしたらわかる）。最初の番号はなんでもよいのですが、たいていランダムにセットされます。ここでは2648756644です。2行ありますが、relative（相対）のほうはWiresharkのサービスです。

#### SYN/ACK

サーバ側は上記のSYNに確認応答（ACK）を送ると同時に、自分のSYNで自分側の送信データのほうのコネクションの確立を図ります。

```
Transmission Control Protocol, Src Port: 80, Dst Port: 54976, Seq: 0, Ack: 1, Len: 0
    Source Port: 80
    Destination Port: 54976
    Sequence Number: 0    (relative sequence number)
    Sequence Number (raw): 1870694100
    Acknowledgment Number: 1    (relative ack number)
    Acknowledgment number (raw): 2648756645
    1000 .... = Header Length: 32 bytes (8)
    Flags: 0x012 (SYN, ACK)
    Window: 65535
    Checksum: 0x8a84 [unverified]
    Urgent Pointer: 0
    Options: (12 bytes), Maximum segment size, No-Operation (NOP), Window scale, SACK permitted, End of Option List (EOL)
```

- SYN側のデータはSequence Numberフィールドです。ここでは、1870694100が用いられています。
- ACK側のデータはAcknowledgment numberで、2648756645です。この値は先ほどのSYNのときより一つ多い値です。これで上記のTCP SYNは確認されました。

#### ACK

```
Transmission Control Protocol, Src Port: 54976, Dst Port: 80, Seq: 1, Ack: 1, Len: 0
    Source Port: 54976
    Destination Port: 80
    Sequence Number: 1    (relative sequence number)
    Sequence Number (raw): 2648756645
    Acknowledgment Number: 1    (relative ack number)
    Acknowledgment number (raw): 1870694101
    0101 .... = Header Length: 20 bytes (5)
    Flags: 0x010 (ACK)
    Window: 516
    Checksum: 0xa8b5 [unverified]
    Urgent Pointer: 0
```

- 上記のTCP SYN/ACKのSYN部分を確認応答しています。Acknowledgment Numberは1870694101で、こちらも上記の+1の値です。


### HTTP

TCP 3-wayハンドシェイクが完了すれば、つぎはHTTPの出番です。

> 最近のWebサーバの大半はHTTPS（ポート番号443）を用いており、ピュアにHTTSのものは少なくなっています。

```
No.	Time		Source			SrcPort	Destination		DstPort	Proto	Length	Info
133	4.815457	192.168.1.80	55524	49.212.180.206	80		HTTP	425		GET /about/index.html HTTP/1.1 
134	4.962406	49.212.180.206	80		192.168.1.80	55524	TCP		60		[TCP Window Update] 80 → 55524 [ACK] Seq=1 Ack=1 Win=132096 Len=0
135	4.963369	49.212.180.206	80		192.168.1.80	55524	TCP		1506	80 → 55524 [ACK] Seq=1 Ack=372 Win=132096 Len=1452 [TCP segment of a reassembled PDU]
136	4.963369	49.212.180.206	80		192.168.1.80	55524	TCP		1506	80 → 55524 [ACK] Seq=1453 Ack=372 Win=132096 Len=1452 [TCP segment of a reassembled PDU]
137	4.963369	49.212.180.206	80		192.168.1.80	55524	TCP		1506	80 → 55524 [ACK] Seq=2905 Ack=372 Win=132096 Len=1452 [TCP segment of a reassembled PDU]
138	4.963410	192.168.1.80	55524	49.212.180.206	80		TCP		54		55524 → 80 [ACK] Seq=372 Ack=4357 Win=132096 Len=0
139	5.110104	49.212.180.206	80		192.168.1.80	55524	HTTP	483		HTTP/1.1 200 OK  (text/html)
140	5.119282	192.168.1.80	55524	49.212.180.206	80		HTTP	379		GET /favicon.ico HTTP/1.1 
141	5.268662	49.212.180.206	80		192.168.1.80	55524	HTTP	418		HTTP/1.1 404 Not Found  (text/html)
142	5.316413	192.168.1.80	55524	49.212.180.206	80		TCP		54		55524 → 80 [ACK] Seq=697 Ack=5150 Win=131328 Len=0
```

ブラウザはページ要求のGET要求をサーバに送ります（上記ではNo. 133）。HTTPはテキストベースのコマンド体系を採用しているので、以下に示された要求に付随するHTTPヘッダはすべてそのまま送信されています（IPやTCPのようにWiresharkが解釈した結果ではありません）。

```
Hypertext Transfer Protocol
    GET /about/index.html HTTP/1.1\r\n
    Host: www.cutt.co.jp\r\n
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0\r\n
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n
    Accept-Language: ja,en-NZ;q=0.7,en;q=0.3\r\n
    Accept-Encoding: gzip, deflate\r\n
    Connection: keep-alive\r\n
    Upgrade-Insecure-Requests: 1\r\n
    \r\n
```

No. 135から139の5セグメントがサーバからの応答データ（HTMLテキスト）です。大きなデータを一気に流し込んでいるので、TCPソフトウェアが自動的に複数のTCPセグメントに分割して送信しています。それぞれのセグメントでもデータは読めますが、最後（No. 139）にまとめて示されてます。ちなみに、HTTPヘッダも含めて総データサイズは4785バイトです。HTMLページ部分のサイズはContent-Length: フィールドからわかります。

```
Hypertext Transfer Protocol
    HTTP/1.1 200 OK\r\n
    Server: nginx\r\n
    Date: Sun, 21 Nov 2021 02:38:39 GMT\r\n
    Content-Type: text/html\r\n
    Content-Length: 4547\r\n
    Connection: keep-alive\r\n
    Last-Modified: Thu, 08 Aug 2019 08:18:00 GMT\r\n
    ETag: "11c3-58f96b2221e00"\r\n
    Accept-Ranges: bytes\r\n
    \r\n
```    

Connection: keep-aliveというヘッダがあるので、このTCPコネクションはこのページ以外のデータの搬送に再利用できます。それが、No. 140のfavicon要求です。

faviconはブラウザのバーに表示される非常に小さいアイコンです。ブラウザによっては、どこにアクセスしようとそのサイトのアイコンが`/favicon.ico`と仮定してそれを要求するものもあります。この場合、サーバーは持ち合わせがないため、404を返しています。


### TCPコネクションの切断

`/about/index.html`と`/favicon.ico`の転送要求が終わったので、コネクションを切断します。これには通信ペアのどちらかからTCP FINパケットを送ります。それを受信した相手は、それを確認（ACK）するとともに、こちらも終了することを告げるために同様にFINを送ります。

ここでは、最後の通信（favicon要求）から5秒ほど経過したので、サーバ側がクライアントに追加要求はないと判断して先行して切断しています。

```
284	10.271621	49.212.180.206	80		192.168.1.80	55524	TCP		60		80 → 55524 [FIN, ACK] Seq=5150 Ack=697 Win=132096 Len=0
285	10.271810	192.168.1.80	55524	49.212.180.206	80		TCP		54		55524 → 80 [ACK] Seq=697 Ack=5151 Win=131328 Len=0
286	10.272059	192.168.1.80	55524	49.212.180.206	80		TCP		54		55524 → 80 [FIN, ACK] Seq=697 Ack=5151 Win=131328 Len=0
288	10.419838	49.212.180.206	80		192.168.1.80	55524	TCP		60		80 → 55524 [ACK] Seq=5151 Ack=698 Win=132096 Len=0
```
