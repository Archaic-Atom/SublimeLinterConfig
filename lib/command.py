# -*- coding: utf-8 -*-
import os
import shutil


class Command(object):
    """docstring for Command"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def remove_file(path):
        os.remove(path)

    @staticmethod
    def copy_file(source_path, traget_path):
        shutil.copyfile(source_path, traget_path)
