import sqlite3 as sq


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sq.connect(' photo.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    cur = conn.cursor()
    print('База данных успешно подключена')
    if force:
        cur.execute('DROP TABLE IF EXISTS photo.db')

    cur.execute('''
     CREATE TABLE IF NOT EXISTS photo(
         id INTEGER PRIMARY KEY,
         file_id TEXT,
         pHash TEXT,
         dHash TEXT)
        '''
                )
    # сохраннение изменений
    conn.commit()


@ensure_connection
async def sql_add_command(state, conn, data):
    async with state.proxy() as data:
        cur = conn.cursor()
        cur.execute('INSERT INTO photo VALUES (?, ?, ?)', tuple(data.values()))
        conn.commit()


@ensure_connection
async def duplicate_check(state, conn):
    cur = conn.cursor()
    photos_p_Hash = cur.execute('SELECT pHash FROM photo.db').fetchall()
    return photos_p_Hash
