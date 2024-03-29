# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import os
from zipfile import ZipFile
import urllib.request
from io import BytesIO

try:
    from .lib import sys_define as sys_def
    from .lib.file_handler import FlieHandler
    from .lib.command import Command
except ImportError:
    from lib import sys_define as sys_def
    from lib.file_handler import FlieHandler
    from lib.command import Command


def _show_config_file_panel(view: object, call_back_func: object) -> list:
    window = view.window()
    pkg_path = sublime.packages_path()
    cfg_path = os.path.join(pkg_path, sys_def.USER_FOLDER)

    res_list = FlieHandler.find_file(cfg_path, sys_def.FILE_NAME_FORMAT)

    if len(res_list) == 0:
        sublime.message_dialog(
            "SublimelinterComfig can't find the config files, please create it!")
    else:
        window.show_quick_panel(res_list, call_back_func)

    return res_list


def _check_idx(idx: int) -> bool:
    return idx >= sys_def.INVAILD_ID


def _create_default_cfg_file():
    pkg_path = sublime.packages_path()
    plugin_path = os.path.join(pkg_path, sys_def.DEFAULT_DIR)
    cfg_path = os.path.join(pkg_path, sys_def.DEFAULT_DIR + sys_def.DEFAULT_CONFIG_DIR)

    folder = os.path.exists(plugin_path)
    if not folder:
        os.makedirs(plugin_path)

    folder = os.path.exists(cfg_path)
    if not folder:
        os.makedirs(cfg_path)

    url = urllib.request.urlopen(sys_def.SETTING_URL)
    default_cfg_path = os.path.join(pkg_path,
        sys_def.DEFAULT_DIR + sys_def.DEFAULT_CONFIG_DIR + sys_def.DEFAULT_CONFIG_FIEL_NAME)

    with ZipFile(BytesIO(url.read())) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            with open(default_cfg_path, "wb") as output:
                for line in my_zip_file.open(contained_file).readlines():
                    # print(line)
                    output.write(line)
                output.close()

def _open_setting(file_name) -> None:
    pkg_path = sublime.packages_path()
    cfg_path = os.path.join(pkg_path, sys_def.USER_FOLDER)

    default_cfg_path = os.path.join(pkg_path,
        sys_def.DEFAULT_DIR + sys_def.DEFAULT_CONFIG_DIR + sys_def.DEFAULT_CONFIG_FIEL_NAME)

    if not os.path.exists(default_cfg_path):
        _create_default_cfg_file()

    window = sublime.active_window()
    view = window.open_file(default_cfg_path)
    view.set_read_only(True)

    window.run_command('set_layout',
                       {"cols": [0.0, 0.5, 1.0],
                        "rows": [0.0, 1.0],
                        "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]}
                       )
    file_path = os.path.join(cfg_path, file_name)
    window.open_file(file_path)


class sublime_linter_config_open_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit: object) -> None:
        # self.view.insert(edit, 0, "Hello, World1!")
        view = self.view
        sublime_linter_config_open_file_actions._RES_LIST = \
            _show_config_file_panel(view,
                                    sublime_linter_config_open_file_actions._on_done)

    @staticmethod
    def _on_done(idx) -> None:
        # type: (int) -> None
        if not _check_idx(idx):
            return

        file_name = sublime_linter_config_open_file_actions._RES_LIST[idx]
        sublime_linter_config_open_file_actions._RES_LIST = []
        _open_setting(file_name)


class sublime_linter_config_create_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit) -> None:
        # self.view.insert(edit, 0, "Hello, World2!")
        view = self.view
        window = view.window()

        window.show_input_panel('The sublimelinter config file name:', '',
                                sublime_linter_config_create_file_actions._on_done,
                                None,
                                None)

    @staticmethod
    def _on_done(line_str: str) -> None:
        pkg_path = sublime.packages_path()
        cfg_path = os.path.join(pkg_path, sys_def.USER_FOLDER)
        sublime_linter_config_create_file_actions._RES_LIST = FlieHandler.find_file(
            cfg_path, sys_def.FILE_NAME_FORMAT)

        file_name = line_str + sys_def.FILE_NAME_TYPE

        if file_name in sublime_linter_config_create_file_actions._RES_LIST:
            sublime.message_dialog("This config file already exists!")
            return

        file_path = os.path.join(cfg_path, file_name)
        file_object = open(file_path, "x")
        file_object.close

        _open_setting(file_name)
        sublime.set_timeout(sublime_linter_config_create_file_actions._set_template,
                            200)

    @staticmethod
    def _set_template() -> None:
        window = sublime.active_window()
        view = window.active_view()
        view.run_command('sublime_linter_config_write_default_file_actions')


class sublime_linter_config_write_default_file_actions(sublime_plugin.TextCommand):
    def run(self, edit:object) -> None:
        view = self.view
        view.insert(edit, 0, "// sublime linter config \n{\n\n}\n")


class sublime_linter_config_switch_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit: object) -> object:
        view = self.view
        sublime_linter_config_switch_file_actions._RES_LIST = \
            _show_config_file_panel(view,
                                    sublime_linter_config_switch_file_actions._on_done)

    @staticmethod
    def _on_done(idx:int) -> object:
        # type: (int) -> None
        if not _check_idx(idx):
            return

        file_name = sublime_linter_config_switch_file_actions._RES_LIST[idx]
        sublime_linter_config_switch_file_actions._RES_LIST = []
        pkg_path = sublime.packages_path()
        cfg_path = os.path.join(pkg_path, sys_def.USER_FOLDER)
        default_cfg_path = os.path.join(cfg_path, 'SublimeLinter.sublime-settings')
        Command.remove_file(default_cfg_path)
        file_path = os.path.join(cfg_path, file_name)
        Command.copy_file(file_path, default_cfg_path)

        window = sublime.active_window()
        view = window.active_view()
        view.run_command('sublime_linter_reload')


class sublime_linter_config_remove_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit: object) -> None:
        view = self.view
        sublime_linter_config_remove_file_actions._RES_LIST = \
            _show_config_file_panel(view,
                                    sublime_linter_config_remove_file_actions._on_done)

    @staticmethod
    def _on_done(idx: int) -> None:
        # type: (int) -> None
        if not _check_idx(idx):
            return

        line_str = sublime_linter_config_remove_file_actions._RES_LIST[idx]
        sublime_linter_config_remove_file_actions._RES_LIST = []
        pkg_path = sublime.packages_path()
        cfg_path = os.path.join(pkg_path, sys_def.USER_FOLDER)

        file_path = os.path.join(cfg_path, line_str)
        Command.remove_file(file_path)
