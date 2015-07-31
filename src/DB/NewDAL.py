import functools
import threading
from src.utils import DBconfig
import src.utils.LogConstant as LogConstant

__author__ = 'Sapocaly'

config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                       [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))

logger = LogConstant.DAL_DIGEST_LOGGER
logger_err = LogConstant.DAL_DIGEST_LOGGER_ERROR

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


def close_engine():
    global DB_ENGINE
    if not DB_ENGINE is None:
        DB_ENGINE.conn.disconnect()
        DB_ENGINE = None


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


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)

    return _wrapper


def sql_format(val):
    if isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif val is None:
        return 'null'
    else:
        return "'{0}'".format(str(val))


ECHO = False


@with_connection
def execute(sql):
    cursor = DB_CONNECTOR.cursor()
    try:
        if ECHO:
            print sql
        cursor.execute(sql)
        DB_CONNECTOR.commit()
        logger.info(sql)
    except Exception as e:
        print e
        logger_err.error(sql)
        logger_err.exception(str(e))
    cursor.close()


@with_connection
def select(sql):
    cursor = DB_CONNECTOR.cursor()
    try:
        if ECHO:
            print sql
        cursor.execute(sql)
        results = [i for i in cursor]
        logger.info(sql)
        if ECHO:
            print results
        return results
    except Exception as e:
        print e
        logger_err.error(sql)
        logger_err.exception(str(e))
    cursor.close()


def insert_into(table_name, **args):
    try:
        keys = args.keys()
        values = [sql_format(args[key]) for key in keys]
        sql = "insert into {0} ({1})values({2})".format(
            table_name, ",".join(keys), ",".join(values))
        execute(sql)
    except Exception as e:
        print e
        logger_err.exception(str(e))


def select_from(table_name, **args):
    try:
        if len(args) > 0:
            sql = "select * from {0} where ".format(table_name)
            for key in args:
                formatted_key = sql_format(args[key])
                if formatted_key == 'null':
                    sql += "{0} is {1} and ".format(key, 'null')
                else:
                    sql += "{0} = {1} and ".format(key, formatted_key)
            sql = sql[:-5]
        else:
            sql = "select * from " + table_name

        return select(sql)
    except Exception as e:
        print e
        logger_err.exception(str(e))


def delete_from(table_name, **args):
    try:
        if len(args) > 0:
            sql = "delete from {0} where ".format(table_name)
            for key in args:
                formatted_key = sql_format(args[key])
                if formatted_key == 'null':
                    sql += "{0} is {1} and ".format(key, 'null')
                else:
                    sql += "{0} = {1} and ".format(key, formatted_key)
            sql = sql[:-5]
        else:
            sql = "select * from " + table_name
        execute(sql)
    except Exception as e:
        print e
        logger_err.exception(str(e))


def update(table_name, **args):
    try:
        keys = args.keys()
        query_keys = filter(lambda x: x[0] == '_', keys)
        update_keys = filter(lambda x: x[0] != '_', keys)
        query_keys = list(map(lambda x: x[1:], query_keys))
        for key in keys:
            args[key] = sql_format(args[key])
        where_clause = ''
        if len(query_keys) != 0:
            where_clause = 'where '
            for key in query_keys:
                formatted_key = args['_' + key]
                if formatted_key == 'null':
                    where_clause += "{0} is {1} and ".format(key, 'null')
                else:
                    where_clause += "{0} = {1} and ".format(key, formatted_key)
            where_clause = where_clause[:-5]
        update_clause = ''
        for key in update_keys:
            update_clause += "{0} = {1}, ".format(key, args[key])
        update_clause = update_clause[:-2]
        sql = "update {0} set {1} {2}".format(
            table_name, update_clause, where_clause)
        execute(sql)
    except Exception as e:
        print e
        logger_err.exception(str(e))





if __name__ == '__main__':
    ECHO = True
    create_engine(**config_args)
    print DB_ENGINE.conn.is_connected()
    try:
        with connection():
            print DB_ENGINE.conn.is_connected()
            print DB_CONNECTOR.conn
            print 1
            raise Exception()
    except Exception:
        print 'good'

    print DB_CONNECTOR.conn
    print DB_ENGINE.conn.is_connected()
    close_engine()
    print DB_ENGINE
    #############
    create_engine(**config_args)
    select_from('stock',ticker='aapl')
    insert_into('stock', ticker='sheng')
    insert_into('stock', aticker='sheng')
    select_from('stock', name=None)
    update('stock', _ticker='sheng', _name=None, name='shengye')
    delete_from('stock', ticker="sheng", pv_close=None)
    close_engine()

