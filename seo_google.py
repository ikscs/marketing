from googleapiclient.discovery import build
import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
#from connection import connection_to_db
from time import sleep
import traceback
from core_mk.credentials import GoogleAPI, DB

my_api_key = GoogleAPI['key']
my_cse_id = GoogleAPI['id']
# con = MySQLdb.connect(host=DB['host'], user=DB['user'], password=DB['password'], db=DB['database'])
engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["database"]}')

data = {'keywords': [], 'date': [], 'rating': [], 'domain': [], 'url': [], 'title': [], 'description': []}
df_google = pd.DataFrame(data)
mk = pd.read_sql('SELECT * FROM mk_google_kw', engine)

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    sleep(0.33)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if "items" in res.keys():
        return res['items']
    else:
        return None
for i, row in mk.iterrows():
    query = row['keyword']
    for page_num in range(row['depth']):
        num_position = 0
        start_position = page_num * 10 +1
        try:
            results = google_search(query, my_api_key, my_cse_id, num=10, gl='ua', start=start_position)
            if results != None:
                for result in results:
                    rating = start_position + num_position
                    date = datetime.datetime.now()
                    title = result['title']
                    domain = result['displayLink']
                    description = result['snippet']
                    url = result['link']
                    new_row = {'keywords': query,'date': date, 'rating': rating, 'domain': domain, 'url': url, 'title': title, 'description': description}
                    df_google = pd.concat([df_google, pd.DataFrame((new_row,))], ignore_index=True)
                    num_position += 1
            else:
                break
        except Exception as e:
            if 'HttpError 429' in traceback.format_exc():
                print('Превышен лимит запросов')

    df_google.to_sql("mk_google_rp", con=engine, if_exists='append', index=False,
                  dtype={'keywords': sqlalchemy.types.NVARCHAR(length=255), 'date': sqlalchemy.DateTime(), 'rating': sqlalchemy.types.INTEGER,
                     'domain': sqlalchemy.types.NVARCHAR(length=50), 'url': sqlalchemy.types.NVARCHAR(length=255),
                     'title': sqlalchemy.types.NVARCHAR(length=255), 'description': sqlalchemy.types.NVARCHAR(length=500)})
    data = {'keywords': [], 'date': [], 'rating': [], 'domain': [], 'url': [], 'title': [], 'description': []}
    df_google = pd.DataFrame(data)
