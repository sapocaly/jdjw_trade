# -*- coding: utf-8 -*-
import threading

import mysql.connector

import src.utils.LogConstant as LogConstant
from src.utils import DBconfig

config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")

logger = LogConstant.DAL_DIGEST_LOGGER
logger_err = LogConstant.DAL_DIGEST_LOGGER_ERROR

ECHO = False


class Connection(threading.local):
    def __init__(self):
        self.conn = None

    def cursor(self):
        if not self.conn:
            self.conn = mysql.connector.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD,
                                                database=config.DB_NAME)
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def clean(self):
        self.conn.close()
        self.conn = None


DB_CONNECTION = Connection()


def sql_format(val):
    if isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif val is None:
        return 'null'
    else:
        return "'{0}'".format(str(val))


def close():
    DB_CONNECTION.clean()


def execute(sql):
    cursor = DB_CONNECTION.cursor()
    try:
        if ECHO:
            print sql
        cursor.execute(sql)
        DB_CONNECTION.commit()
        logger.info(sql)
    except Exception as e:
        print e
        logger_err.error(sql)
        logger_err.exception(str(e))
    cursor.close()


def select(sql):
    cursor = DB_CONNECTION.cursor()
    try:
        if ECHO:
            print sql
        cursor.execute(sql)
        toReturn = [i for i in cursor]
        logger.info(sql)
        if ECHO:
            print toReturn
        return toReturn
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


# todo：支持更复杂的query范围，><等
# todo: 变量名等格式化
# todo: 异常处理
class StockDAL:
    # 控制是否输出sql todo:对connector反馈一并更好控制
    ECHO = False
    # todo:增加logger，logger也需要控制

    config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")

    def __init__(self):
        # todo: 配置文件化
        # toda: 线程管理，资源管理
        self.logger = LogConstant.DAL_DIGEST_LOGGER
        self.logger_err = LogConstant.DAL_DIGEST_LOGGER_ERROR
        self.conn = mysql.connector.connect(
            host=self.config.DB_HOST, user=self.config.DB_USER, passwd=self.config.DB_PASSWORD,
            database=self.config.DB_NAME)

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print e
            self.logger_err.exception(str(e))

    def insert_into(self, table_name, **args):
        try:
            cursor = self.conn.cursor()
            keys = args.keys()
            values = [sql_format(args[key]) for key in keys]
            sql = "insert into {0} ({1})values({2})".format(
                table_name, ",".join(keys), ",".join(values))
            self.execute(sql)
        except Exception as e:
            print e
            self.logger_err.exception(str(e))

    def select_from(self, table_name, **args):
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

            return self.select(sql)
        except Exception as e:
            print e
            self.logger_err.exception(str(e))

    def delete_from(self, table_name, **args):
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
            self.execute(sql)
        except Exception as e:
            print e
            self.logger_err.exception(str(e))

    def update(self, table_name, **args):
        try:
            cur = self.conn.cursor()
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
            self.execute(sql)
        except Exception as e:
            print e
            self.logger_err.exception(str(e))

    def select(self, sql):
        cur = self.conn.cursor()
        try:
            if StockDAL.ECHO:
                print sql
            cur.execute(sql)
            toReturn = [i for i in cur]
            self.logger.info(sql)
            if StockDAL.ECHO:
                print toReturn
            return toReturn
        except Exception as e:
            print e
            self.logger_err.error(sql)
            self.logger_err.exception(str(e))
        cur.close()

    def execute(self, sql):
        ##这块要研究下
        cur = self.conn.cursor()
        try:
            if StockDAL.ECHO:
                print sql
            cur.execute(sql)
            # 坑？？
            self.conn.commit()
            self.logger.info(sql)
        except Exception as e:
            print e
            self.logger_err.error(sql)
            self.logger_err.exception(str(e))
        cur.close()


if __name__ == '__main__':
    StockDAL.ECHO = True
    ECHO = True
    a = StockDAL()
    a.insert_into('stock', ticker="uber", name=None)
    a.insert_into('stock', aticker="uber", name=None)
    a.select_from('stock', ticker="uber", name=None)
    a.update('stock', _ticker="uber", _name=None, name="优步")
    a.delete_from('stock', ticker='uber', pv_close=None)
    a.close()
    insert_into('stock', ticker='sheng')
    select_from('stock', name=None)
    update('stock', _ticker='sheng', _name=None, name='shengye')
    delete_from('stock', ticker="sheng", pv_close=None)
    close()
    print 'finished'
