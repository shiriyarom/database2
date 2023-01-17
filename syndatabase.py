"""
author: Shiri Yarom
name: SynDataBase
description: sync of the readers and the writters
so they would have te accsses by the right rules
"""


import multiprocessing
from filedatabase import FileDatabase
import win32event


class SynDataBase():

    def __init__(self, mode, database):
        """
              init class that sync between readers and writers
              :param mode: threading/ processing
              :param database
              """
        self.database = database
        self.semaphore = win32event.CreateSemaphore(None, 10, 10, 'semaphore')
        self.lock = win32event.CreateMutex(None, False, 'lock')

    def write_data(self):
        """
              have the accseed to changes values in the dictionary
              :return: None
              """
        win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        for k in range(10):
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        print("writer has an access")

    def write_release(self):
        """
               release access to change values in the dictionary
               :return: None
            self.semaphore.release()
        self.lock.release()
               """
        win32event.ReleaseSemaphore(self.semaphore, 10)
        win32event.ReleaseMutex(self.lock)
        logging.debug("writer released an access")

        def read_data(self):
            """
            get access to read details in the dictionary
            :return: None
            """
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
            print("reader has an access")

        def read_release(self):
            """
            release access to read details in the dictionary
            :return: None
            """
            win32event.ReleaseSemaphore(self.semaphore, 1)
            print("reader released an access")

    def get_value(self, key):
        """
                returns in the dictionary the value of the value before of
                the key
                :param key
                :return: flag - the value of the value of the key's dictionary
                """
        self.read_data()
        flag = self.database.get_value(key)
        self.read_release()
        return flag

    def set_value(self, key, val):
        """
             changes in the dictionary the value of the value before of
             the key
             :param key
             :param val
             :return: flag - True/ False if it works
             """
        self.write_data()
        flag = self.database.set_value(key, val)
        self.write_release()
        return flag

    def delete_value(self, key):
        """
                    deletes in the dictionary the value of the value before of
                     the key
                     :param key
                     :param val
                     :return: flag - True/ False if it works
                     """
        self.write_data()
        flag = self.database.delete_value(key)
        self.write_release()
        return flag


