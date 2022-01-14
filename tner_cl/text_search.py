""" Indexing document for contextualized prediction.
tner-text-search -p ./tner_output/index/2021_large -f cache/twitter_ner/raw/large.eval.csv -t tweet -d created_at -i id
tner-text-search -p ./tner_output/index/2021_large --interactive-mode
"""
import argparse
import logging
from pprint import pprint

from tner import WhooshSearcher

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def arguments(parser):
    parser.add_argument('-p', '--index-path', help='path to index directory', required=True, type=str)
    parser.add_argument('-f', '--csv-file', help='csv file to index', default=None, type=str)
    parser.add_argument('-t', '--column-text', help='column of text to index', default=None, type=str)
    parser.add_argument('-d', '--column-datetime', help='column of text to index', default=None, type=str)
    parser.add_argument('-i', '--column-id', help='column of text to index', default=None, type=str)
    parser.add_argument('--datetime-format', help='datetime format', default='%Y-%m-%d', type=str)
    parser.add_argument('--interactive-mode', help='', action='store_true')
    return parser


def main():
    parser = argparse.ArgumentParser(description='Index document for contextualized prediction.')
    parser = arguments(parser)
    opt = parser.parse_args()
    searcher = WhooshSearcher(index_path=opt.index_path)
    if opt.csv_file is not None:
        assert opt.column_text is not None, 'please specify target column in the csv by `--column-text`'
        searcher.whoosh_indexing(
            csv_file=opt.csv_file,
            column_text=opt.column_text,
            column_id=opt.column_id,
            column_datetime=opt.column_datetime,
            datetime_format=opt.datetime_format
        )
    if opt.interactive_mode:
        while True:
            _inp = input('query >>>')
            if _inp == 'q':
                break
            elif _inp == '':
                continue
            else:
                out = searcher.search(_inp)
                print('# {} documents #'.format(len(out)))
                print('#' * 100)
                for n, i in enumerate(out):
                    print(' *** {} *** \n{}'.format(n, i))
                    print('#' * 100)
