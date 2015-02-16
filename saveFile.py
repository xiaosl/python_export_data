#!/bin/env python
# -*-coding:utf-8-*-

class SaveFile(object):
    desc_file = 'output/export.sql'

    def write_file(self,data_msg_list):
        """
        写入文件
        :param datas:
        :param filename:
        :return:
        """
        file_object = None
        try:
            file_object = open(self.desc_file, 'a')
            file_object.writelines([line+'\n' for line in data_msg_list])
        finally:
            file_object.close()
    # @staticmethod
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