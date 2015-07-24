
# -*- coding: utf-8 -*- 
import mysql.connector



class StockDAL:
    def __init__(self):
        #todo: 配置文件化
        self.conn = mysql.connector.connect(host='www.jdjw.org', user='jdjw', passwd='10041023', database='master_db')



    def insert_into(self,table_name,**args):
        cursor = self.conn.cursor()
        keys = args.keys()
        values = ["'{0}'".format(args[key]) if isinstance(args[key], basestring) else (str(args[key]) if args[key] != None else 'null') for key in keys]
        sql = "insert into {0} ({1})values({2})".format(table_name, ",".join(keys), ",".join(values))
        print sql
        cursor.execute(sql)
        self.conn.commit()

    def select_from(self, table_name, **args):
        if len(args) > 0:
            sql = "select * from {0} where ".format(table_name)
            for key in args:
                sql += "{0} = {1} and ".format(key, "'{0}'".format(args[key]) if isinstance(args[key], basestring) else (str(args[key]) if args[key] != None else 'null'))
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
    a.insert_into('stock_list', ticker="uber", name=None)
    a.select_from('stock_list', ticker="ali")



