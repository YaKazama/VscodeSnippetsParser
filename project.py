import os
import sublime
import glob
from . import settings


def get_all_files(path):
    files = []
    if not os.path.isdir(path):
        raise
    for x in os.listdir(path):
        f = os.path.join(path, x)
        if os.path.isdir(f):
            files.extend(get_all_files(f))
        else:
            files.append(f)
    return files


def get_vscode_external_files():
    vs_load_files = settings.get("vscode_external_files", [])
    vs_extensions = settings.get("vscode_extensions")
    project_folders = sublime.active_window().folders()
    external_files = []
    tmp_files = []

    if vs_load_files == [] or vs_load_files == "":
        vs_load_files = project_folders

        for _dir in vs_load_files:
            tmp_files.extend(get_all_files(_dir))

        for _f in tmp_files:
            for _extension in vs_extensions:
                if _f.endswith(_extension):
                    external_files.append(_f)
    elif isinstance(vs_load_files, str):
        project_folders = os.path.join(
            os.path.dirname(sublime.packages_path()),
            vs_load_files
        )
        if not os.path.exists(project_folders):
            print("warnning: {} not exists!".format(project_folders))
            return external_files
        vs_load_files = [project_folders]

        for _dir in vs_load_files:
            tmp_files.extend(get_all_files(_dir))

        for _f in tmp_files:
            for _extension in vs_extensions:
                if _f.endswith(_extension):
                    external_files.append(_f)
    else:
        for _folder in project_folders:
            for _f in vs_load_files:
                if not _f.startswith("/"):
                    _f = "/".join([_folder, _f])
                if os.path.isdir(_f):
                    tmp_files.extend(get_all_files(_f))

                    for _f in tmp_files:
                        for _extension in vs_extensions:
                            if _f.endswith(_extension):
                                external_files.append(_f)
                else:
                    external_files.extend(glob.glob(_f))

    return external_files
