#!/usr/bin/env python
# encoding: utf-8

"""
File: tagger_trainer.py
Author: Yasser Ebrahim
Date: NOV 2012

This script takes an input file containing a taxonomy of categories of maximum depth 2 (categories and subcategories), then it tries to find corresponding wikipedia pages for each cateogry/subcategory by traversing English wikipedia urls whose suffix is the category name. It uses Goose, a python library that extracts article body text from a given url. You can read more about Goose here: https://github.com/jiminoc/goose/wiki

The script creates a file for each category/subcategory insdie the directory "crawled." In the file is pure text extracted from the url, which can later be used to train a tagger. A simple urls_file is included called topics.txt, obtained by reformatting the 'categories.txt' file on http://rdf.dmoz.org/rdf/ to get only the first two levels.

Usage:
        python tagger_trainer.py urls_file.txt

***Plese note that this requires Goose to be installed before running.
"""

import os, sys, codecs, httplib, urlparse, unicodedata
from goose.Goose import Goose
from optparse import OptionParser

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None

def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

def remove_diacritic(input):
    input = unicode(input, 'ISO-8859-1')
    return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')

# __main__ execution

parser = OptionParser(usage='usage: %prog [options] urls_file')
options, args = parser.parse_args()

if len(args) < 1:
    print(parser.print_help())
    quit()

f = open(sys.argv[1])
files = f.read().splitlines()

malwriter = codecs.open('not_found.txt', encoding='utf-8', mode='w+')

g = Goose()
for f in files:
    # only take the name of the subcategory
    p = f.split('/')[-1]
    # if the category is something like "Religion_and_Spirituality", split
    p = p.split('_and_')[0]
    # wikipedia uses single forms in urls
    if p[-1] == 's': p = p[:-1]
    # avoid problems in file names
    f = f.replace('/','#')
    # avoid problems with accented characters
    f = remove_diacritic(f)
    # if filed already crawled, skip
    if os.path.exists('crawled/' + f + '.txt'):
        continue

    url = 'http://en.wikipedia.org/wiki/' + p
    if not check_url(url):
        url = remove_diacritic(url)
        malwriter.write(p + '\n')
        continue

    print('crawing: ' + url)
    article = g.extractContent(url=url)
    writer = codecs.open('crawled/' + f + '.txt',encoding='utf-8',mode='w+')
    writer.write(article.title + '\n')
    writer.write(article.cleanedArticleText)
