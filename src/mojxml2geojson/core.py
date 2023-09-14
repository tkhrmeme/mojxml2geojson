# coding: utf-8

import argparse
import traceback
import package.xml2geojson
import pathlib
import zipfile
import tempfile

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
        path_src = pathlib.Path(srcFile)

        if not path_src.exists():
            # 変換するXMLファイルが存在しない
            print("Source file not found:", srcFile)
        else:
            if path_src.suffix == '.zip':
                # 一時ディレクトリを作成
                with tempfile.TemporaryDirectory() as tmp_dir_name:
                    path_tmp_dir = pathlib.Path(tmp_dir_name)

                    # zipファイルを展開する
                    with zipfile.ZipFile(srcFile) as zf:
                        # ファイル名のリストを取り出す
                        zf_names = zf.namelist()
                         # 一時ディレクトリ内に展開
                        zf.extractall(path_tmp_dir)

                    for src_name in zf_names:
                        srcFile = path_tmp_dir / src_name
                        package.xml2geojson.SaveGeoJson(srcFile, dstDir, exclude_flag)

            elif path_src.suffix != '.xml':
                # 拡張子が.xmlではない
                print('File extension is not .xml:', srcFile)
                raise()
            else:
                package.xml2geojson.SaveGeoJson(srcFile, dstDir, exclude_flag)

    except Exception:
        print('Error Source File:', srcFile)
        traceback.print_exc()


if __name__ == '__main__':
    main()
