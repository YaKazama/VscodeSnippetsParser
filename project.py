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
    vs_extension = settings.get("vscode_extension")
    project_folders = sublime.active_window().folders()
    external_files = []
    tmp_files = []

    if vs_load_files == "auto":
        vs_load_files = project_folders

        for _dir in vs_load_files:
            tmp_files.extend(get_all_files(_dir))

        for _f in tmp_files:
            for _extension in vs_extension:
                if _f.endswith(_extension):
                    external_files.append(_f)
    elif vs_load_files == []:
        for _folder in project_folders:
            for _f in vs_load_files:
                if not _f.startswith("/"):
                    _f = "/".join([_folder, _f])
                if os.path.isdir(_f):
                    print("Directory: ", _f)
                    raise ValueError("Can't be a directory")
                external_files.extend(glob.glob(_f))
    else:
        for file_path in vs_load_files:
            external_files.extend(glob.glob(file_path))
    return external_files
