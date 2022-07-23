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

#region Init
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
#endregion
#region Templates
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
#endregion
#region Stylesheets
apprentice_css = """/*
This stylesheet is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This stylesheet is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this stylesheet. If not, see <https://www.gnu.org/licenses/>. 
*/

body {
    background-color: #262626;
    color: #BCBCBC;
    font-family: monospace; /* delete/comment this line if you use another
                            font. i wrote this because it's hard to read a
                            text with default browser font, and monospace
                            fonts are my favorites. */
}

blockquote {
    border-left: 2px solid #444444;
    padding-left: 10px;
}

table {
    border: 1px solid #444444;
    border-collapse: collapse;
}

th, td, table caption {
    border: 1px solid #444444;
    padding: 5px;
}

tr:nth-child(even) {
    background-color: #1C1C1C;
}

th {
    background-color: #303030;
}

a:link {
    color: #5f87af;
}

a:visited {
    color: #8787af;
}

a:active {
    color: #af5f5f;
}

mark {
    background-color: #FFFFAF;
}

iframe {
    border: 1px solid #444444;
}

fieldset {
    border: 1px solid #444444;
}

input, textarea, button {
    background-color: #303030;
    border: 1px solid #444444;
    color: #BCBCBC;
}

button[disabled], input[disabled] {
    background-color: #262626;
    border: 1px solid #303030;
    color: #585858;
}

input[type="file"]::file-selector-button, input[type="file"]::-webkit-file-upload-button {
    background-color: #303030;
    border: none;
    border-right: 1px solid #444444;
    color: #BCBCBC;
}

select {
    background-color: #303030;
    border: 1px solid #444444;
    color: #BCBCBC;
}

input[type="range"] {
    -webkit-appearance: none;
}

input[type="range"]:focus {
    outline: none;
}

input[type=range]::-webkit-slider-runnable-track {
    height: 5px;
    cursor: pointer;
    background: #5F87AF;
    border-radius: 3px;
    border: 1px solid #303030;
    margin-top: 5px;
    margin-bottom: 5px;
}

input[type=range]::-webkit-slider-thumb {
    border: 1px solid #303030;
    height: 15px;
    width: 15px;
    border-radius: 3px;
    background: #BCBCBC;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -6px;
}

input[type=range]:focus::-webkit-slider-runnable-track {
    background: #5F87AF;
}

input[type="range"]::-moz-range-track {
    cursor: pointer;
    background: #5F87AF;
    border-radius: 3px;
    border: 1px solid #303030;
}

input[type="range"]::-moz-range-thumb {
    border: 1px solid #303030;
    border-radius: 3px;
    background: #BCBCBC;
    cursor: pointer;
}"""

prism_apprentice_css = """/**
* Apprentice Theme Originally by Jeet Sukumaran
* https://romainl.github.io/Apprentice/
*
* Ported for PrismJS by Cinar Yilmaz
* Based on Nord for PrismJS (except colors)
* https://github.com/PrismJS/prism-themes/blob/master/themes/prism-nord.css
*/

code[class*="language-"],
pre[class*="language-"] {
    color: #BCBCBC;
    background: none;
    font-family: monospace;
    text-align: left;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;
    word-wrap: normal;
    line-height: 1.5;
    -moz-tab-size: 4;
    -o-tab-size: 4;
    tab-size: 4;
    -webkit-hyphens: none;
    -moz-hyphens: none;
    -ms-hyphens: none;
    hyphens: none;
    padding: 0;
}

/* Code blocks */
pre[class*="language-"] {
    padding: 1em;
    margin: .5em 0;
    overflow: auto;
    border-radius: 0.3em;
    border: #111111 1px solid;
}

:not(pre) > code[class*="language-"],
pre[class*="language-"] {
    background: #1C1C1C;
}

/* Inline code */
:not(pre) > code[class*="language-"] {
    padding: .1em;
    border-radius: .3em;
    white-space: normal;
}

.token.comment,
.token.prolog,
.token.doctype,
.token.cdata {
    color: #6C6C6C;
}

.token.punctuation {
    color: #BCBCBC;
}

.namespace {
    opacity: .7;
}

.token.property,
.token.tag,
.token.constant,
.token.symbol,
.token.deleted {
    color: #8FAFD7;
}

.token.number {
    color: #FFFFAF;
}

.token.boolean {
    color: #8FAFD7;
}

.token.selector,
.token.attr-name,
.token.string,
.token.char,
.token.builtin,
.token.inserted {
    color: #87AF87;
}

.token.entity,
.token.url,
.language-css .token.string,
.style .token.string,
.token.variable {
    color: #FFFFAF;
}


.token.operator {
    color: #5FAFAF;
}

.token.atrule,
.token.attr-value,
.token.function,
.token.class-name {
    color: #5FAFAF;
}

.token.keyword {
    color: #8787AF;
}

.token.regex,
.token.important {
    color: #FFFFAF;
}

.token.important,
.token.bold {
    font-weight: bold;
}

.token.italic {
    font-style: italic;
}

.token.entity {
    cursor: help;
}"""
#endregion
#region Languages
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
#endregion
#region Application
app = flask.Flask(__name__)
app.url_map.strict_slashes = False

