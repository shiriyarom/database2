"""
author: Shiri Yarom
name: threading
description: it checks the sync of writers and readers while
mode is threading
"""

from database import DataBase
from filedatabase import FileDataBase
from syndatabase import SynDataBase
from threading import Thread
import logging
import win32process
import win32event

Fname = "newfile"
MODE = "threading"



def reader_db(database):
    """
    reader is trying to get an access to read
    the value from the dictionary
    :param database
    :return: None
    """
    print("reader started")
    for k in range(100):
        flag = database.get_value(k) == k or database.get_value(k) is None
        assert flag
    print("reader left")

def writer_db(database):
    """
    writer is trying to get an access to write the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    :return: None
    """
    print("writer started")
    for k in range(100):
        assert database.set_value(k, k)
    for k in range(100):
        flag = database.delete_value(k) == k or database.delete_value(k) is None
        assert flag
    print("writer left")


def main():
    """
         running of the writers and the readers while combine
          them togheter by using threading
        :return: None
        """

    logging.basicConfig(filename='logging_thread.text',
      level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    data = SynDataBase(MODE, FileDataBase(Fname))
    SynDataBase.write_db(data)
    SynDataBase.read_db(data)
    # הרשאת כתיבה כאשר יש תחרות
    print(" other process running  ")
    all_threads = []
    for i in range(1000, 1100):
        data.set_value(i, i)
    count = 0
    for i in range(0, 50):
        thread = Thread(target=reader_db, args=(data,))
        all_threads.append(thread)
        thread = win32process.beginthreadex(None, 1000, writer_db, (data,), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            count += 1
    for i in range(0, 10):
        thread = Thread(target=writer_db, args=(data,))
        all_threads.append(thread)
    for i in all_threads:
        i.start()
    for i in all_threads:
        i.join()
    for i in range(1000, 1100):
        assert data.get_value(i) == i
        thread = win32process.beginthreadex(None, 1000, reader_db, (data,), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            count += 1
    assert count == 60


if __name__ == "main":
  main()
