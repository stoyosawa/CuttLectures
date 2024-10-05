#!/usr/bin/env python
# GeoJSONから地図を生成する（Originally from 『Webスクレイピング～Pythonによるインターネット情報活用術』）。

import sys
import plotly.express as px
import requests


def get_page(url):
    resp = requests.get(url, headers={'Accept': 'application/json'})
    if resp.status_code != 200:
        raise Exception(f'HTTP failure. Code {resp.status_code}.')

    resp.encoding = resp.apparent_encoding

    print(f'{url} loaded. {len(resp.text)} chars.', file=sys.stderr)
    return resp.json()


def extract_locations(json_body):
    geo_info = []
    for features in json_body['features']:
        geo_info.append(
            {
                '緯度': float(features['geometry']['coordinates'][1]),
                '経度': float(features['geometry']['coordinates'][0]),
                '施設名': features['properties']['タイトル'],
                '住所': features['properties']['所在地']
            }
        )    

    print(f'JSON data loaded. {len(geo_info)} elements yanked.', file=sys.stderr)
    return geo_info


def generate_map(geo_info):
    fig = px.scatter_mapbox(
       data_frame = geo_info,
        lat = '緯度',
        lon = '経度',
        hover_name = '施設名',
        center = {'lat':35.65915518488515, 'lon':139.74528644617095},   # 東京タワー,
        zoom = 14,
        mapbox_style='open-street-map',
        opacity=0.5
    )                            
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title_text="港区区役所"
    )
    fig.update_traces(marker={'size': 20, 'color': 'red', 'opacity': 0.5})

    return fig



if __name__ == '__main__':
    url = 'https://opendata.city.minato.tokyo.jp/dataset/74c06ebb-47dd-4fe1-8ba7-a5be60d2a448/resource/f1a1056b-a00e-4c12-8a78-288e0eee7ba0/download/minatokushisetsujoho_kuyakusyo.json'
    json_data = get_page(url)
    geo_info = extract_locations(json_data)
    fig = generate_map(geo_info)
    # fig.show()
    fig.write_html('json_geo.html')
