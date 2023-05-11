"""Construct a graph of trait and daemon relationships."""


import os
import pathlib
import copy
import collections
import toml
import json
from dataclasses import dataclass

from yaq_traits.__traits__ import traits
import markdown


__here__ = pathlib.Path(__file__).resolve().parent


# posts -------------------------------------------------------------------------------------------


extension_configs = {"toc": {"permalink": " ¶"}}
md = markdown.Markdown(
    extensions=["meta", "toc", "extra"], extension_configs=extension_configs
)

@dataclass
class Post:
    id: str
    title: str
    content: str
    date: str
    tags: list

posts = []
tags = []
for post in (__here__ / "posts").iterdir():
    with open(post, "r") as f:
        s = f.read()
        content = md.convert(s)
        kwargs = {
            "id": md.Meta["id"][0],
            "title": md.Meta["title"][0],
            "content": content,
            "date": md.Meta["date"][0],
            "tags": md.Meta.get("tags", list()),
        }
        posts.append(Post(**kwargs))
        tags += kwargs["tags"]

posts.sort(key=lambda y: y.date)

tags = list(set(tags))
tags.sort()


# trait -------------------------------------------------------------------------------------------


class Trait(object):
    def __init__(self, **kwargs):
        self.trait = kwargs["trait"]
        self.name = self.trait
        self.doc = kwargs["doc"]
        self.requires = kwargs["requires"]
        self.config = kwargs.get("config", dict())
        self.state = kwargs.get("state", dict())
        self.messages = kwargs.get("messages", dict())
        self.daemons = []
        self.types = kwargs.get("types", [])
        self.types = [ty for ty in self.types if ty["name"] != "ndarray"]
        self.posts = [post for post in posts if self.name in post.tags]

    def __repr__(self):
        return self.name

    def format_origin(self, origin):
        return f"from <a href='../{origin}'>{origin}</a>"


# initialize
for k in traits:
    t = Trait(**traits[k])
    traits[k] = t

# sort
traits = collections.OrderedDict(sorted(traits.items()))


# daemon ------------------------------------------------------------------------------------------


class Daemon(object):
    def __init__(self, **kwargs):
        self.protocol = kwargs["protocol"]
        self.name = self.protocol
        self.doc = kwargs["doc"]
        self.links = kwargs.get("links", dict())
        self.installation = kwargs.get("installation", dict())
        self.traits = kwargs["traits"]
        self.config = kwargs.get("config", dict())
        self.state = kwargs.get("state", dict())
        self.messages = kwargs.get("messages", dict())
        self.hardwares = kwargs.get("hardware", [])
        self.types = kwargs.get("types", [])
        self.types = [ty for ty in self.types if ty["name"] != "ndarray"]
        self.example_configs = self.links.get("example-configs", None)
        self.posts = [post for post in posts if self.name in post.tags]

    def __repr__(self):
        return self.name

    def format_origin(self, origin):
        return f"from <a href='../../traits/{origin}'>{origin}</a>"


daemons = {}

# initialize
for name in os.listdir(__here__ / "daemons"):
    with open(__here__ / "daemons" / name, "r") as f:
        dic = json.load(f)
    d = Daemon(**dic)
    daemons[d.name] = d

# sort
daemons = collections.OrderedDict(sorted(daemons.items()))

# back-populate
for d in daemons.values():
    for t in d.traits:
        traits[t].daemons.append(d.name)


# hardware ----------------------------------------------------------------------------------------


class Hardware(object):
    def __init__(self, **kwargs):
        self.make = kwargs["make"]
        self.model = kwargs["model"]
        self.doc = kwargs.get("doc", "")
        self.links = kwargs.get("links", dict())
        self.daemons = kwargs["daemons"]

    def __repr__(self):
        return ":".join([self.make, self.model])


hardwares = {}

# initialize
dic = toml.load(__here__ / "known-hardware.toml")
for make_name, make in dic.items():
    for model_name, model in make.items():
        if model_name in ["doc", "links"]:
            continue
        identifier = ":".join([make_name, model_name])
        daemons_ = []
        for d in daemons.values():
            if identifier in d.hardwares:
                daemons_.append(d.protocol)
        h = Hardware(make=make_name, model=model_name, **model, daemons=daemons_)
        hardwares[identifier] = h


# sort
def key(item):
    k, v = item
    return "/".join([v.make, v.model])
hardwares = collections.OrderedDict(sorted(hardwares.items(), key=key))
