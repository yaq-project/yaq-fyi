# yaq-fyi

Main website for yaq documentation.

This repository attempts to document completely each and every trait, family, and daemon in the yaq project.
Each of these is documented in a simple TOML file, the contents of which are detailed below.

Jinja2 is used to generate a static website using the information in the simple TOML files.
The website that is rendered from this information is hosted at https://yaq.fyi

## daemons

```toml
name = ""  # required
description = ""  # required
repository-url = ""  # optional
bugtracker-url = ""  # optional
family = ""  # required (can be base)
traits = []  # required (can be empty)

[install]
language = "python"  # required
# other keys optional, language dependent
```

## families

## traits
