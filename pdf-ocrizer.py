from PIL import Image
import sys
from pdf2image import convert_from_path
import re
import subprocess
import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('pdf_path', metavar='DIR', help='path to pdf')

parser.add_argument('pdf_file', metavar='DIR', help='path to pdf directory')

def convert_pdf2text(file_path):

    #配置先ディレクトリ
    pdf_path = Path("./pdf_file/"+file_path+".pdf")
    txt_path = Path("./txt_file/"+file_path + ".txt")
    out_path = Path("./pdf_file/output/"+file_path+".pdf") 

    pages = convert_from_path(str(pdf_path),300)

    txt=''
    print('全部で{}ページ'.format(len(pages)))

    #マルチページのTIFFとして保存する
    image_dir = Path("./image_file")
    tiff_name = pdf_path.stem + ".tif"
    image_path = image_dir / tiff_name
    to_pdf = pdf_path.stem + "_TO"
    topdf_path = image_dir / to_pdf

    #既存ファイル削除
    if os.path.exists(image_path):
        os.remove(image_path)
    if os.path.exists(str(topdf_path)+'.pdf'):
        os.remove(str(topdf_path)+'.pdf')

    pages[0].save(str(image_path), "TIFF", compression="tiff_deflate", save_all=True, append_images=pages[1:])

    
    print('テキストオンリーpdfの生成')

    #テキストオンリーpdfの生成
    cmd = 'tesseract -c page_separator="[PAGE SEPRATOR]" -c textonly_pdf=1 "' + str(image_path) + '" "' +  str(topdf_path) +'" -l jpn pdf'
    print(cmd)
    returncode = subprocess.Popen(cmd,shell=True )
    returncode.wait()


    #オリジナルのpdfにtextonlyのpdfをオーバーレイして最小サイズのpdfを生成してみる。qpdfの基本コマンドは以下
    #to.pdf＝テキストオンリーpdf　org.pdf＝オリジナルpdf　out.pdf=オーバレイ済pdf
    #qpdf --overlay to.pdf -- org.pdf out.pdf
    if os.path.exists(out_path):
        print('remove　' + out_path)
        os.remove(out_path)
    cmd = 'qpdf --overlay "' + str(topdf_path) + '.pdf" -- "' + str(pdf_path) +'" "' + str(out_path) + '" '
    print(cmd)
    returncode = subprocess.Popen(cmd,shell=True )
    returncode.wait()

def main():
    args = parser.parse_args()
    convert_pdf2text(args.pdf_path)

if __name__ == '__main__':
    main()
