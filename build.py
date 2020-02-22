#!/usr/bin/env python3

import os
import pathlib
import toml
from jinja2 import Environment, FileSystemLoader


__here__ = pathlib.Path(__file__).resolve().parent

env = Environment(loader = FileSystemLoader(str(__here__ / "templates")))

if not os.path.isdir(__here__ / "public"):
    os.mkdir(__here__ / "public")

# css ---------------------------------------------------------------------------------------------

p = __here__ / "public" / "style.css"
template = env.get_template('style.css')
with open(p, 'w') as fh:
    fh.write(template.render())

# landing page ------------------------------------------------------------------------------------

p = __here__ / "public" / "index.html"
template = env.get_template('index.html')
with open(p, 'w') as fh:
    fh.write(template.render())

# protocol ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "protocol"):
    os.mkdir(__here__ / "public" / "protocol")

p = __here__ / "public" / "protocol" / "index.html"
template = env.get_template('protocol.html')
with open(p, 'w') as fh:
    fh.write(template.render())

# introduction ------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "introduction"):
    os.mkdir(__here__ / "public" / "introduction")

p = __here__ / "public" / "introduction" / "index.html"
template = env.get_template('introduction.html')
with open(p, 'w') as fh:
    fh.write(template.render())

# licensing ---------------------------------------------------------------------------------------

# glossary ----------------------------------------------------------------------------------------

# traits ------------------------------------------------------------------------------------------

# families ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "families"):
    os.mkdir(__here__ / "public" / "families")

daemons = []
for name in os.listdir(__here__ / "daemons"):
    daemons.append(toml.load(__here__ / "daemons" / name))

# families landing page
p = __here__ / "public" / "families" / "index.html"
template = env.get_template('families.html')
with open(p, 'w') as fh:
    fh.write(template.render(daemons=daemons))

# daemons -----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "daemons"):
    os.mkdir(__here__ / "public" / "daemons")

daemons = []
for name in os.listdir(__here__ / "daemons"):
    daemons.append(toml.load(__here__ / "daemons" / name))

# main daemon page
p = __here__ / "public" / "daemons" / "index.html"
template = env.get_template('daemons.html')
with open(p, 'w') as fh:
    fh.write(template.render(daemons=daemons))

# page for each daemon
for daemon in daemons:
    p = __here__ / "public" / "daemons" / daemon["name"] / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    template = env.get_template('daemon.html')
    with open(p, 'w') as fh:
        fh.write(template.render(daemon=daemon))
