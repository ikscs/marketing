from core_mk.core_io import load_table, empty_table
from core_mk.driver import Driver

from price_rozetka import rozetka_art
from price_prom import prom_art
from price_hotline import hotline_art
from price_gmc import gmc_art

from schema_parser import schema_parser

if __name__ == '__main__':

    empty_table('mk_price')
    mk_articles = load_table('mk_article')
    mk_urls = load_table('mk_url')

    driver = Driver()
    for article in (e['article'] for e in mk_articles):
        print(article)
        print('prom\t', prom_art([article], driver))
        print('hotline\t', hotline_art([article], driver))
        print('gmc\t', gmc_art([article], driver))
        print('rozetka\t', rozetka_art([article], driver))

    for url, article, store in ((e['url'], e['article'], e['store']) for e in mk_urls):
        print(url, article, store)
        if not schema_parser(url, article, store, driver):
            print(f'Error parse: {url}')

    driver.close()
