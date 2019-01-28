# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import os
import re
import json
import sublime
from . import settings
from . import cache
from . import project

RE_BLANK_LINE = r"^\s*$"
RE_LINE = r"^(/){2,}.*|(\s)*[^:\"](/){2,}.*\"?|((\s)*/\*(.*)\*/)"
RE_MULTI_LINE_START = r"^(\s*(/\*)+|(/\*)+)+.*"
RE_MULTI_LINE_END = r".*\*/.*$"
RE_REPLACE = r"[/():\ ]"
RE_DESCRIPTION = r"[<>]"


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def view_delete_all(view):
    view.run_command("select_all")
    view.run_command("right_delete")


def view_move_cursor(view, region):
    view.sel().clear()
    view.sel().add(region)
    return view.sel()[0]


def view_load_file(view, edit, path):
    if not os.path.exists(path):
        raise TypeError("File not exists")

    vscode_extensions = settings.get("vscode_extensions")

    if os.path.splitext(path)[-1] not in vscode_extensions:
        raise TypeError("The extensions not allow.")

    with open(path, "r") as f:
        contents = f.read()
        view.set_name(path)
        view_delete_all(view)
        view.insert(edit, 0, contents)


def filter_file(edit, path):
    _start = []
    _end = []
    contents = []
    line_break = settings.get("vscode_line_break")
    _is_save_filter = settings.get("vscode_save_filter_to_file")

    view = settings.get_output_panel()
    view_load_file(view, edit, path)

    region_lines = view.lines(sublime.Region(0, view.size()))

    for _region in region_lines:
        content = view.substr(_region)
        content = re.sub(RE_LINE, "", content)
        if re.match(RE_MULTI_LINE_START, content):
            _start.append(_region)
            continue
        else:
            if re.match(RE_MULTI_LINE_END, content):
                _end.append(_region)
                continue
            if _start and not _end:
                continue
            _start = []
            _end = []
        if not re.match(RE_BLANK_LINE, content):
            if line_break:
                content = content + line_break
            contents.append(content)
    if _is_save_filter:
        cache.save_filter(contents)
    return contents


def load_filter_json(edit):
    _filter = settings.get("vscode_save_filter_to_file")
    _filter_json = {}
    if _filter:
        json_file = cache.get_filter_file()
        with open(json_file) as f:
            _filter_json = json.load(f)
        if os.path.exists(json_file):
            os.remove(json_file)
    return _filter_json


def parser_and_save_json_completions(data):
    _key = ""
    json_new_dict = {}
    _dict_completions = []
    _scopes_dict = settings.get("vscode_scopes")
    _save = settings.get("vscode_save_completions_file")

    for key in data.keys():
        _data = data[key]
        if _data["scope"] == "":
            _sublime_scope = "all"
        elif _data["scope"] in _scopes_dict.keys():
            _sublime_scope = _scopes_dict[_data["scope"]]
        else:
            _sublime_scope = "text.plain"

        if not _key or _key == _data["scope"]:
            _key = _data["scope"]
        else:
            _key = ""
            _competion_dict = {}
            _dict_completions = []

        _competion_dict = {
            "trigger": _data["prefix"],
            "contents": "\n".join(_data["body"]),
            "description": _data["description"]
        }
        _dict_completions.append(_competion_dict)
        if _sublime_scope == "all":
            _tmp_dict = {
                "completions": _dict_completions
            }
        else:
            _tmp_dict = {
                "scope": _sublime_scope,
                "completions": _dict_completions
            }
        json_new_dict.update(
            {
                "%s" % _data["scope"] or "all": _tmp_dict
            }
        )

    if _save:
        for key, value in json_new_dict.items():
            user_path = os.path.join(
                *[
                    sublime.packages_path(),
                    "User",
                    "VscodeSnippetsParser",
                    "Completions",
                    key + settings.get(
                        "vscode_completions_file_extensions",
                        ".sublime-completions"
                    )
                ]
            )
            user_dir = os.path.dirname(user_path)

            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            with open(user_path, "w") as f:
                f.write(
                    json.dumps(
                        value,
                        sort_keys=True,
                        indent=4,
                        separators=(',', ': ')
                    )
                )


def parser_and_save_json_snippets(data):
    _scopes_dict = settings.get("vscode_scopes")
    _save = settings.get("vscode_save_snippets_file")

    for key in data.keys():
        _data = data[key]
        if _data["scope"] == "":
            _sublime_scope = "all"
        elif _data["scope"] in _scopes_dict.keys():
            _sublime_scope = _scopes_dict[_data["scope"]]
        else:
            _sublime_scope = "text.plain"

        if re.findall(RE_DESCRIPTION, _data["description"]):
            _description = "<![CDATA[{}]]>".format(_data["description"])
        else:
            _description = _data["description"]

        if _sublime_scope == "all":
            snippet_info = """<snippet>
    <content><![CDATA[{}]]></content>
    <tabTrigger>{}</tabTrigger>
    <description>{}</description>
</snippet>""".format(
                "\n".join(_data["body"]),
                _data["prefix"],
                _description
            )
        else:
            snippet_info = """<snippet>
    <content><![CDATA[{}]]></content>
    <tabTrigger>{}</tabTrigger>
    <scope>{}</scope>
    <description>{}</description>
</snippet>""".format(
                "\n".join(_data["body"]),
                _data["prefix"],
                _sublime_scope,
                _description
            )

        if _save:
            if _sublime_scope == "all":
                _scope = "all"
            else:
                _scope = _sublime_scope

            file_name = (
                _scope + "_" + key + settings.get(
                    "vscode_snippets_file_extensions",
                    ".sublime-snippets"
                ))
            user_path = os.path.join(
                *[
                    sublime.packages_path(),
                    "User",
                    "VscodeSnippetsParser",
                    "Snippets",
                    re.sub(RE_REPLACE, "_", file_name)
                ]
            )
            user_dir = os.path.dirname(user_path)

            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            with open(user_path, "w") as f:
                f.write(snippet_info)


def parser_file(edit, path=None):
    if not path:
        all_path = project.get_vscode_external_files()
    else:
        all_path = [path]

    _completion = settings.get("vscode_save_completions_file", False)
    _snippet = settings.get("vscode_save_snippets_file", False)

    for path in all_path:
        filter_file(edit, path)
        json_data = load_filter_json(edit)
        if _completion:
            parser_and_save_json_completions(json_data)
        if _snippet:
            parser_and_save_json_snippets(json_data)
