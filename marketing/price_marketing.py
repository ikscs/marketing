#encoding: utf-8
import os
import sys 
from pathlib import Path

SUBJECT_ID = 'DEADBEEF'
SUBJECT_ROLE = 4
SUBJECT_FNAME = 'marketing'

current_path = os.getcwd()
try:
    os.chdir(SUBJECT_FNAME)
except Exception:
    pass
MODULE_FOLDER = os.getcwd()

#Add cp/Parser to module path
parent_folder = Path().resolve().parent
parent_folder = Path(parent_folder).resolve().parent
cp_folder = Path(parent_folder, 'cp', 'Parser')

sys.path.append(str(cp_folder))
sys.path.append('..')
from core.processor import Provider
from core.informer import Informer

sys.path.append(MODULE_FOLDER)
exec(f'from loader_{SUBJECT_FNAME} import Loader')
exec(f'from manager_{SUBJECT_FNAME} import dict2data')
exec(f'from adapter_{SUBJECT_FNAME} import adapt_product, adapt_group, beautify')

os.chdir(current_path)

if __name__ == '__main__':
    current_module = sys.modules[__name__]
    provider = Provider(current_module, Informer(), is_offline=True, engine='test.db')
    provider.execute()
