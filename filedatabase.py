"""
author: Shiri Yarom
name: database
description: actions for the dictionary
while using the file
"""

from database import DataBase
import pickle
import win32file


class FileDataBase(DataBase):

    def __init__(self, file):
        """
                 init a class that has a dictionary in a file
                 :param file
                 """
        super().init()
        self.file = file
        try:
            FILE = open(self.file, "x")
        except:
            pass

    def load(self):
        """
                read from the file
                :return: None
                """

        with open("dbfile.txt", "rb") as file:
            self.dict = pickle.load(file)

    def dump(self):
        """
               write in the file
               :return: None
               """
        data = pickle.dumps(self.dict)
        file = win32file.CreateFile(self.file, win32file.GENERIC_WRITE, 0, None, win32file.CREATE_ALWAYS, 0, None)
        win32file.WriteFile(file, data)
        win32file.CloseHandle(file)

    def get_value(self, key):
        """
               returns in the dictionary the value of the value before of
                the key
               :param key
               :return: the value of the value of the key's dictionary
               """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """
                            deletes in the dictionary the value of the value before of
                             the key
                             :param key
                             :return: the value that deleted
                             """
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val

    def set_value(self, key, val):
        """
                     changes in the dictionary the value of the value before of
                     the key
                     :param key
                     :param val
                     :return: True/ False if it works
                     """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag



