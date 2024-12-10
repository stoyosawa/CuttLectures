## Q & A

### HTTPSのペイロードを見たい

SSL/TLSで暗号化されているHTTPSトラフィックは、鍵がないと解読できません。鍵（pre-master secret）を入手する方法は、東陽テクニカさんの「[SSL/TLSの復号#1 ～Wiresharkの設定～](https://www.toyo.co.jp/onetech_blog/articles/detail/id=36994 "LINK")」がわかりやすいです。

Pre-master secretについては、SSL/TLSネゴシエーション上のどこで使われているかは「[SSL/TLS session negotiation](https://www.infraexpert.com/study/security28.html "LINK")」が、計算方法は「[TLS, Pre-Master Secrets and Master Secrets](https://www.cryptologie.net/article/340/tls-pre-master-secrets-and-master-secrets/ "LINK")」（英）がわかりやすいでしょう。

プロトコルを限れば、[`curl`](https://curl.se/ "LINK")でSSL/TLSトラフィックの中身を見ることができます。コマンドオプションに`--trace-ascii -`を加えるだけです。

```
$ curl -s --trace-ascii - https://www.cutt.co.jp/
== Info:   Trying 49.212.180.206:443...
== Info: TCP_NODELAY set
== Info: Connected to www.cutt.co.jp (49.212.180.206) port 443 (#0)
== Info: ALPN, offering h2
== Info: ALPN, offering http/1.1
== Info: successfully set certificate verify locations:
== Info:   CAfile: /etc/ssl/certs/ca-certificates.crt
  CApath: /etc/ssl/certs
=> Send SSL data, 5 bytes (0x5)
0000: .....
== Info: TLSv1.3 (OUT), TLS handshake, Client hello (1):
=> Send SSL data, 512 bytes (0x200)
0000: ......#J..H.~^.........jj.p.7HLNg..... ...y...'E..5...cku.,jT...
0040: .ex..W..>.......,.0.........+./...$.(.k.#.'.g.....9.....3.....=.
0080: <.5./.....u.........www.cutt.co.jp........................3t....
00c0: .....h2.http/1.1.........1.....*.(..............................
0100: ...........+........-.....3.&.$... o..#..nJ.........N...)..+ fB.
0140: _...............................................................
0180: ................................................................
01c0: ................................................................
<= Recv SSL data, 5 bytes (0x5)
0000: ....f
== Info: TLSv1.3 (IN), TLS handshake, Server hello (2):
︙
```

