import datetime
import pandas as pd
import traceback
from sqlalchemy import create_engine
import mysql.connector
import sqlite3
#import sqlalchemy

try:
    from core_mk.credentials import DB
except Exception:
    from credentials import DB

LOG_FNAME = "price_log.txt"
engine_str = f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["database"]}'

last_date = None

def write2database(df, table, engine=None):
    global last_date
    if not last_date:
        last_date = datetime.datetime.now()

#    print(1111, engine)
    if engine == None:
        engine = create_engine(engine_str)
#        print(777, engine)
    else:
        engine = create_engine('sqlite:///' + engine, echo=False)

#    print(2222, engine)
    result = 1

    try:
        df_dates = pd.DataFrame()
        df_dates['date'] = [last_date]*df.shape[0]
        df = df_dates.join(df)

#        dtype = {
#         'article': sqlalchemy.types.NVARCHAR(length=255),
#         'title': sqlalchemy.types.NVARCHAR(length=255),
#         'price': sqlalchemy.types.Float(),
#         'store': sqlalchemy.types.NVARCHAR(length=50),
#         'seller': sqlalchemy.types.NVARCHAR(length=255),
#         'url': sqlalchemy.types.NVARCHAR(length=255),
#         }

        r = df.to_sql(table, con=engine, if_exists='append', index=False)
#        df.to_sql(table, con=engine, if_exists='append', index=False)
#        print(r, engine_str, engine)
#        print(r, df)
    except Exception as err:
        print(err)
        log_error(f'Problem with download {table} to sql {err}')
        result = 0
    return result

def load_table(table, engine=None):
    if engine == None:
        engine = create_engine(engine_str)
    else:
        engine = create_engine('sqlite:///' + engine, echo=False)

    try:
        df = pd.read_sql_table(table, con=engine)
        result = df.to_dict('records')
    except Exception as err:
        print(err)
        result = []
    return result

def empty_table(table, engine=None):
    if engine == None:
        mydb = mysql.connector.connect(host=DB['host'], user=DB['user'], password=DB['password'], database=DB['database'], autocommit = True)
        cursor = mydb.cursor(buffered=True)
    else:
        mydb = sqlite3.connect(engine)
        cursor = mydb.cursor()

    sql = f'DELETE FROM {table}'
    try:
        cursor.execute(sql)
        mydb.commit()
        rez = str(cursor.rowcount)
    except Exception as err:
        rez = str(err)

    if engine == None:
        cursor.reset()
    cursor.close()
    mydb.close()
    return rez

def log_error(s):
     _log(s, is_error=True)

def log_info(s):
     _log(s, is_error=False)

def _log(s, is_error):
    with open(LOG_FNAME, 'a', encoding='utf-8') as f:
        f.write('\n' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
        f.write(s + '\n')
        if is_error:
            traceback.print_exc(file=f)
