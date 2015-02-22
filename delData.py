#!/usr/bin/env python
# coding=utf-8
#__author__ = 'xiaosl'

import encryptFunction as func
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class DelData(object):
    table = None
    data_list = None
    datas = None
    columns = []
    table_rules = {}
    result_list = []
    function_list = {}
    
    def __init__(self):
        default_fun = ['__builtins__','__doc__','__file__','__name__','__package__']
        attr_list = dir(func)
        for i in attr_list:
            if hasattr(func,i) and i not in default_fun:
                self.function_list[i] = getattr(func, i)
    ##用完务必值为None
    def del_rules(self):
        self.table_rules = {}
    
    def set_rules(self,rules):
        for i in range(len(self.columns)):
            if self.columns[i] in rules:
                self.table_rules[i] = self.function_list[rules[self.columns[i]]]

def set_table(self,table):
    self.table = table
    
    def set_columns(self,columns):
        for column in columns:
            self.columns.append(column[0])

def set_datas(self,datas):
    self.datas = datas
    
    def del_datas(self):
        self.data_list = map(self.encrypt_data,self.datas)
        self.format_sql()
        return self.result_list
    def format_sql(self):
        """
            处理数据，对特定字段做加密
            :param table_name:
            :param columns:
            :param datas:
            :param rules:
            :return:
            """
        for data in self.data_list:
            data_temp = ["'"+str(line)+"'" for line in data]
            strsql = "INSERT INTO `%s` VALUES (%s);" % (self.table,','.join(data_temp))
            self.result_list.append(strsql)

def encrypt_data(self,data):
    list_temp = []
        for i in range(len(data)):
            if i in self.table_rules:
                list_temp.append(apply(self.table_rules[i],(data[i],)))
            else:
                list_temp.append(data[i])
    return list_temp
