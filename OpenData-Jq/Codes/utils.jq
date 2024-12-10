# Utility functions for Public Wifi Accesspoint data from Tokyo Open Data API
#  https://portal.data.metro.tokyo.lg.jp/opendata-api/
# 2023-02-13: (c) Satoshi Toyosawa


# Input (.) is an array of two-element arrays consisiting of [経度(Longtitude), 緯度(Latitude)].
# The Unit is in degree.
# See also: https://keisan.casio.jp/exec/system/1257670779
#
# For test:
# jq -n 'include "utils"; [ [139.5607125, 35.7027021], [139.710121, 35.693105]] | distance'

def distance:
    (3.14159265358979323846 / 180) as $to_radian |  # m_pi from math.h
    6378.137 as $radius |
    (.[0] | map(. * $to_radian)) as $rad1 |
    (.[1] | map(. * $to_radian)) as $rad2 |
    ($rad2[0] - $rad1[0]) as $delta |
    ($rad1[1] | sin) * ($rad2[1] | sin) + ($rad1[1] | cos) * ($rad2[1] | cos) * ($delta | cos) |
    acos * $radius;


# stats (equivalent to 'uniq -c')

def district_count:
    [
        .[0][]."設置地点"."住所"."表記" |
        if startswith("東京都") then
            .[3:]
        else
            .
        end |
        split("[区市村]"; "g")[0]
    ] as $input |
    $input |
    unique |
    map(
        . as $element |
        $input | map(select(. == $element)) | length |
        {($element): .}
    ) |
    add;

