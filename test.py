#!/bin/env python
# -*-coding:utf-8-*-

import commands
import sys
import mysqlExec
import saveFile
import delData
import config

def test(aa):
    l = []
    for i in aa:
        if i > 5:
            l.append(i*10)
        else:
            l.append(i/10)
    return l

x = [[2,8,3,9,3,1],[12,45,3,5,8,2],[8,9,6,3]]

m = map(test,x)
print m
sys.exit()
# def get_mysql_conf(mysql_server='talk_server'):
#     """
#     获取数据库配置
#     :param mysql_server:
#     :return:
#     """
#     host = config.get_config(mysql_server, 'host')
#     port = config.get_config(mysql_server, 'port')
#     username = config.get_config(mysql_server, 'username')
#     password = config.get_config(mysql_server, 'password')
#     database = config.get_config(mysql_server, 'database')
#
#     return {'config':mysql_server,'host':host,'port':port,'username':username,'password':password,'database':database}

# def get_encrypt_rules():
#     rules = {}
#     rules_items = config.get_config_items('rules')
#     for item in rules_items:
#         if item[1] :
#             table_keys = item[1].split(',')
#             for table_key in table_keys:
#                 keys = table_key.split('.')
#                 if keys[1] :
#                     if keys[0] in rules:
#                         rules[keys[0]][keys[1]]=item[0]
#                     else:
#                         rules[keys[0]] = {keys[1]:item[0]}
#
#     return rules


# def encrypt_data(data,columns,rules):
#
#     print
# def del_data_to_sql(table_name,columns,datas,rules):
#     list_datas = []
#     ##匹配规则
#     if table_name in rules:
#         table_rules = []
#         for i in range(len(columns)):
#             if columns[i] in rules:
#                 table_rules[i] = rules[columns[i]]
#         list_datas = map(encrypt_data,datas,columns,rules[table_name])
#
#     else:
#         list_datas = [list(line) for line in datas]
#     return list_datas

# def format_sql(table_name,list_datas):
#     """
#     处理数据，对特定字段做加密
#     :param table_name:
#     :param columns:
#     :param datas:
#     :param rules:
#     :return:
#     """
#     result_list = []
#
#     for list_data in list_datas:
#         str_data = ["'"+str(line)+"'" for line in list_data]
#         strsql = "INSERT INTO `%s` VALUES (%s)" % (table_name,','.join(str_data))
#         result_list.append(strsql)
#     return result_list

# def write_file(data_msg_list,filename='export.sql'):
#     """
#     写入文件
#     :param datas:
#     :param filename:
#     :return:
#     """
#     file_object = None
#     try:
#         file_object = open('output/'+filename, 'a')
#         file_object.writelines([line+'\n' for line in data_msg_list])
#     finally:
#         file_object.close()


# def mysql_exec(sql, mysql_config):
#     """
#     :param sql:
#     :param db_name:talk
#     :return:
#     """
#     cursor = None
#     try:
#         connect = MySQLdb.connect(host=mysql_config['host'], port=int(mysql_config['port']), user=mysql_config['username'],
#                                   passwd=mysql_config['password'],db=mysql_config['database'],connect_timeout=5, charset='gbk')
#         cursor = connect.cursor()
#         cursor.execute(sql)
#         result = cursor.fetchall()
#     except MySQLdb.Error, e:
#         error_content = "Mysql Error %d: %s" % (e.args[0], e.args[1])
#         raise error_content
#     finally:
#         if cursor is not None:
#             cursor.close()
#     return result


# mysql_config = []
# mysql_config.append(get_mysql_conf('talk_server'))
#获取导出数据配置
# export_config = get_export_conf()
# #获取数据过滤方法
# rules = get_encrypt_rules()
# #获取数据库配置
# mysql_config = get_mysql_conf('talk_server')

database = config.Config.mysql_config_list['talk_server']['database']
print database
sys.exit()
export_config = config.Config.export_config
# tables = mysql_exec("show tables",mysql_config)
tables = mysqlExec.MysqlExec.get_tables()
for table in tables:
    ##获取表中数据条数
    # count_sql = "select count(*) from %s" % (table)
    # count = mysql_exec(count_sql,mysql_config)[0][0]
    count = mysqlExec.MysqlExec.get_data_count()
    if count > 0:
        # columns_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (table[0],mysql_config['database'])
        # columns = mysql_exec(columns_sql,mysql_config)
        columns = mysqlExec.MysqlExec.get_columns(table,database)
        print columns
        sql = "select * from %s order by id asc " % (table)
        ##计算导出数量
        start = int(float(export_config['start'])*count)
        end = int(float(export_config['end'])*count)
        print start
        print end
        length = int(export_config['length'])
        if length > 0 and (end-start) > length:
            end = start + length
        ##考虑数据量可以循环获取
        page=1000
        # endnum = start + page
        while (start + page) <= end:
            # exec_sql = sql + " limit %d,500" % (start)
            # print exec_sql
            # datas = mysql_exec(exec_sql,mysql_config)
            datas = mysqlExec.MysqlExec.get_datas(table,start)
            if datas :
                data_msg_list = del_data_to_sql(table[0],columns,datas,rules)
                print data_msg_list
                sys.exit()
                write_file(data_msg_list)
                #写入文件
            # INSERT INTO `block` VALUES ('11', '系统权限管理', '211', '', 'on', '0', '2011-08-12 06:48:03', '2013-04-12 10:59:58', 'jiacj', '2');
            start += page
            break
        # sql += " limit %d,%d" % (start,length)

    break

