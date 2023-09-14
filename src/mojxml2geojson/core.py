# coding: utf-8

import argparse
import traceback
import package.xml2geojson


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('FILE_PATH')
    parser.add_argument('-e', '--exclude', help='地番が地図外、別図の筆を除外して出力', action='store_true')
    parser.add_argument('-o', '--output', help='ファイル出力先のディレクトリパス', action='store')
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    srcFile = args.FILE_PATH
    dstDir = args.output
    exclude_flag = args.exclude

    try:
        package.xml2geojson.SaveGeoJson(srcFile, dstDir, exclude_flag)
    except Exception:
        print('Error Source File:', srcFile)
        traceback.print_exc()


if __name__ == '__main__':
    main()
