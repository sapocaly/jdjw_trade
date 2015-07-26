# -*- coding: utf-8 -*-
import mysql.connector
import logging
import logging.config
import DBconfig


def sql_format(val):
    if isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif val == None:
        return 'null'
    else:
        return "'{0}'".format(str(val))

logging.config.fileConfig("../conf/jdjw_trade_logger.cfg")


# todo：支持更复杂的query范围，><等
# todo: 变量名等格式化
# todo: 异常处理
class StockDAL:

    # 控制是否输出sql todo:对connector反馈一并更好控制
    ECHO = True
    # todo:增加logger，logger也需要控制

    config = DBconfig.DBConfig("../conf/jdjw_trade_db.cfg")

    def __init__(self):
        # todo: 配置文件化
        # toda: 线程管理，资源管理
        self.logger = logging.getLogger("jdjw_trade_dal")
        self.logger_err = logging.getLogger("jdjw_trade_dal.err")
        self.conn = mysql.connector.connect(
            host=self.config.DB_HOST, user=self.config.DB_USER, passwd=self.config.DB_PASSWORD, database=self.config.DB_NAME)

    def close(self):
        self.conn.close()

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
                    sql += "{0} = {1} and ".format(key, sql_format(args[key]))
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
                    sql += "{0} = {1} and ".format(key, sql_format(args[key]))
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
                    where_clause += "{0} = {1} and ".format(
                        key, args['_' + key])
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
        try:
            if StockDAL.ECHO:
                print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            toReturn = [i for i in cur]
            cur.close()
            self.logger.info(sql)
            if StockDAL.ECHO:
                print toReturn
            return toReturn
        except Exception as e:
            print e
            self.logger_err.error(sql)
            self.logger_err.exception(str(e))

    def execute(self, sql):
        try:
            if StockDAL.ECHO:
                print sql
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            self.logger.info(sql)
        except Exception as e:
            print e
            self.logger_err.error(sql)
            self.logger_err.exception(str(e))

if __name__ == '__main__':
    a = StockDAL()
    a.insert_into('stock', ticker="uber", name=None)
    a.insert_into('stock', aticker="uber", name=None)
    a.update('stock', _ticker="uber", name="优步")
    a.select_from('stock', ticker="ali")
    a.close()
    print 'finished'
