"""Main script to update avpr files."""

import pathlib
import glob
import subprocess

import toml
import json


__here__ = pathlib.Path(__file__).parent


from git import setup
setup()


for path in (__here__.parent / "daemons").glob("*.avpr"):
    # read from existing avpr
    kind = path.stem
    print((kind + "-"*100)[:99])
    with open(path, "r") as f:
        avpr = json.load(f)
    sources = avpr.get("installation", {})
    if not sources:
        # TODO: raise a gitlab issue noting that this daemon doesn't provide sources
        continue
    # install
    if "PyPI" in avpr["installation"]:
        from pypi import install
        try:
            version = install(sources["PyPI"], kind)
        except Exception as e:
            print(e)
            continue
    # check avpr
    new_avpr = json.loads(subprocess.check_output([f"yaqd-{kind}", "--protocol"]).decode())
    if avpr == new_avpr:
        print("EQUALITY", kind)
    else:
        from git import open_mr
        open_mr(kind, version)
