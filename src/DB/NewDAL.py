import threading
from src.utils import DBconfig

__author__ = 'Sapocaly'

config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))

DB_ENGINE = None


class Engine():
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        if not self.conn.is_connected():
            self.conn.connect()
        return self.conn


def create_engine(**args):
    import mysql.connector
    global DB_ENGINE
    if DB_ENGINE is not None:
        raise Exception('Engine is already initialized.')
    DB_ENGINE = Engine(mysql.connector.connect(**args))
    ##log


class DbConnector(threading.local):
    def __init__(self):
        self.conn = None

    def init(self):
        global DB_ENGINE
        self.conn = DB_ENGINE.connect()

    def is_init(self):
        return not self.conn is None

    def close(self):
        self.conn.close()
        self.conn = None
        ##log

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def cursor(self):
        return self.conn.cursor()


DB_CONNECTOR = DbConnector()


class Connection():
    def __enter__(self):
        global DB_CONNECTOR
        if DB_CONNECTOR.is_init():
            self.need_clean = False
        else:
            DB_CONNECTOR.init()
            self.need_clean = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.need_clean:
            global DB_CONNECTOR
            DB_CONNECTOR.close()


def connection():
    return Connection()


if __name__ == '__main__':
    create_engine(**config_args)
    with connection():
        print 1
