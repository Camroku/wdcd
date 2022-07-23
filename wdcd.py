#!/bin/env python3

# Toryus is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# Toryus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with Toryus. If not, see
# <https://www.gnu.org/licenses/>. 

import sys
import configparser
import flask
import requests
import bs4
import html
import pathlib

if not len(sys.argv) == 2:
    print("Usage: {} <config file>".format(sys.argv[0]))
    sys.exit(1)

template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{}{} - wdcd</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/style/apprentice.css">
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
<style>
i.fa-solid {{
    font-family: 'FontAwesome', sans-serif;
    font-style: normal;
}}
</style>
</head>
<body>
{}
</body>
</html>
"""

ftemplate = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{}{} - wdcd</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/style/apprentice.css">
<link href="/style/prism-apprentice.css" rel="stylesheet">
<link href="https://prismjs.com/plugins/line-numbers/prism-line-numbers.css" rel="stylesheet">
<link rel="stylesheet" href="https://prismjs.com/plugins/line-highlight/prism-line-highlight.css" data-noprefix="">
</head>
<body>
{}
<script src=\"https://prismjs.com/prism.js\"></script>
<script src=\"https://prismjs.com/plugins/line-numbers/prism-line-numbers.js\"></script>
<script src=\"https://prismjs.com/plugins/autoloader/prism-autoloader.js\"></script>
<script src=\"https://prismjs.com/plugins/line-highlight/prism-line-highlight.js\"></script>
</body>
</html>
"""

languages = { # by file extensions
    ".c": "c",
    ".h": "c",
    ".py": "py",
    ".pyw": "py",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".md": "md",
    ".ld": "ld",
    ".asm": "nasm",
    ".s": "nasm",
    ".mk": "makefile",
}

app = flask.Flask(__name__)
app.url_map.strict_slashes = False

config = configparser.ConfigParser()
config.read(sys.argv[1])

@app.route('/')
def index():
    repos = []
    result = template
    out = ""
    for repo in config.sections():
        if repo.startswith("repo-"):
            repos.append(repo[5:])
    for repo in repos:
        out += "<h3><a href=\"/{}/dir\">{}</a></h3>".format(repo, config["repo-" + repo]['name'])
    result = result.format("Repositories", "", out)
    return result

def get_dir_list(repo, path):
    result = template
    req = requests.get(config["repo-" + repo]["dirurl"] + "/" + path)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    files = soup.find("div", {"aria-labelledby": "files"})
    files = files.find_all("div", {"class": "py-2"})
    tree = ""
    if path != "":
        tree += "<h3><a href=\"/{}/dir{}\">..</a></h3>".format(repo, path + "/..")
    else:
        tree += "<h3><a href=\"/\">Main Page</a></h3>"
    for f in files:
        isdir = f.find("div", {"class": "flex-shrink-0"}).find("svg").get("aria-label") == "Directory"
        filename = f.find("div", {"class": "col-md-2"}).find("span").find("a").text
        if isdir:
            tree += "<h3><i class=\"fa-solid fa-folder\" style=\"color: #FFCC4D;\"></i> <a href=\"/{}/dir{}\">{}</a></h3>".format(repo, f"{path}/{filename}", filename)
        else:
            tree += "<h3><i class=\"fa-solid fa-file\"></i> <a href=\"/{}/file{}\">{}</a></h3>".format(repo, f"{path}/{filename}", filename)
    result = result.format(config["repo-" + repo]['name'], path, tree)
    return result

def show_file(repo, path):
    result = ftemplate
    req = requests.get(config["repo-" + repo]["rawurl"] + "/" + path)
    parents = []
    pathpar = pathlib.Path(path).parent
    while pathpar.name != "":
        parents.append(pathpar)
        pathpar = pathlib.Path(pathpar).parent
    parents.reverse()
    pathpar = f"<a href=\"/{repo}/dir\">{config['repo-' + repo]['name']}</a>/"
    for parent in parents:
        pathpar += f"<a href=\"/{repo}/dir{str(parent)}\">{parent.name}</a>/"
    pathfile = pathlib.Path(path).name
    if pathlib.Path(path).name in ["Makefile", "makefile"]:
        lang = "makefile"
    else:
        lang = languages.get(pathlib.Path(path).suffix, "plaintext")
    result = result.format(config["repo-" + repo]['name'], path, f"<h2>{pathpar}{pathfile}</h2><pre class=\"linkable-line-numbers\" id=\"code\"><code class=\"language-{lang} line-numbers\">{html.escape(req.text)}</code></pre>")
    return result

@app.route('/<repo>/dir/<path:path>')
def dir(repo, path):
    return get_dir_list(repo, "/" + path)

@app.route('/<repo>/dir')
def dirroot(repo):
    return get_dir_list(repo, "")

@app.route('/<repo>/file/<path:path>')
def file(repo, path):
    return show_file(repo, "/" + path)

@app.route('/style/<path:path>')
def style(path):
    return flask.send_from_directory('style', path)

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

app.run(debug=True, port=int(config["server"]["port"]))
