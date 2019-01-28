# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import sublime

_version = sublime.version()
scratch_view = None


if int(_version) < 3000:
    raise ValueError("The Version must be greater than or equal 3000.")


def get_settings():
    _settings_file = "VscodeSnippetsParser.sublime-settings"
    settings = sublime.load_settings(_settings_file)
    return settings


def get(key, default=None):
    settings = get_settings()
    if settings:
        return settings.get(key) if settings.get(key) else default
    else:
        return default


def get_output_panel(name='VscodeSnippetsParser', is_scratch=True):
    global scratch_view
    if not scratch_view:
        scratch_view = sublime.active_window().create_output_panel(name)
        if is_scratch:
            scratch_view.set_scratch(True)
    return scratch_view
