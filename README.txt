tagger_trainer - a training data collector for an automated text categorizer/tagger
created by Yasser Ebrahim, 07NOV12
----

This script takes an input file containing a taxonomy of categories of maximum depth 2 (categories and subcategories), then it tries to find corresponding wikipedia pages for each cateogry/subcategory by traversing English wikipedia urls whose suffix is the category name. It uses Goose, a python library that extracts article body text from a given url. You can read more about Goose here: https://github.com/jiminoc/goose/wiki

The script creates a file for each category/subcategory insdie the directory "crawled." In the file is pure text extracted from the url, which can later be used to train a tagger. A simple urls_file is included called topics.txt

Usage:
    python tagger_trainer.py urls_file.txt

***Plese note that this requires Goose to be installed before running.
