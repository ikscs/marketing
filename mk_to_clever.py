import os
import sys
from pathlib import Path

parent_folder = Path().resolve().parent
sys.path.append(str(Path(parent_folder, 'cp', 'Parser')))

from core.processor import Provider
from core.logger import Logger
from core.informer import Informer

import marketing.price_marketing

if __name__ == '__main__':

#    is_offline = True
    is_offline = False
#    engine = Path('test.db').resolve()
    engine = None

    log = Logger('mk_to_clever', os.getcwd(), is_overwrite=False)
    log.info('===================\nmarketing started')

    informer = Informer()
    provider = Provider(marketing.price_marketing, informer, is_offline=is_offline, engine=engine)

    provider.execute_block1()
    provider.execute_block2()
    provider.execute_block3()

    log.info('marketing ended\n===================')
