
import mysql.connector


class StockDAL:
    def __init__(self):
        self.conn = mysql.connector.connect(host='www.jdjw.org', user='jdjw', passwd='10041023', database='master_db')
        self.cur = self.conn.cursor()



    def insert_into(self,table_name, **args):
        keys = args.keys()
        values = [str(args[key]) for key in keys]

        sql = "insert into " + table_name + " (" + ",".join(keys) + ")values(" + ",".join(values) + ")"
        print sql
        self.cur.execute(sql)
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




a = StockDAL()
a.insert_into('stock_list', ticker="'apple'")
a.select_from('stock_list')



