## GeoJSON LineStringデータのプロット

Plotly Expressの`px.line_mapbox()`を使って、地図に線（経路）をマーキングします。線データはGeoJSONのジオメトリタイプ（`features[].geometry.type`）がLineStringであるものです。例題は、品川区の「避難道路」です。

まずはダウンロードです。

```Python
url = 'https://www.opendata.metro.tokyo.lg.jp/shinagawa/hinandoro.geojson'
resp = requests.get(url)
```

しかし、このままでは文字化けします。HTTP応答ヘッダには中身がただのテキスト（`text/plain`）とあり、また文字エンコーディング情報が未指定なので、デフォルトでISO-8859-1と解釈されてしまうからです。そこで、文字エンコーディングをUTF-8に強制します。

```Python
>>> resp.headers['Content-Type']
'text/plain'
>>> resp.encoding
'ISO-8859-1'
>>> resp.encoding = 'utf-8'
```

JSONに変換します。

```Python
json_body = resp.json()
```

中には、全部で2つの`features`（線）があります。


```Python
>>> len(json_body['features'])
2
```

中身を0番目の要素から確認します。ポイントは、線の位置情報は点（Point）が複数含まれた配列であるところと、ジオメトリタイプがLineStringであるところです。

```Pythom
>>> pprint(json_body['features'][0])
{'geometry': {'coordinates': [[139.73642484220247, 35.59488111889783],
                              [139.7365831458941, 35.59529876730483],
                              [139.73675449728765, 35.59569677575642],
                              ...
                              [139.74306922121434, 35.60666790197767],
                              [139.74307598964577, 35.606734519224744]],
              'type': 'LineString'},
 'properties': {'種別': '避難道路'},
 'type': 'Feature'}
```

この0個目の線には22点があります。つまり、21本の線分からなる経路です。

```Python
>>> len(json_body['features'][0]['geometry']['coordinates'])
22
```

どの`features`要素もLineStringであるかを確認します。

```Python
>>> set([feature['geometry']['type'] for feature in json_body['features']])
{'LineString'}
```

GeoJSONデータから線番号（0または1）、緯度、経度の表を作成します。

```Python
geo_info = []
for idx, feat in enumerate(json_body['features']):
    for cord in feat['geometry']['coordinates']:
        geo_info.append(
            {
                'id': idx,
                '経度': cord[0],
                '緯度': cord[1]
            }
        )
```

中身を確認します。

```Python
>>> pprint(geo_info)
[
 {'id': 0, '経度': 139.73642484220247, '緯度': 35.59488111889783},
 {'id': 0, '経度': 139.7365831458941, '緯度': 35.59529876730483},
 ...
 {'id': 1, '経度': 139.74135409191086, '緯度': 35.596165848738295},
 {'id': 1, '経度': 139.73994441754567, '緯度': 35.596389659984425},
 ...
]
```

あとは、`px.line_mapbox()`で描画するだけです。要領は`px.scatter_mapbox()`と同じです。

```Python
fig = px.line_mapbox(
    data_frame=geo_info,
    lat='緯度',
    lon='経度',
    color='id',
    mapbox_style='stamen-terrain',
    center = {'lat':35.593444, 'lon':139.743306},   # 大井競馬場
    zoom = 14,
    title='品川区避難道路'
)
```

あとは表示あるいは保存するだけです。

```Python
fig.show()
fig.write_html('EvacuationRoutes.html')
```