config = configparser.ConfigParser()
config.read(sys.argv[1])

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])
#endregion
#region Routes
@app.route('/')
def index():
    repos = []
    result = template
    out = ""
    for repo in config.sections():
        if repo.startswith("repo-"):
            repos.append(repo[5:])
    for repo in repos:
        out += "<h3><a href=\"/{}\">{}</a></h3>".format(repo, config["repo-" + repo]['name'])
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
        tree += "<h3><a href=\"/{}{}\">..</a></h3>".format(repo, path + "/..")
    else:
        tree += "<h3><a href=\"/\">Main Page</a></h3>"
    for f in files:
        isdir = f.find("div", {"class": "flex-shrink-0"}).find("svg").get("aria-label") == "Directory"
        filename = f.find("div", {"class": "col-md-2"}).find("span").find("a").text
        if isdir:
            tree += "<h3><i class=\"fa-solid fa-folder\" style=\"color: #FFCC4D;\"></i> <a href=\"/{}{}\">{}</a></h3>".format(repo, f"{path}/{filename}", filename)
        else:
            tree += "<h3><i class=\"fa-solid fa-file\"></i> <a href=\"/{}{}\">{}</a></h3>".format(repo, f"{path}/{filename}", filename)
    result = result.format(config["repo-" + repo]['name'], path, tree)
    return result

def show_file(repo, path):
    result = ftemplate
    req = requests.get(config["repo-" + repo]["rawurl"] + "/" + path)
    if req.status_code == 404:
        return None
    parents = []
    pathpar = pathlib.Path(path).parent
    while pathpar.name != "":
        parents.append(pathpar)
        pathpar = pathlib.Path(pathpar).parent
    parents.reverse()
    pathpar = f"<a href=\"/{repo}\">{config['repo-' + repo]['name']}</a>/"
    for parent in parents:
        pathpar += f"<a href=\"/{repo}{str(parent)}\">{parent.name}</a>/"
    pathfile = pathlib.Path(path).name
    if pathlib.Path(path).name in ["Makefile", "makefile"]:
        lang = "makefile"
    else:
        lang = languages.get(pathlib.Path(path).suffix, "plaintext")
    result = result.format(config["repo-" + repo]['name'], path, f"<h2>{pathpar}{pathfile}</h2><pre class=\"linkable-line-numbers\" id=\"code\"><code class=\"language-{lang} line-numbers\">{html.escape(req.text)}</code></pre>")
    return result

@app.route('/<repo>/<path:path>')
def dir(repo, path):
    f = show_file(repo, "/" + path)
    if f is None:
        return get_dir_list(repo, "/" + path)
    else:
        return f

@app.route('/<repo>')
def dirroot(repo):
    return get_dir_list(repo, "")

@app.route('/style/apprentice.css')
def apprentice():
    response = app.response_class(
        response=apprentice_css,
        status=200,
        mimetype='text/css'
    )
    return response

@app.route('/style/prism-apprentice.css')
def prism_apprentice():
    response = app.response_class(
        response=prism_apprentice_css,
        status=200,
        mimetype='text/css'
    )
    return response
#endregion

app.run(debug=True, port=int(config["server"]["port"]))
