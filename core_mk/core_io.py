import datetime
import pandas as pd
import traceback
from sqlalchemy import create_engine
import mysql.connector
import sqlite3

try:
    from core_mk.credentials import DB
except Exception:
    from credentials import DB

dbms = DB.get('dbms', 'mysql')
if dbms == 'mysql':
    engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["database"]}')
else:
    #sqlite only
    engine = create_engine(f'sqlite:///{DB["file"]}', echo=False)

LOG_FNAME = "price_log.txt"
last_date = None

def write2database(df, table):
    global last_date
    if not last_date:
        last_date = datetime.datetime.now()

    try:
        df_dates = pd.DataFrame()
        df_dates['date'] = [last_date]*df.shape[0]
        df = df_dates.join(df)
        r = df.to_sql(table, con=engine, if_exists='append', index=False)
    except Exception as err:
        print(err)
        log_error(f'Problem with download {table} to sql {err}')
        return 0
    return 1

def load_table(table):
    try:
        df = pd.read_sql_table(table, con=engine)
        result = df.to_dict('records')
    except Exception as err:
        print(err)
        result = []
    return result

def empty_table(table):
    if dbms == 'mysql':
        mydb = mysql.connector.connect(host=DB['host'], user=DB['user'], password=DB['password'], database=DB['database'], autocommit = True)
        cursor = mydb.cursor(buffered=True)
    else:
        #sqlite only
        mydb = sqlite3.connect(DB["file"])
        cursor = mydb.cursor()

    sql = f'DELETE FROM {table}'
    try:
        cursor.execute(sql)
        mydb.commit()
        rez = str(cursor.rowcount)
    except Exception as err:
        rez = str(err)

    if dbms == 'mysql':
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
