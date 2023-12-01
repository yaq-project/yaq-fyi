---
title: implementing has-position
id: has-position
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


`has-position` is one of the most commonly used traits, and it is
required by several other traits. The central idea is that there is one
value, the position, represented as a floating point number, which
describes the core functionality of the daemon. This is a value that
might be scanned for an acquisition such as the color of a light source
or position of a translation stage. In , even hardware which is
fundementally discrete, such as shutters or valves, are mapped to a
floating point position variable for consistency, though interacting
using the `is-discrete` trait may be more natural in those cases.

When implementing a `has-position` daemon, there are actually only a
small number of things to consider, as much of the functionality is
provided by the mix-in class. You must consider the units of the
position, if units are provided (they can be `None`, the default, if no
units make logical sense). You must implement the procedure for actually
communicating with the hardware and setting the position:
`_set_position`. This is implemented as a private function (beginning
with `_`) because the mix-in class (and, in fact, some of the mix-in
classes for related traits) manage setting of some state variables such
as `destination`. Next you must implement some mechanism of updating the
state variable for `position`. Depending on the hardware interface, this
could mean polling the hardware for its direct knowledge of its
position, updating the position in response to communication initated by
the hardware, or even simply setting the state value in the position
setting function if there is no mechanism to query the hardware.
Finally, you must carefully manage the `busy` state of the daemon. It is
expected that the daemon will return busy at every instance between the
request being sent and the motion being complete. `busy` is set to True
by the mix-in class when the request is first processed, but it must be
set back to False by the daemon implementation. It is common to update
both busy and position in the `update_state` asynchronous method, though
other options are valid.

```python
class MyDaemon(HasPosition, IsDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(self, name, config, config_filepath)
        self.units = "mm"
        self.dev = Device() # Some generic manufacturer interface

    def _set_position(self, position):
        self.dev.write(position)

    async def update_state(self):
        while True:
            self._state["position"] = self.dev.read()
            self.busy = not self.dev.is_still()
            await asyncio.sleep(0.1)
```
