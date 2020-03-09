#!/usr/bin/env python3

import os
import pathlib
import toml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

__here__ = pathlib.Path(__file__).resolve().parent

env = Environment(loader = FileSystemLoader(str(__here__ / "templates")))

if not os.path.isdir(__here__ / "public"):
    os.mkdir(__here__ / "public")

date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# landing page ------------------------------------------------------------------------------------

p = __here__ / "public" / "index.html"
template = env.get_template('index.html')
with open(p, 'w') as fh:
    fh.write(template.render(title="yaq", date=date))

# pages without arguments -------------------------------------------------------------------------

names = ["protocol", "introduction", "licensing", "glossary"]

for name in names:

    if not os.path.isdir(__here__ / "public" / name):
        os.mkdir(__here__ / "public" / name)

    p = __here__ / "public" / name / "index.html"
    template = env.get_template(name + '.html')
    with open(p, 'w') as fh:
        fh.write(template.render(title=name, date=date))

# traits ------------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "traits"):
    os.mkdir(__here__ / "public" / "traits")

traits = {}
for name in os.listdir(__here__ / "traits"):
    t = toml.load(__here__ / "traits" / name)
    traits[t["name"]] = t

# traits landing page
p = __here__ / "public" / "traits" / "index.html"
template = env.get_template('traits.html')
with open(p, 'w') as fh:
    fh.write(template.render(traits=traits.values(), title="traits", date=date))

# page for each trait
for trait in traits.values():
    # ensure directory exists
    p = __here__ / "public" / "traits" / trait["name"] / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # generate requires list
    requires = []
    todo = trait["requires"][:]  # copy
    while todo:
        now = todo.pop(0)
        for new in traits[now.split("→")[-1]]["requires"]:
            todo.append(now + "→" + new)
        requires.append(now)
    # generate config dict
    config = {}
    if "config" in trait.keys():
        config.update(trait["config"])
    for r in requires:
        t = r.split("→")[-1]
        if not "config" in traits[t].keys():
            continue
        config.update(traits[t]["config"])
        for key in traits[t]["config"].keys():
            config[key]["origin"] = r
    # generate state dict
    state = {}
    if "state" in trait.keys():
        state.update(trait["state"])
    for r in requires:
        t = r.split("→")[-1]
        if not "state" in traits[t].keys():
            continue
        state.update(traits[t]["state"])
        for key in traits[t]["state"].keys():
            state[key]["origin"] = r
    # generate method dict
    method = {}
    if "method" in trait.keys():
        method.update(trait["method"])
    for r in requires:
        t = r.split("→")[-1]
        if not "method" in traits[t].keys():
            continue
        method.update(traits[t]["method"])
        for key in traits[t]["method"].keys():
            method[key]["origin"] = r
    template = env.get_template('trait.html')
    with open(p, 'w') as fh:
        fh.write(template.render(trait=trait, config=config, state=state, method=method,
                                 title=trait["name"], date=date))

# families ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "families"):
    os.mkdir(__here__ / "public" / "families")

families = []
for name in os.listdir(__here__ / "families"):
    families.append(toml.load(__here__ / "families" / name))

# families landing page
p = __here__ / "public" / "families" / "index.html"
template = env.get_template('families.html')
with open(p, 'w') as fh:
    fh.write(template.render(families=families, title="families", date=date))

# page for each family
for family in families:
    p = __here__ / "public" / "families" / family["name"] / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    template = env.get_template('family.html')
    with open(p, 'w') as fh:
        fh.write(template.render(family=family, title=family["name"], date=date))

# daemons -----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "daemons"):
    os.mkdir(__here__ / "public" / "daemons")

daemons = []
for name in os.listdir(__here__ / "daemons"):
    daemons.append(toml.load(__here__ / "daemons" / name))

# daemon landing page
p = __here__ / "public" / "daemons" / "index.html"
template = env.get_template('daemons.html')
with open(p, 'w') as fh:
    fh.write(template.render(daemons=daemons, title="daemons", date=date))

# page for each daemon
for daemon in daemons:
    p = __here__ / "public" / "daemons" / daemon["name"] / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    template = env.get_template('daemon.html')
    with open(p, 'w') as fh:
        fh.write(template.render(daemon=daemon, title=daemon["name"], date=date))

# css ---------------------------------------------------------------------------------------------

for d, _, _ in os.walk(__here__ / "public", topdown=False):
    template = env.get_template('style.css')
    with open(os.path.join(d, "style.css"), 'w') as fh:
        fh.write(template.render())
