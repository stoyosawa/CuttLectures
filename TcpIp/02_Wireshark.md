## パケットキャプチャツール

本章ではパケットキャプチャツールとして（おそらく最も）ポピュラーなWiresharkをインストールします。


### インストール

[Wireshark.org](https://www.wireshark.org/ "LINK")からWindows Installer (64-bit)をダウンロード。とくに制約がなければ最新版を入手します。

インストール手順は[ネットワーク入門サイト Wiresharkの使い方](https://beginners-network.com/wireshark.html "LINK")がわかりやすいと思います。

インストール途中で`Npcap`をインストールするか訊いてくるので、許可します（必須です）。概要は[pcap（Wikipedia）](https://ja.wikipedia.org/wiki/Pcap "LINK")参照。`USBPcap`も勧められます。こちらはUSBの通信をキャプチャするためのもので、本コースでは利用しません。

インストール後は再起動が必要です。


### リブート中

Zoomセッションから退出し、再起動後してください。[10分後](https://vclock.com/set-timer-for-10-minutes/ "LINK")に再集結します。


### お試し

1. Wireshark を起動。
2. インタフェースを選択。電図風のグラフがアクティブなものがたいていはメイン。無線LANを使っていれば`Wi-Fi`を選択。
3. デフォルトでは送受するすべてのパケットが表示されるので、画面が忙しくなります。とりあえず「赤い四角ボタン」を押して、停止します。

> 複数のインタフェースを同時にキャプチャできますが、結果が読みにくくなるので、普通は一つだけ選択します。


#### DNSによる名前解決

1. DNS通信のみ表示するようにフィルタに`dns`または`udp.port == 43`を指定します。
2. [青い背びれボタン]を押して、キャプチャを開始します。
3. コンソールを起動し、DNS名前解決を実行します: `nslookup www.cutt.co.jp`。コンソールはWindowsではコマンドプロンプトまたはWindows Subsystem for Linuxです。
4. 3、4個のパケットが往来したら、「赤い四角ボタン」を押して停止します。
5. Wiresharkの画面から送受信パケットを確認します（仕様はUDPは[RFC 768](https://datatracker.ietf.org/doc/html/rfc768 "LINK")、DNSは[RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035 "LINK")）。


#### HTTP通信

1. HTTP通信のみ表示するようにフィルタに`http`を指定します。
2. [青い背びれボタン]を押して、キャプチャを開始します。
3. HTTP通信をします。
	1. `curl`があれば`curl -D - http://www.cutt.co.jp/about/index.html`（画像がなくてシンプルだから）。
	2. なければブラウザから。
4. 往復のパケットが表示されます。
5. Wiresharkの画面から送受信パケットを確認します。
6. フィルタを`tcp.port == 80`に変更して、2～5を再度実行します。

**TCP segment of a reasembled PDU**は、（この場合）大きなHTTPストリームデータがTCPセグメントに分割されて送信されたことを示します。それぞれのペイロードサイズを足せば、受信したHTMLデータと等しくなります（試してみましょう）。
