import sqlite3

class DBError(Exception):
    def __init__(self, code, msg):
        Exception.__init__(self)
        self.code = code
        self.msg = msg

class Connection(object):

    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = dict_factory
        self._conn.text_factory = str
        self._cursor = self._conn.cursor()

    @property
    def cursor(self):
        return self._cursor

    @property
    def connection(self):
        return self._conn

    def __getattr__(self, attr):
        return getattr(self._conn, attr)

    def select(self, script, params=None):
        if None == params:
            self._cursor.execute(script)
        else:
            self._cursor.execute(script, params)
        return self._cursor.fetchall()

    def update(self, script, params=None):
        if None == params:
            self._cursor.execute(script)
        else:
            self._cursor.execute(script, params)
        return self._cursor.rowcount

    def commit(self):
        try:
            self._conn.commit()
        except:
            self._conn.rollback()
            raise

    create = update
    insert = update
    delete = update
    execute = update

def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))

if __name__ == '__main__':
    conn = Connection('db')
