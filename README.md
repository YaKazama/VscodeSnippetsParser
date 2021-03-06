# VscodeSnippetsParser

* 用于将 `VS Code` 的代码片段（`Snippets`）文件转换为Sublime Text 3 (3188) 支持的
  文件：`.sublime-completions` 或 `.sublime-snippet`。
* 代码片段中的环境变量，没有做处理。
* 生成后的文件存放于 `Packages/User/VscodeSnippetsParser` 目录下。

## 参数说明

```
# 是否在启动软件时，自动运行。
"vscode_run_at_startup": false,

# 需要解析的文件列表，可以包括：“*”。
# 示例：
#  []
#  ["path/to/file/"]
#  ["path/to/python.code-snippets"]
#  ["path/to/*.code-snippets"]
# []：在当前目录中查找。
# 相对路径：会在已打开的所有目录（folders）下查找。
# 绝对路径：会直接查找指定文件。
# 指定目录：会遍历目录下的所有文件，找出由：vscode_extensions 中指定后缀的文件。
# 任意字符串：遍历`os.path.join(os.path.dirname(sublime.packages_path()), settings.get("vscode_external_files", "VscodeSnippets"))`目录。目录不存在则新建空目录。
"vscode_external_files": "VscodeSnippets",

# 允许解析的文件后缀名称。必须是 JSON 格式，否则会出现不可明状的错误。
"vscode_extensions": [
    ".code-snippets", ".json"
],

# 换行符。
"vscode_line_break": "\n",

# 是否使用过滤文件。目前此参数必需为：true。文件名由参数：vscode_filter_file 定义。
# true，会将过滤后的结果，写处临时文件中备用。
# false，返回一个包含所有过滤结果的列表。
"vscode_save_filter_to_file": true,

# 过滤结果写入的文件名。
"vscode_filter_file": "vscode_filter_file.json",

# 是否保存为：completions 文件。默认：true。
"vscode_save_completions_file": true,

# completions 文件后缀。
"vscode_completions_file_extensions": ".sublime-completions",

# 是否保存为：snippet 文件。默认：false。
"vscode_save_snippets_file": false,

# snippet 文件后缀。
"vscode_snippets_file_extensions": ".sublime-snippet",

# 是否在转换后的文件中写入 description 内容。默认：false。
"vscode_display_description": false,

# scope 转换字典。格式："<vscode_scope>": "<sublime_scope>"。
"vscode_scopes": {
    "python": "source.python",
    "restructuredtext": "text.restructuredtext",
    "shellscript": "source.shell.bash"
}
```

## 快捷键

```
{
    "keys": ["shift+alt+f"],
    "command": "vscode_snippets_parser",
    "args": {"is_run": true}
}
```

# 安装

```
cd /opt/sublime_text/Data/Packages/
git clone https://github.com/YaKazama/VscodeSnippetsParser.git
```
