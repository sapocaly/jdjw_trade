import functools
import threading
import time
import uuid

from src.utils import DBconfig
import src.utils.LogConstant as LogConstant

__author__ = 'Sapocaly'

_logger = LogConstant.DAL_DIGEST_LOGGER
_logger_err = LogConstant.DAL_DIGEST_LOGGER_ERROR

DB_ENGINE = None

ECHO = False


class Engine:
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


def close_engine():
    global DB_ENGINE
    if DB_ENGINE is not None:
        DB_ENGINE.conn.disconnect()
        DB_ENGINE = None


class DbConnector(threading.local):
    def __init__(self):
        self.conn = None
        self.transaction_level = 0
        self.need_rollback = False

    def init(self):
        global DB_ENGINE
        conn = DB_ENGINE.connect()
        _logger.info('open connection <{0}>...'.format(hex(id(conn))))
        self.conn = conn

    def is_init(self):
        return not self.conn is None

    def close(self):
        conn = self.conn
        conn.close()
        _logger.info('close connection <{0}>...'.format(hex(id(conn))))
        self.conn = None

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def cursor(self):
        return self.conn.cursor()


_DB_CONNECTOR = DbConnector()


class Connection():
    def __enter__(self):
        global _DB_CONNECTOR
        if _DB_CONNECTOR.is_init():
            self.need_clean = False
        else:
            _DB_CONNECTOR.init()
            self.need_clean = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.need_clean:
            global _DB_CONNECTOR
            _DB_CONNECTOR.close()


def connection():
    return Connection()


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)

    return _wrapper


class Transaction:
    def __enter__(self):
        self.uuid = str(uuid.uuid4())
        global _DB_CONNECTOR
        if _DB_CONNECTOR.is_init():
            self.need_clean = False
        else:
            _DB_CONNECTOR.init()
            self.need_clean = True
        if _DB_CONNECTOR.transaction_level == 0:
            _DB_CONNECTOR.need_rollback = False
        log_string = 'Transaction <{0}> START (Nested = {1})'.format(self.uuid, _DB_CONNECTOR.transaction_level != 0)
        _logger.info(log_string)
        _DB_CONNECTOR.transaction_level += 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _DB_CONNECTOR
        _DB_CONNECTOR.transaction_level -= 1
        log_string = 'Transaction <{0}> FINISH (Nested = {1})'.format(self.uuid, _DB_CONNECTOR.transaction_level != 0)
        _logger.info(log_string)
        if _DB_CONNECTOR.transaction_level == 0:
            try:
                if _DB_CONNECTOR.need_rollback:
                    self.rollback()
                else:
                    self.commit()
                _DB_CONNECTOR.need_rollback = False
            finally:
                if self.need_clean:
                    _DB_CONNECTOR.close()

    def commit(self):
        global _DB_CONNECTOR
        try:
            _DB_CONNECTOR.commit()
            log_string = 'Transaction <{0}> COMMIT_SUCCESS (Nested = False)'.format(self.uuid)
            _logger.info(log_string)
        except:
            log_string = 'Transaction <{0}> COMMIT_FAIL (Nested = False)'.format(self.uuid)
            _logger.info(log_string)
            self.rollback()

    def rollback(self):
        global _DB_CONNECTOR
        _DB_CONNECTOR.rollback()
        log_string = 'Transaction <{0}> ROLLBACK_SUCCESS (Nested = False)'.format(self.uuid)
        _logger.info(log_string)


def transaction():
    return Transaction()


def with_transaction(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with transaction():
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


def sql_with_logging(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        start = time.time()
        sql = args[0]
        if ECHO:
            print sql
        result = 'True'
        try:
            res = func(*args, **kw)
            if res and ECHO:
                print res
            return result
        except Exception as e:
            result = 'False'
            _logger_err.exception(sql)
        finally:
            delta = int((time.time() - start) * 1000)
            log_string = '({0}),{1},{2}ms'.format(sql, result, delta)
            _logger.info(log_string)

    return _wrapper


def exception_handler(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            log_string = '{0},{1},{2}'.format(func.__name__, args, kw)
            _logger_err.exception(log_string)

    return _wrapper


@sql_with_logging
@with_connection
def execute(sql):
    cursor = None
    success = False
    global _DB_CONNECTOR
    try:
        cursor = _DB_CONNECTOR.cursor()
        cursor.execute(sql)
        success = True
        if _DB_CONNECTOR.transaction_level == 0:
            _DB_CONNECTOR.commit()
    finally:
        if not success and _DB_CONNECTOR.transaction_level != 0:
            _DB_CONNECTOR.need_rollback = True
        if cursor:
            cursor.close()


@sql_with_logging
@with_connection
def select(sql):
    cursor = None
    success = False
    global _DB_CONNECTOR
    try:
        cursor = _DB_CONNECTOR.cursor()
        cursor.execute(sql)
        success = True
        results = [i for i in cursor]
        return results
    finally:
        if not success and _DB_CONNECTOR.transaction_level != 0:
            _DB_CONNECTOR.need_rollback = True
        if cursor:
            cursor.close()



@exception_handler
def insert_into(table_name, **args):
    keys = args.keys()
    values = [sql_format(args[key]) for key in keys]
    sql = "insert into {0} ({1})values({2})".format(
        table_name, ",".join(keys), ",".join(values))
    execute(sql)


@exception_handler
def select_from(table_name, **args):
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


@exception_handler
def delete_from(table_name, **args):
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


@exception_handler
def update(table_name, **args):
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


if __name__ == '__main__':
    config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
    config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                           [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
    ECHO = True
    create_engine(**config_args)
    print DB_ENGINE.conn.is_connected()
    try:
        with connection():
            print DB_ENGINE.conn.is_connected()
            print _DB_CONNECTOR.conn
            print 1
            raise Exception()
    except:
        print 'good'

    print _DB_CONNECTOR.conn
    print DB_ENGINE.conn.is_connected()
    close_engine()
    print DB_ENGINE

    create_engine(**config_args)
    select_from('stock', ticker='aapl')
    with connection():
        insert_into('stock', ticker='sheng')
        print DB_ENGINE.conn.is_connected()
        insert_into('stock', aticker='sheng')
    select_from('stock', name=None)
    update('stock', _ticker='sheng', _name=None, name='shengye')
    delete_from('stock', ticker="sheng", pv_close=None)

    with transaction():
        select_from('stock', ticker='aapl')
        insert_into('stock', ticker='sheng')
        update('stock', _ticker='sheng', _name=None, name='shengye')
        with transaction():
            select_from('stock', ticker='aapl')
            insert_into('stock', ticker='sheng')
            update('stock', _ticker='sheng', _name=None, name='shengye')
            delete_from('stock', ticker="sheng", pv_close=None)
        delete_from('stock', ticker="sheng", pv_close=None)
    close_engine()




