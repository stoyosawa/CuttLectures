## GeoJSON Polygonデータのプロット

Plotly Expressの`px.choropleth_mapbox()`を使って、地図に領域情報をマーキングします。

ここで扱うのは「面」情報です。つまり、GeoJSONのジオメトリタイプ（`features[].geometry.type`）がPolygonのものです。例題は、品川区の[「地区内残留地区」](https://www.opendata.metro.tokyo.lg.jp/shinagawa/chikunaizanryuchiku.geojson)です。

まずは、ダウンロードです。前回同様、文字化けには気を付けます。

```Python
url = 'https://www.opendata.metro.tokyo.lg.jp/shinagawa/chikunaizanryuchiku.geojson'
resp = requests.get(url)
resp.encoding = 'utf-8'
json_body = resp.json()
```

全部で5つの`features`（領域）があります。

```Python
>>> len(json_body['features'])
5
```

どれもがPolygonであるかを確認します。

```Python
>>> set([feature['geometry']['type'] for feature in json_body['features']])
{'Polygon'}
```

ひとつ中身を確認します。

```Python
>>> pprint(json_body['features'][0]['geometry']['coordinates'])
[[
  [139.75797216658606, 35.61889961946038],
  [139.75797241070856, 35.6188747414995],
  ...
  [139.75792061780407, 35.618895170440226],
  [139.75797216658606, 35.61889961946038]
]]  
```

`px.choropleth_mapbox()`では、領域情報（上記）とその領域への意味付け（データ）が必要です。ここでは、GeoJSONそのものに含まれている`properties`からデータを用意します。

```Python
>>> pprint(json_body['features'][0]['properties'])
{'Name': 'No evacuation required area Konan & Higashi-shinagawa area',
 'No': '311',
 '人数': '600',
 '名称': '地区内残留 港南・東品川地区'}
```

意味データは、上記から`No`と`人数`のプロパティを抽出して、（これまで同様）辞書形式で作成します。`No`は文字列としますが、人数は色付けに使うので数値に直します。

```Python
df = []
for feat in json_body['features']:
    df.append(
        {
            'No': feat['properties']['No'],
            'Numbers': int(feat['properties']['人数'])
        }
    )
```

確認します。

```Python
>>> pprint(df)
[{'No': '311', 'Numbers': 600},
 {'No': '322', 'Numbers': 16200},
 {'No': '313', 'Numbers': 200},
 {'No': '331', 'Numbers': 7000},
 {'No': '305', 'Numbers': 75000}]
```

位置（領域）情報`geo_info`と意味情報`df`の2つの「表」はこの`No`で関連付けられます。SQLデータベースの`JOIN`の塩梅です。このとき、関連付けるキーの`No`の値は文字列でなければならないという制約があります。

あとは、`px.choropleth_mapbox()`で描画するだけです。要領は前2つのものと同じです。

```Python
fig = px.choropleth_mapbox(
    data_frame=df,
    geojson=json_body,
    featureidkey='properties.No',
    locations='No',
    color='Numbers',
    color_continuous_scale='Viridis',
    opacity=0.5,
    mapbox_style='open-street-map',
    zoom=13,
    center = {'lat':35.628222, 'lon':139.738694},   # 品川駅
)
```

ポイントは、GeoJSON形式の位置情報を`geojson`キーワード引数から、意味データを`data_frame`キーワード引数からそれぞれ指定するところ、そしてそれぞれの「表」のキーの対応付けを`featureidkey`、`locations`キーワード引数から指定するところです。SQLの`JOIN`風に書けば、こんな意味合いです。

```
df.No = json_body.features.No
```

あとは、得られた`fig`（`px.Figure`オブジェクト）からWebブラウザに表示する、あるいはHTMLファイルとして保存するだけです。

```Python
fig.show()
fig.write_html('NoEvacuation.html')
```
