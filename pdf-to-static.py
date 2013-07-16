#!/usr/bin/env python
import os
import sys
from subprocess import check_call, CalledProcessError
from os.path import isfile, splitext
import glob
from datetime import date


def convert(filename=None,imageformat=None):
    try:
        if isfile(filename):
            if '/' in splitext(filename)[0]:
                pdfname = splitext(filename)[0].split('/')[-1]
            else:
                pdfname = splitext(filename)[0]

            if imageformat:
                jpg = imageformat
            else:
                jpg = pdfname + ".jpg"

            img_path = pdfname + '_images'
            convert_to_images(pdfname, jpg, img_path)
            convert_to_markdown(pdfname, img_path)
            convert_to_html(pdfname, img_path)

    except (OSError, CalledProcessError, TypeError, UnboundLocalError) as e:
        print "-----{0}-----".format(e)


def convert_to_images(pdfname, jpg, img_path):
    """

    This function takes the pdf name and resultant image format
    and converts all the pages in pdf in to a separate jpg image
    files

    """
    print "\nConverting pdf file to images .............."
    if not os.path.isdir(img_path):
        os.mkdir(img_path)
    check_call(["convert", "-density", "150", "-trim",
                        filename, "-quality", "100", "-scene", "1", os.path.join(os.path.abspath(img_path), jpg)])


def convert_to_markdown(pdfname, img_path):
    """

    This function takes the pdf name and images path
    and converts all the images in to markdown files

    """

    md_path = pdfname + '_md'
    if not os.path.isdir(md_path):
        os.mkdir(md_path)
    print "\nConverting image files to markdown files ........."
    for image in glob.iglob(img_path + '/' + pdfname + '-[0-9]*.jpg'):
        print "    Converted image '{0}' to markdown file.........".format(image)
        markdownfile = open(md_path + '/' + image.split(
            '.')[0].split('/')[-1] + '.md', 'wb')
        markdownfile.write('Date:{0} \nTitle: {1} \n'.format(
            str(date.today()), image))
        markdownfile.write('![Alt {0}]({1})'.format(
            image, os.path.abspath(image)))
        markdownfile.close()


def convert_to_html(pdfname, img_path):
    """

    This function converts all the markdown files in to
    html files

    """

    md_path = pdfname + '_md'
    print "\nConverting markdown files to html files .........\n"
    if os.path.isdir(md_path):
        os.system("pelican {0}".format(md_path))
    print "\n ---- Conversion Completed ---- \n"

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        if len(sys.argv) < 3:
            convert(filename)
        else:
            imageformat = sys.argv[2]
            convert(filename, imageformat)
    except (IndexError) as e:
        print "----please provide input file----"
