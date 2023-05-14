#!/usr/bin/env python3

import os
import pathlib
import toml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from graph import traits, daemons, hardwares, posts, tags
from helpers import helpers


__here__ = pathlib.Path(__file__).resolve().parent

if not os.path.isdir(__here__ / "public"):
    os.mkdir(__here__ / "public")

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

env = Environment(loader=FileSystemLoader(str(__here__ / "templates")))
env.globals["date"] = date
env.globals["helpers"] = helpers


# landing page ------------------------------------------------------------------------------------

p = __here__ / "public" / "index.html"
template = env.get_template("index.html")
with open(p, "w") as fh:
    fh.write(template.render(title="yaq"))

# pages without arguments -------------------------------------------------------------------------

names = ["introduction", "licensing", "contact", "alternatives"]

for name in names:

    if not os.path.isdir(__here__ / "public" / name):
        os.mkdir(__here__ / "public" / name)

    p = __here__ / "public" / name / "index.html"
    template = env.get_template(name + ".html")
    with open(p, "w") as fh:
        fh.write(template.render(title=name))

# packages ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "packages"):
    os.mkdir(__here__ / "public" / "packages")

p = __here__ / "public" / "packages" / "index.html"
template = env.get_template("packages.html")
with open(p, "w") as fh:
    pkgs = toml.load(__here__ / "known-packages.toml")
    fh.write(template.render(title="packages", packages=pkgs))

# blog posts --------------------------------------------------------------------------------------


if not os.path.isdir(__here__ / "public" / "blog"):
    os.mkdir(__here__ / "public" / "blog")

template = env.get_template("post-index.html")
with open(__here__ / "public" / "blog" / "index.html", "w") as f:
    f.write(template.render(posts=posts))

template = env.get_template("post-tags.html")
if not os.path.isdir(__here__ / "public" / "blog" / "tags"):
    os.mkdir(__here__ / "public" / "blog" / "tags")
with open(__here__ / "public" / "blog" / "tags" / "index.html", "w") as f:
    f.write(template.render(posts=posts, tags=tags, title="tags", date=date))

template = env.get_template("post.html")
for post in posts:
    (__here__ / "public" / "blog" / post.id).mkdir(exist_ok=True)
    with open(__here__ / "public" / "blog" / post.id / "index.html", "w") as f:
        f.write(template.render(post=post, title=post.title, date=date))


# traits ------------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "traits"):
    os.mkdir(__here__ / "public" / "traits")

# traits landing page
p = __here__ / "public" / "traits" / "index.html"
template = env.get_template("traits.html")
with open(p, "w") as fh:
    fh.write(template.render(traits=traits.values(), title="traits", ))

# page for each trait
for trait in traits.values():
    # ensure directory exists
    p = __here__ / "public" / "traits" / trait.name / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("trait.html")
    with open(p, "w") as fh:
        fh.write(template.render(trait=trait, title=trait.name, posts=posts, ))

# daemons -----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "daemons"):
    os.mkdir(__here__ / "public" / "daemons")

# daemon landing page
p = __here__ / "public" / "daemons" / "index.html"
template = env.get_template("daemons.html")
with open(p, "w") as fh:
    fh.write(template.render(daemons=daemons.values(), title="daemons", ))

# page for each daemon
for daemon in daemons.values():
    # ensure directory exists
    p = __here__ / "public" / "daemons" / daemon.name / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("daemon.html")
    with open(p, "w") as fh:
        fh.write(template.render(daemon=daemon, title=daemon.name, posts=posts, ))

# hardware ----------------------------------------------------------------------------------------

if not os.path.isdir(__here__ / "public" / "hardware"):
    os.mkdir(__here__ / "public" / "hardware")

# hardwares landing page
p = __here__ / "public" / "hardware" / "index.html"
template = env.get_template("hardwares.html")
with open(p, "w") as fh:
    fh.write(template.render(hardwares=hardwares.values(), title="hardware", ))

# page for each make
for hardware in hardwares.values():
    # ensure directory exists
    p = __here__ / "public" / "hardware" / hardware.make / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("make.html")
    d = toml.load(__here__ / "known-hardware.toml")[hardware.make]
    make = hardware.make
    doc = d.get("doc", "")
    links = d.get("links", {})
    with open(p, "w") as fh:
        fh.write(template.render(make=make, doc=doc, links=links, title=make, hardwares=hardwares.values()))

# page for each model
for hardware in hardwares.values():
    # ensure directory exists
    p = __here__ / "public" / "hardware" / hardware.make / hardware.model / "index.html"
    if not os.path.isdir(p.parent):
        os.mkdir(p.parent)
    # run template
    template = env.get_template("model.html")
    with open(p, "w") as fh:
        fh.write(template.render(hardware=hardware, title=hardware.model))

# css ---------------------------------------------------------------------------------------------

for d, _, _ in os.walk(__here__ / "public", topdown=False):
    template = env.get_template("style.css")
    with open(os.path.join(d, "style.css"), "w") as fh:
        fh.write(template.render())
