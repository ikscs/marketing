#encoding: utf-8
from pathlib import Path
import os
import sys 

#Add cp/Parser to module path
parent_folder = Path().resolve().parent
parent_folder = Path(parent_folder).resolve().parent
cp_folder = Path(parent_folder, 'cp', 'Parser')

sys.path.append(str(cp_folder))
sys.path.append('..')
from core.loader import Loader as Loader_parent
from core.logger import Logger

from core_mk.core_io import load_table

class Loader(Loader_parent):
    def load_online(self):
#        path_to_db = 'test.db'
        path_to_db = None
        data = load_table('mk_price', path_to_db)
        if not data:
            self.log.error(f'Problem with download from database')
            return False
        return {'data' : data}

if __name__ == '__main__':
    current_path = os.getcwd()
    subject_fname = 'marketing'
    log = Logger(subject_fname, current_path)
    provider = Loader(subject_fname, log, current_path, is_offline = True)
#    provider = Loader(subject_fname, log, current_path, is_offline = False)
    d = provider.load()
    print(d)
#    provider.save(d)
