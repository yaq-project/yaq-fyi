#!/usr/bin/env python3

import os
import pathlib
import toml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from graph import traits, daemons, hardwares

__here__ = pathlib.Path(__file__).resolve().parent

env = Environment(loader=FileSystemLoader(str(__here__ / "templates")))

if not os.path.isdir(__here__ / "public"):
    os.mkdir(__here__ / "public")

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# landing page ------------------------------------------------------------------------------------

p = __here__ / "public" / "index.html"
template = env.get_template("index.html")
with open(p, "w") as fh:
    fh.write(template.render(title="yaq", date=date))

# pages without arguments -------------------------------------------------------------------------

names = ["introduction", "licensing", "glossary", "contact"]

for name in names:

    if not os.path.isdir(__here__ / "public" / name):
        os.mkdir(__here__ / "public" / name)

    p = __here__ / "public" / name / "index.html"
    template = env.get_template(name + ".html")
    with open(p, "w") as fh:
        fh.write(template.render(title=name, date=date))

# traits ------------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "traits"):
    os.mkdir(__here__ / "public" / "traits")

# traits landing page
p = __here__ / "public" / "traits" / "index.html"
template = env.get_template("traits.html")
with open(p, "w") as fh:
    fh.write(template.render(traits=traits.values(), title="traits", date=date))

# page for each trait
for trait in traits.values():
    # ensure directory exists
    p = __here__ / "public" / "traits" / trait.name / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("trait.html")
    with open(p, "w") as fh:
        fh.write(template.render(trait=trait, title=trait.name, date=date))

# daemons -----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "daemons"):
    os.mkdir(__here__ / "public" / "daemons")

# daemon landing page
p = __here__ / "public" / "daemons" / "index.html"
template = env.get_template("daemons.html")
with open(p, "w") as fh:
    fh.write(template.render(daemons=daemons.values(), title="daemons", date=date))

# page for each daemon
for daemon in daemons.values():
    # ensure directory exists
    p = __here__ / "public" / "daemons" / daemon.name / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("daemon.html")
    with open(p, "w") as fh:
        fh.write(template.render(daemon=daemon, title=daemon.name, date=date))

# hardware ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "hardware"):
    os.mkdir(__here__ / "public" / "hardware")

# hardwares landing page
p = __here__ / "public" / "hardware" / "index.html"
template = env.get_template("hardwares.html")
with open(p, "w") as fh:
    fh.write(template.render(hardwares=hardwares.values(), title="hardware", date=date))

# page for each hardware
for hardware in hardwares.values():
    # ensure directory exists
    p = __here__ / "public" / "hardware" / hardware.model / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("hardware.html")
    with open(p, "w") as fh:
        fh.write(template.render(hardware=hardware, title=hardware.model, date=date))

# css ---------------------------------------------------------------------------------------------

for d, _, _ in os.walk(__here__ / "public", topdown=False):
    template = env.get_template("style.css")
    with open(os.path.join(d, "style.css"), "w") as fh:
        fh.write(template.render())
