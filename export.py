#!/bin/env python
# -*-coding:utf-8-*-

import commands
import sys
import mysqlExec
import saveFile
import delData
import config

the_config = config.Config.GetInstance()
mysql = mysqlExec.MysqlExec(the_config.mysql_config_list['talk_server'])
del_data = delData.DelData()
save_file = saveFile.SaveFile()

export_config = the_config.export_config
tables = mysql.get_tables()
for table in tables:
    ##获取表中数据条数
    count = mysql.get_data_count(table[0])
    if count > 0:
        columns = mysql.get_columns(table[0],the_config.mysql_config_list['talk_server']['database'])
        del_data.set_table(table[0])
        del_data.set_columns(columns)
        if table[0] in the_config.rules:
            del_data.set_rules(the_config.rules[table[0]])
        ##计算导出数量
        start = int(float(export_config['start'])*count)
        end = int(float(export_config['end'])*count)
        print start
        print end
        length = int(export_config['length'])
        if length > 0 and (end-start) > length:
            end = start + length
        ##考虑数据量可以循环获取
        size=500
        while start <= end:
            if (start+size) > end:
                size = end-start
            datas = mysql.get_datas(table[0],start,size)
            print datas
            if datas :
                del_data.set_datas(datas)
                data_msg_list = del_data.del_datas()
                print data_msg_list

                save_file.write_file(data_msg_list)
            start += size


