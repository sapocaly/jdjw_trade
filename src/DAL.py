# -*- coding: utf-8 -*-
import mysql.connector
import logging


def sql_format(val):
    if isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif val == None:
        return 'null'
    else:
        return "'{0}'".format(str(val))


# todo：支持更复杂的query范围，><等
# todo: 变量名等格式化
# todo: 异常处理
class StockDAL:

    # 控制是否输出sql todo:对connector反馈一并更好控制
    ECHO = True
    # todo:增加logger，logger也需要控制

    def __init__(self):
        # todo: 配置文件化
        # toda: 线程管理，资源管理
        #self.logger = logging.getLogger("jdjw_trade_dal")
        self.conn = mysql.connector.connect(
            host='www.jdjw.org', user='jdjw', passwd='10041023', database='master_db')

    def insert_into(self, table_name, **args):
        try:
            cursor = self.conn.cursor()
            keys = args.keys()
            values = [sql_format(args[key]) for key in keys]
            sql = "insert into {0} ({1})values({2})".format(
                table_name, ",".join(keys), ",".join(values))
            if StockDAL.ECHO:
                print sql
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e

    def select_from(self, table_name, **args):
        try:
            if len(args) > 0:
                sql = "select * from {0} where ".format(table_name)
                for key in args:
                    sql += "{0} = {1} and ".format(key, sql_format(args[key]))
                sql = sql[:-5]
            else:
                sql = "select * from " + table_name
            if StockDAL.ECHO:
                print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            toReturn = [i for i in cur]
            if StockDAL.ECHO:
                print toReturn
            return toReturn
        except Exception as e:
            print e

    def delete_from(self, table_name, **args):
        try:
            if len(args) > 0:
                sql = "delete from {0} where ".format(table_name)
                for key in args:
                    sql += "{0} = {1} and ".format(key, sql_format(args[key]))
                sql = sql[:-5]
            else:
                sql = "select * from " + table_name
            if StockDAL.ECHO:
                print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e

    def select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        toReturn = [i for i in cur]
        return toReturn

    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

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
                    where_clause += "{0} = {1} and ".format(
                        key, args['_' + key])
                where_clause = where_clause[:-5]
            update_clause = ''
            for key in update_keys:
                update_clause += "{0} = {1}, ".format(key, args[key])
            update_clause = update_clause[:-2]
            print update_clause
            sql = "update {0} set {1} {2}".format(
                table_name, update_clause, where_clause)
            if StockDAL.ECHO:
                print sql
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e


if __name__ == '__main__':
    l = []
    for i in range(10):
        l.append(StockDAL())
    a = StockDAL()
    a.insert_into('stock', ticker="uber", name=None)
    #a.select_from('stock', ticker="ali")
    a.delete_from('stock', ticker="uber")
