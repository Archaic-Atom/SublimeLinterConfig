# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import os
from .lib import sys_define as sys_def
from .lib.file_handler import FlieHandler


class sublime_linter_config_open_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit):
        # self.view.insert(edit, 0, "Hello, World1!")
        view = self.view
        window = view.window()

        pkg_path = sublime.packages_path()
        cfg_pth = os.path.join(pkg_path, sys_def.USER_FOLDER)

        sublime_linter_config_open_file_actions._RES_LIST = FlieHandler.find_file(
            cfg_pth,
            sys_def.FILE_NAME_FORMAT)

        window.show_quick_panel(sublime_linter_config_open_file_actions._RES_LIST,
                                sublime_linter_config_open_file_actions._on_done)

    @staticmethod
    def _on_done(idx):
        # type: (int) -> None
        if idx < sys_def.INVAILD_ID:
            sublime.message_dialog(
                "SublimelinterComfig can't find the config files, please create it!")
            return

        sublime.message_dialog(sublime_linter_config_open_file_actions._RES_LIST[idx])
        sublime_linter_config_open_file_actions._RES_LIST = []


class sublime_linter_config_create_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit):
        # self.view.insert(edit, 0, "Hello, World2!")
        view = self.view
        window = view.window()

        window.show_input_panel('The sublimelinter config file name:', '',
                                sublime_linter_config_create_file_actions._on_done,
                                None,
                                None)

    @staticmethod
    def _on_done(line_str: str):
        pkg_path = sublime.packages_path()
        cfg_pth = os.path.join(pkg_path, sys_def.USER_FOLDER)
        sublime_linter_config_create_file_actions._RES_LIST = FlieHandler.find_file(
            cfg_pth, sys_def.FILE_NAME_FORMAT)

        line_str = line_str + sys_def.FILE_NAME_TYPE

        if line_str in sublime_linter_config_create_file_actions._RES_LIST:
            sublime.message_dialog("This config file already exists!")
            return

        sublime.run_command("new_window")
        default_cfg_path = os.path.join(pkg_path, sys_def.DEFAULT_CONFIG_PATH)

        window = sublime.active_window()
        window.open_file(default_cfg_path)
        view = window.new_file()
        view.set_name(line_str)
        window.run_command('set_layout',
                           {"cols": [0.0, 0.5, 1.0],
                            "rows": [0.0, 1.0],
                            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]}
                           )


class sublime_linter_config_switch_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        pkg_path = sublime.packages_path()
        pass
        # self.view.insert(edit, 0, "Hello, World3!")


class sublime_linter_config_remove_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        pkg_path = sublime.packages_path()
        # self.view.insert(edit, 0, "Hello, World4!")
        pass
