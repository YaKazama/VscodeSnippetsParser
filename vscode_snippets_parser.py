# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import sublime_plugin
from . import parser
from . import settings


class VscodeSnippetsParserCommand(sublime_plugin.TextCommand):
    def run(self, edit, is_run=False):
        if not is_run:
            is_run = settings.get("vscode_run_at_startup")

        if is_run:
            parser.parser_file(edit)
