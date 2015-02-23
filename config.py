#!/bin/env python
# -*-coding:utf-8-*-

import os
import ConfigParser
import threading

class Config(object):
    mysql_config_list = {}
    export_config = {}
    rules = {}

    instance=None

    mutex=threading.Lock()

    def _init__(self):
        pass
    @staticmethod
    def GetInstance():
        if(Config.instance==None):
            Config.mutex.acquire()
            if(Config.instance==None):
                Config.instance=Config()
                Config.instance.init_config()
            Config.mutex.release()
        return Config.instance

    def init_config(self):
        self.get_mysql_conf()
        self.get_export_conf()
        self.get_encrypt_rules()

    def get_config(self,group, config_name, ini_name='mysql_config.ini'):
        config = ConfigParser.ConfigParser()
        config_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'config/%s' % ini_name).replace('\\', '/'))
        config.readfp(open(config_path, 'rw'))
        config_value = config.get(group, config_name).strip(' ').strip('\'').strip('\"')
        return config_value

    def get_config_items(self,group,ini_name='main.ini'):
        config = ConfigParser.ConfigParser()
        config_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'config/%s' % ini_name).replace('\\', '/'))
        config.readfp(open(config_path, 'rw'))
        config_value = config.items(group)
        return config_value

    def get_export_conf(self):
        """
        获取导出数据配置
        :return:
        """
        start = self.get_config('export', 'start','main.ini')
        end = self.get_config('export', 'end','main.ini')
        length = self.get_config('export', 'length','main.ini')
        self.export_config = {'start':start,'end':end,'length':length,'rules':[]}

    def get_encrypt_rules(self):
        rules_items = self.get_config_items('rules')
        for item in rules_items:
            if item[1] :
                table_keys = item[1].split(',')
                for table_key in table_keys:
                    keys = table_key.split('.')
                    if keys[1] :
                        if keys[0] in self.rules:
                            self.rules[keys[0]][keys[1]]=item[0]
                        else:
                            self.rules[keys[0]] = {keys[1]:item[0]}

    def get_mysql_conf(self,mysql_server='talk_server'):
        """
        获取数据库配置
        :param mysql_server:
        :return:
        """
        host = self.get_config(mysql_server, 'host')
        port = self.get_config(mysql_server, 'port')
        username = self.get_config(mysql_server, 'username')
        password = self.get_config(mysql_server, 'password')
        database = self.get_config(mysql_server, 'database')

        self.mysql_config_list[mysql_server] = {'config':mysql_server,'host':host,'port':port,'username':username,'password':password,'database':database}



