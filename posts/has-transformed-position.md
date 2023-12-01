---
title: implementing has-transformed-position
id: has-transformed-position
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


At first, implementing `has-transformed-position` seems like a daunting
task. There are many methods that are implemented which naturally are
all interconnected. However, most of the heavy lifting is implemented by
the mix-in class, leaving only a couple variables for the simplest case
and optionally a couple methods for more complex cases. If all you want
is a simple shift of where the zero position is, then the default
implementation will work and all you have to think about is setting the
variable `self._native_units` in the same manner as `self._units` for a
generic `has-position` device. Consideration for the default or setting
the state value introduced by `has-transformed-position`,
`native_reference_position`, at initialization time may be useful as
well.

More complicated cases, such as those with non-unity transformation
functions, must also implement two methods: `_relative_to_transformed`
and `_transformed_to_relative`. These two functions work together to
provide the scaling factors between the native position and the
transformed position. They are referred to as "relative" rather than
"native" because the mix-in class still manages adding and subtracting
the `native_reference_position`. The two functions must provide the
expected inversion such that calling one on the result of the other
returns the original input (within rounding errors). Additional
configuration and/or state values may be required to properly compute
the transformation, but that will depend on the specific circumstances.

Additionally, some implementations may need to override one or more of
the methods, for instance `set_native_reference`, to properly update
their state, such as the `yaqd-attune-delay` daemon offseting the
spectral delay correction curve.

Because the mix-in class relies on calling methods of `HasPosition`,
care should be taken to ensure that the `HasTransformedPosition` class
appears *before* `HasPosition` in the class declaration.

```python
class MyDaemon(HasTransformedPosition, HasPosition, IsDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._native_units = "cm"
        self._units = "cc"

    def _relative_to_transformed(self, relative_position):
        return relative_position ** 3

    def _transformed_to_relative(self, transformed_position):
        return transformed_position ** (1/3)
```
