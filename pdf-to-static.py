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
                imagename = splitext(filename)[0].split('/')[-1]
            else:
                imagename = splitext(filename)[0]

            if imageformat:
                jpg = imageformat
            else:
                jpg = imagename + ".jpg"
            img_path = imagename + '_' + 'images'
            if not os.path.isdir(img_path):
                os.mkdir(img_path)
            check_call(["convert", "-density", "150", "-trim",
                        filename, "-quality", "100", "-scene", "1", os.path.join(os.path.abspath(img_path), jpg)])
            md_path = imagename + '_' + 'md'
            for image in glob.iglob(img_path + '/' + imagename + '-[0-9].jpg'):
                if not os.path.isdir(md_path):
                    os.mkdir(md_path)
                markdownfile = open(md_path + '/' + image.split(
                    '.')[0].split('/')[-1] + '.md', 'wb')
                markdownfile.write('Date:{0} \nTitle: {1} \n'.format(
                    str(date.today()), image.split('/')[-1]))
                markdownfile.write('![Alt {0}]({1})'.format(
                    image, os.path.abspath(image)))
                markdownfile.close()
            if os.path.isdir(md_path):
                os.system("pelican {0}".format(md_path))

    except (OSError, CalledProcessError, TypeError, UnboundLocalError) as e:
        print "-----{0}-----".format(e)


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
