# -*- coding: utf-8 -*-
import sublime
import sublime_plugin


class sublime_linter_config_open_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")


class sublime_linter_config_create_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")


class sublime_linter_config_switch_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")


class sublime_linter_config_remove_file_actions(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")
