# standard libraries
import os
import subprocess
import itertools
import json
import pathlib

# 3rd-party libraries
from flask import Flask
from flask import render_template
from flask import request
import jinja2

# 1st-party libraries
from blastradius.handlers.dot import DotGraph, Format, DotNode
from blastradius.util import which
from blastradius.graph import Node, Edge, Counter, Graph

app = Flask(__name__)

@app.route('/')
def index():
    # we need terraform, graphviz, and an init-ed terraform project.
    if not which('dot') and not which('dot.exe'):
        return render_template('error.html')
    else:
        return render_template('index.html')

@app.route('/graph.svg')
def graph_svg():
    Graph.reset_counters()
    dot = DotGraph('', file_contents=pathlib.Path(app.config['dotfile']).read_text())

    module_depth = request.args.get('module_depth', default=app.config['module_depth'], type=int)
    refocus      = request.args.get('refocus', default=None, type=str)

    if module_depth is not None and module_depth >= 0:
        dot.set_module_depth(module_depth)

    if refocus is not None:
        node = dot.get_node_by_name(refocus)
        if node:
            dot.center(node)

    return dot.svg()


@app.route('/graph.json')
def graph_json():
    Graph.reset_counters()
    dot = DotGraph('', file_contents=pathlib.Path(app.config['dotfile']).read_text())
    module_depth = request.args.get('module_depth', default=app.config['module_depth'], type=int)
    refocus      = request.args.get('refocus', default=None, type=str)
    if module_depth is not None and module_depth >= 0:
        dot.set_module_depth(module_depth) 

    for node in dot.nodes:
        node.definition = ''

    if refocus is not None:
        node = dot.get_node_by_name(refocus)
        if node:
            dot.center(node)

    return dot.json()
