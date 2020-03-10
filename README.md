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
family = ""  # required (can be base)
traits = []  # required (can be empty)

[links]  # all optional, arbitrary keys supported
documentation = ""
source = ""
bugtracker = ""

[install]
language = "python"  # required
# other keys optional, language dependent

[config]  # optional
NAME.type = "TYPE"  # required for each parameter
NAME.default = ""  # if absent, parameter will be required
NAME.options = ""  # optional
NAME.description = ""  # optional

[state]  # optional
NAME.type = "TYPE"  # required for each parameter
NAME.description = "" # optional

[method]  # optional

  [method.NAME]
  args.NAME.type = "TYPE"  # required for each argument
  args.NAME.default = ""  # if absent, argument will be required
  args.NAME.options = ""  # optional
  args.NAME.description = ""  # optional
  returns = "TYPE"  # optional
  description = ""  # required
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
NAME.type = "TYPE"  # required for each parameter
NAME.default = ""  # if absent, parameter will be required
NAME.options = ""  # optional
NAME.description = ""  # optional

[state]  # optional
NAME.type = "TYPE"  # required for each parameter
NAME.description = "" # optional

[method]  # optional

  [method.NAME]
  args.NAME.type = "TYPE"  # required for each argument
  args.NAME.default = ""  # if absent, argument will be required
  args.NAME.options = ""  # optional
  args.NAME.description = ""  # optional
  returns = "TYPE"  # optional
  description = ""  # required
```
