# coding: utf-8

import os
import pathlib
import xmltodict
import package.MojXmlDef as MojXmlDef
import package.MojXmlPolygon as MojXmlPolygon
import package.MojXMLtoGeoJSON as MojXMLtoGeoJSON


def SaveGeoJson(src_file, dst_directory, exclude_flag):
    moj_obj = MojXml(src_file)

    mojGeojson = MojGeojson(moj_obj, exclude_flag)

    if dst_directory is not None:
        path_dst = pathlib.Path(dst_directory).resolve()
        path_dst.mkdir(exist_ok = True)

        if path_dst.is_dir():
            path_src = pathlib.Path(src_file).resolve()
            dst_name = (path_dst / path_src.name).with_suffix(".geojson")
    else:
        # 出力先が指定されていない場合はXMLファイルと同じディレクトリに作成
        dst_name = pathlib.Path(src_file).with_suffix(".geojson").resolve()

    with open(dst_name, 'w', encoding='utf-8') as f:
        f.write(mojGeojson)
        f.close()


# convert xml to object
def MojXml(src_file):
    with open(src_file, encoding='utf-8') as fp:
        xml_data = fp.read()
        moj_dict = xmltodict.parse(xml_data)

    version = moj_dict['地図']['version']
    map_name = moj_dict['地図']['地図名']
    city_code = moj_dict['地図']['市区町村コード']
    city_name = moj_dict['地図']['市区町村名']
    crs = moj_dict['地図']['座標系']
    number_crs, named_crs = MojXmlDef.GetCrs(crs)
    datum_type = moj_dict.get('地図', {}).get('測地系判別')

    mojXmlPolygon = MojXmlPolygon.MojXmlPolygon(moj_dict)

    mojObj = {
        'version': version,
        'map_name': map_name,
        'city_code': city_code,
        'city_name': city_name,
        'crs': crs,
        'named_crs': named_crs,
        'number_crs': number_crs,
        'datum_type': datum_type,
        'mojXmlPolygon': mojXmlPolygon,
    }
    return mojObj


def MojGeojson(mojObj: dict, exclude_flag):
    return MojXMLtoGeoJSON.MojXMLtoGeoJSON(mojObj, exclude_flag)
