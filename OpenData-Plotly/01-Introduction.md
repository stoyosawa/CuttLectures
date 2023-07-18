##  はじめに

データ形式である[GeoJSON](https://ja.wikipedia.org/wiki/GeoJSON)と、データソースの[東京都 オープンデータカタログサイト](https://portal.data.metro.tokyo.lg.jp/)について簡単に説明します。


### GeoJSON

おおまかなところは、[Wikipediaの記事](https://ja.wikipedia.org/wiki/GeoJSON)でわかります。と言うか、データを利用するだけなら細かいことは気にしなくてもかまいません。位置（緯度経度）は、`features`配列要素の`geometry`プロパティの`coordinates`属性に収容されていることだけわかっていれば大丈夫です。

```json
{
  "type": "FeatureCollection",
  "features": [                                     # 配列。ここに複数の位置情報が収容されている。
    {
      "type": "Feature",
      "geometry": {                                 # 位置情報
        "type": "Point",                            # この情報の示す位置の形状
        "coordinates": [
          "139.75163",                              # 経度
          "35.658203",                              # 緯度
          0                                         # 高度（ないこともある）
        ]
      },
      "properties": {
        "タイトル": "港区役所",
        "分類": "区役所",
        "地区": "芝地区",
        "所在地": "港区芝公園一丁目5番25号",
        "連絡先": "電話：03-3578-2111（代表） ファックス：03-3578-2034",
        "URL": "<a href='https://www.city.minato.tokyo.jp/ ... 中略 ... /01.html</a>"
      }
    },
    ...
  ]
}
```

> どうでもいいけど、まだ、ファックスあるんですね ...

位置情報のタイプ（形状）には、点を示すPoint、点の集合からなるLineString、これを閉区間にしたPolygonがあります（後述）。

GeoJSONのおおもとであるJSON（JavaScript Object Notation）ですが、Pythonから利用するときは次の対応関係を把握していればおおむね問題はありません。

<table border="0">
 <tr><th colspan="2">JSON</th> <th colspan="2">Python</th></tr>
 <tr><th>型</th><th>例</th><th>型</th><th>例</th></tr>
 <tr><td><tt>null</tt></td><td><tt>null</tt></td><td><tt>None</tt></td><td><tt>None</tt></td></tr>
 <tr><td>真偽値</td><td><tt>true、false</tt></td><td><tt>bool</tt></td><td><tt>True、False</tt></td></tr>
 <tr><td>数値</td><td>400、3.14、6.67e-11</td><td><tt>float</tt></td><td>400、3.14、6.67e-11</td></tr>
 <tr><td>文字列</td><td>"牛めし"</td><td><tt>str</tt></td><td>'牛めし'</td></tr>
 <tr><td>配列</td><td>["ごはん", "牛肉", "玉ねぎ"]</td><td><tt>list</tt></td><td>['ごはん', '牛肉', '玉ねぎ']</td></tr>
 <tr><td>オブジェクト</td><td>{"name": "牛めし"}</td><td><tt>dict</tt></td><td>{'name': '牛めし'}</td></tr>
</table>

JSONテキストとPythonオブジェクトの相互変換には、標準ライブラリの[`json`](https://docs.python.org/ja/3/library/json.html)を使います。

仕様はRFCで定義されています。

- [RFC 7158: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/info/rfc7158)
- [RFC 7946: The GeoJSON Format](https://www.rfc-editor.org/info/rfc7946)


### 東京都 オープンデータカタログサイト

[東京都 オープンデータカタログサイト](https://portal.data.metro.tokyo.lg.jp/)のトップページはこちらです。

```https://portal.data.metro.tokyo.lg.jp/```

［データを探す］をクリックすれば、現在収容されている全データセット（の一部）が表示されます。左パネルの［フォーマット］から「GeoJSON」でフィルタリングすれば、41件のデータセットが見られます。演示では次の3つのデータセットを使います。

- `Point`: [港区の公共施設情報 区役所・総合支所](https://catalog.data.metro.tokyo.lg.jp/dataset/t131032d0000000014) ... 7点。
- `LineString`: [避難道路](https://catalog.data.metro.tokyo.lg.jp/dataset/t131091d0000000139)（品川区）... 2線。
- `Polygon`: [地区内残留地区](https://catalog.data.metro.tokyo.lg.jp/dataset/t131091d0000000135)（品川区）... 6区域。なお、[「地区内残留地区」](https://www.city.shinagawa.tokyo.jp/PC/bosai/bosai2/jishin/hpg000019726.html)とは、「震災時における市街地大火の危険性が少ないことから、避難の必要がないとみなされた地区」らしいです。

リンクをたどれば、ブラウザ上にGeoJSONデータが表示されます。ブラウザによっては、整形して示してくれます（e.g., Firefox）。整形機能がなければ、外部のプラグインを導入してください。

> HTTP応答にデータ種別（`Content-type`）が示されていないと、もとのプレーンテキストで表示されます。いったん保存し、ファイル名に`.json`の拡張子を加えてから開きます。

[`jq`](https://jqlang.github.io/jq/)という、コマンドラインでJSONを整形・表示するツールも便利です。[`curl`](https://curl.se/docs/manpage.html)と組み合わせることで、コマンドラインだけでちゃくっとデータの中身を確認できます。

```bash
$ URL=https://opendata.city.minato.tokyo.jp/dataset/74c06ebb-47dd-4fe1-8ba7-a5be60d2a448/resource/f1a1056b-a00e-4c12-8a78-288e0eee7ba0/download/minatokushisetsujoho_kuyakusyo.json
$ curl $URL | jq -r '.features[] | .geometry.coordinates + [.properties."タイトル"] | join(", ")'
139.75163, 35.658203, 0, 港区役所
139.751576, 35.658185, 0, 芝地区総合支所
139.735091, 35.660657, 0, 麻布地区総合支所
139.731725, 35.674775, 0, 赤坂地区総合支所
139.734045, 35.642076, 0, 高輪地区総合支所
139.751501, 35.646408, 0, 芝浦港南地区総合支所
139.777312, 35.629723, 0, 芝浦港南地区総合支所台場分室
```

興味ある方は、[『オープンデータの活用～JSON＋jqパーザ』](https://github.com/stoyosawa/CuttSeminars/blob/main/OpenData-Jq/README.md)というセミナーもあるので、聴講してみてください。

