#!usr/bin/env python
# -*- coding:utf-8 -*-

import os

def get_file_and_folder_list(dir_path, file_list: list, folder_list: list):
    if os.path.isfile(dir_path):
        file_list.append(dir_path)
    elif os.path.isdir(dir_path):
        for s in os.listdir(dir_path):
            if dir_path not in folder_list:
                folder_list.append(dir_path)
            get_file_and_folder_list(os.path.join(dir_path, s), file_list, folder_list)