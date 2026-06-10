---
title: implementing has-turret
id: has-turret
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


`has-turret` is designed for devices such as monochromators that have a
secondary position called a "turret", such as the ones used for
selecting gratings. The trait has three methods, comprising one single
property: `get_turret`, `set_turret`, and `get_turret_options`. There is
also a state value, `turret`, which stores the current value of the
property.

To implement `has-turret`, the setter and the options getter must be
implemented. The options getter should return a list of string names
which are valid options for `set_turret`. The getter is implemented by
the `HasTurret` mix-in class, simply returning the value as stored in
the state dictionary.

The state value can either be updated when it is set or asynchronously
by reading from the device.

```python
class MyDaemon(HasTurret, IsDaemon):

    ...

    def get_turret_options(self):
        return ["ir", "vis", "uv"]

    def set_turret(self, turret):
        self.device.set_turret(self.gratings[turret]["index"])
        self.device.set_position(self._state["destination"])
        self._calculate_limits()
```
