#!/usr/bin/env python
import os
import sys
from subprocess import check_call, CalledProcessError
from os.path import isfile, splitext
import glob
from datetime import date
import logging

logging.basicConfig()
# create logger
logger = logging.getLogger('pdf-to-static')
logger.setLevel(logging.DEBUG)

# create file handler and set level to INFO
file_handler = logging.FileHandler('pdf-to-static.log')
file_handler.setLevel(logging.INFO)

# create formatter
format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(format)
logger.addHandler(file_handler)


def convert(filename=None,imageformat=None):
    try:
        if isfile(filename):
            if '/' in splitext(filename)[0]:
                pdfname = splitext(filename)[0].split('/')[-1]
            else:
                pdfname = splitext(filename)[0]

            if imageformat:
                jpg = pdfname + '_' + imageformat
            else:
                jpg = pdfname + ".jpg"

            img_path = pdfname + '_images'
            convert_to_images(pdfname, jpg, img_path)
            convert_to_markdown(pdfname, img_path, jpg)
            convert_to_html(pdfname, img_path)

    except (OSError, CalledProcessError, TypeError, UnboundLocalError, NameError) as e:
        logger.error("-----{0}-----".format(e))


def convert_to_images(pdfname, jpg, img_path):
    """

This function takes the pdf name and resultant image format
and converts all the pages in pdf in to a separate jpg image
files

"""
    logger.info("Converting {0} file to images ..............".format(
        pdfname + '.pdf'))
    if not os.path.isdir(img_path):
        os.mkdir(img_path)
    check_call(["convert", "-density", "150", "-trim",
                        filename, "-quality", "100", "-scene", "1", os.path.join(os.path.abspath(img_path), jpg)])


def convert_to_markdown(pdfname, img_path, jpg):
    """

This function takes the pdf name and images path
and converts all the images in to markdown files

"""

    md_path = pdfname + '_md'
    if not os.path.isdir(md_path):
        os.mkdir(md_path)
    logger.info("Converting image files to markdown files .........")
    for image in glob.glob(img_path + '/' + jpg.split('.')[0] + '-[0-9]*.jpg'):
        logger.info(
            " Converted image '{0}' to markdown file.........".format(image))
        markdownfile = open(md_path + '/' + image.split(
            '.')[0].split('/')[-1] + '.md', 'wb')
        markdownfile.write('Date:{0} \nTitle: {1} \n'.format(
            str(date.today()), image.split('/')[-1]))
        markdownfile.write('![Alt {0}]({1})'.format(
            image, os.path.abspath(image)))
        markdownfile.close()


def convert_to_html(pdfname, img_path):
    """

This function converts all the markdown files in to
html files

"""

    md_path = pdfname + '_md'
    logger.info("Converting markdown files to html files .........")
    if os.path.isdir(md_path):
        os.system("pelican {0}".format(md_path))
    logger.info("\n ---- Conversion Completed ---- \n")


if __name__ == '__main__':
    try:
        if len(sys.argv) < 3:
            if isfile(sys.argv[1]):
                filename = sys.argv[1]
                convert(filename)
            elif os.path.isdir(sys.argv[1]):
                pdfs = os.listdir(sys.argv[1])
                for pdf in pdfs:
                    filename = os.path.join(sys.argv[1], pdf)
                    convert(filename)
        else:
            imageformat = sys.argv[2]
            if isfile(sys.argv[1]):
                filename = sys.argv[1]
                convert(filename, imageformat)
            elif os.path.isdir(sys.argv[1]):
                pdfs = os.listdir(sys.argv[1])
                for pdf in pdfs:
                    filename = os.path.join(sys.argv[1], pdf)
                    convert(filename, imageformat)
    except (IndexError) as e:
        print "\n----please provide input file----\n"
