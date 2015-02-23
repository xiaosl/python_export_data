#!/bin/env python
# -*-coding:utf-8-*-
import sys
import MySQLdb
import config

class MysqlExec(object):
    mysql_config = None

    def __init__(self,mysql_config):
        Config = config.Config
        self.mysql_config = mysql_config

    def mysql_exec(slef,sql, mysql_config):
        """
        :param sql:
        :param db_name:talk
        :return:
        """
        cursor = None
        try:
            connect = MySQLdb.connect(host=mysql_config['host'], port=int(mysql_config['port']), user=mysql_config['username'],
                                  passwd=mysql_config['password'],db=mysql_config['database'],connect_timeout=5, charset='utf8')
            cursor = connect.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except MySQLdb.Error, e:
            error_content = "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print error_content
            sys.exit()
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def get_columns(self,table,database):
        #columns_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = %s" % (table)
        columns_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (table,database)
        columns = self.mysql_exec(columns_sql,self.mysql_config)
        return columns

    def get_data_count(self,table):
        count_sql = "select count(*) from %s" % (table)
        count = self.mysql_exec(count_sql,self.mysql_config)[0][0]
        return count

    def get_tables(self):
        tables = self.mysql_exec("show tables",self.mysql_config)
        return tables

    def get_datas(self,table,start,size):
        sql = "select * from %s order by id asc limit %d,%d" % (table,start,size)
        datas = self.mysql_exec(sql,self.mysql_config)
        return datas