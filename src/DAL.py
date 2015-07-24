
# -*- coding: utf-8 -*- 
import mysql.connector



class StockDAL:
    def __init__(self):
        #todo: 配置文件化
        self.conn = mysql.connector.connect(host='www.jdjw.org', user='jdjw', passwd='10041023', database='master_db')



    def insert_into(self,table_name, *args, **args_dict):
        cursor = self.conn.cursor()
        print args
        keys = args_dict.keys()
        values = ["'{0}'".format(args_dict[key]) if isinstance(str(args_dict[key]), basestring) else str(args_dict[key]) for key in keys]
        sql = "insert into {0} ({1})values({2})".format(table_name, ",".join(keys), ",".join(values))
        print sql
        cursor.execute(sql)
        self.conn.commit()

    def select_from(self, table_name, **args):
        if len(args) > 0:
            sql = "select * from " + table_name + " where "
            for key in args:
                sql += key + '=' + str(args[key]) + ' and '
            sql = sql[:-5]
        else:
            sql = "select * from " + table_name
        print sql
        cur = self.conn.cursor()
        cur.execute(sql)
        toReturn = [i for i in cur]
        print toReturn
        return toReturn



if __name__ =='__main__':
    a = StockDAL()
    a.insert_into('stock_list', ticker="ali")
    a.select_from('stock_list')



