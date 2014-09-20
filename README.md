## pdf-to-static

#### pdf-to-static is a tool to convert a pdf or a set of pdfs to a static html website.

### Usage

    pdf-to-static something.pdf
    pdf-to-static somedirectory/has-a.pdf


### Motivations:

There are a lot of pdfs which could be usable as a html website. This is an automated tool to convert them to static website.

The first place we can use this is at Pratham books.

Pratham books is a publisher which makes it books available under a CC license. 
Their english ebooks are at:

https://www.dropbox.com/sh/6u0ylkp136sns44/3KQ3z6Ec3e

Our main goal is to convert this set of pdfs as a single website. However this tool should be able to take an arbitrary pdf or directory as an input.

### Tools:

* Imagemagic is used to convert the [pdf to a set of images](http://stackoverflow.com/questions/6605006/convert-pdf-to-image-with-high-resolution). 
* Pelican is used to stich together the images as a static website. 
