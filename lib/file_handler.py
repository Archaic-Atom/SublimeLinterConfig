# -*- coding: utf-8 -*-
import os
import glob


class FlieHandler(object):
    """docstring for FlieHandler"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def find_file(folder_path: str, filename_format: str) -> list:
        assert os.path.isdir(folder_path)

        tmp_files = glob.glob(os.path.join(folder_path, filename_format))
        res_list = []

        for tmp_file in tmp_files:
            file_name = os.path.split(tmp_file)[-1]
            res_list.append(file_name)

        return res_list

    @staticmethod
    def download_setting(url: str, path: str) -> None:
        pass