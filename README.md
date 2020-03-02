# yaq-fyi

Main website for yaq documentation.

This repository attempts to document completely each and every trait, family, and daemon in the yaq project.
Each of these is documented in a simple TOML file, the contents of which are detailed below.

Jinja2 is used to generate a static website using the information in the simple TOML files.
The website that is rendered from this information is hosted at https://yaq.fyi

## daemons

Daemon documentation goes in the `daemons` directory.
Look there for examples.
The following is a short overview of what kind of information is expected.
Note that only new or changed config, state, and methods should be documented here, properties from traits and family are implied.

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

[config]  # optional
NAME = "TYPE"

[state]  # optional
NAME = "TYPE"

[method]  # optional

  [method.NAME]
  args.NAME = "TYPE"  # optional
  returns = "TYPE"  # optional
  description = ""  # required
```

## families

Families documentation goes in the `families` directory.
Look there for examples.
The following is a short overview of what kind of information is expected.
Families are very simple.

```toml
name = ""  # required
description = ""  # required
parent = ""  # required (can be base)
traits = []  # required (cannot be empty)
```

## traits

Traits documentation goes in the `traits` directory.
Look there for examples
The following is a short overview of what kind of information is expected.
Note that only new or changed config, state, and methods should be documented here, properties from required traits are implied.

``` toml
name = ""  # required
description = ""  # required
requires = []  # required (can be empty)

[config]  # optional
NAME = "TYPE"

[state]  # optional
NAME = "TYPE"

[method]  # optional

  [method.NAME]
  args.NAME = "TYPE"  # optional
  returns = "TYPE"  # optional
  description = ""  # required
```