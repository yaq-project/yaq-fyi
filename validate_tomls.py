#! /usr/bin/env python3
import toml
import pathlib
import sys

here = pathlib.Path()

tomls = here.glob("**/*.toml")

invalid_count = 0
for t in tomls:
    if list(t.parents)[-2] == pathlib.Path(".git"):
        continue
    print(t)
    try:
        toml.load(t)
    except ValueError as e:
        invalid_count += 1
        print(e)
    else:
        print("Okay")

sys.exit(invalid_count)

