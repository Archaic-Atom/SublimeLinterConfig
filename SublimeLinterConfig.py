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
            return

        sublime.message_dialog(sublime_linter_config_open_file_actions._RES_LIST[idx])
        sublime_linter_config_open_file_actions._RES_LIST = []


class sublime_linter_config_create_file_actions(sublime_plugin.TextCommand):
    _RES_LIST = []

    def run(self, edit):
        view = self.view
        window = view.window()

        window.show_input_panel(sys_def.OUR_CAPTION, "",
                                sublime_linter_config_create_file_actions._on_done,
                                None,
                                None)
        # self.view.insert(edit, 0, "Hello, World2!")

    @staticmethod
    def _on_done(line_str: str):
        pkg_path = sublime.packages_path()
        cfg_pth = os.path.join(pkg_path, sys_def.USER_FOLDER)
        sublime_linter_config_create_file_actions._RES_LIST = FlieHandler.find_file(
            cfg_pth, sys_def.FILE_NAME_FORMAT)
        sublime.message_dialog(line_str)


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
