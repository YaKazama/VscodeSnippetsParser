# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import os
import re
import json
from . import sublime
from . import settings


def get_cache_file():
    cache_end_point = [
        "VsParser", "VsParser.completions.cache"
    ]
    _file_path = [sublime.cache_path()] + cache_end_point

    _file_path = os.path.join(*_file_path)
    cache_dir = os.path.dirname(_file_path)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return _file_path


def save_cache(content=None, mode="w", newline=True):
    line_break = settings.get("vscode_line_break")
    _cache = settings.get("vscode_save_cache_to_file")
    if _cache:
        _cache_path = get_cache_file()
        if os.path.exists(_cache_path):
            os.remove(_cache_path)

        with open(_cache_path, mode) as f:
            if newline and not line_break:
                f.write(content + line_break)
            else:
                f.write(content)


def get_filter_file():
    filter_end_point = [
        "VscodeSnippetsParser",
        "Filter",
        settings.get("vscode_filter_file", "vscode_filter_file.json")
    ]
    packages_path = sublime.packages_path()
    _filter_path = [packages_path] + filter_end_point

    _filter_path = os.path.join(*_filter_path)
    filter_dir = os.path.dirname(_filter_path)

    if not os.path.exists(filter_dir):
        os.makedirs(filter_dir)
    return _filter_path


def save_filter(content=None, mode="w", newline=True):
    _filter = settings.get("vscode_save_filter_to_file")
    content = re.sub(r',*(\n\s+[\}\]])', r'\1', "".join(content))
    if _filter:
        _filter_path = get_filter_file()
        if os.path.exists(_filter_path):
            os.remove(_filter_path)

        with open(_filter_path, mode) as f:
            f.write(content)
