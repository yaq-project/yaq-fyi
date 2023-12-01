---
title: busy
id: busy
date: 2023-11-30
authors: Kyle Sunden
tags: patterns
---


The concept of `busy` is something all daemons have in common. The exact
specifics do vary, but generally for motors it means that the motor is
actively moving and for sensors it means that the daemon is acquiring a
measurement. A sensor that is looping or a sensor that does not
implement `has-measure-trigger` will always report that `busy` is True.
This perhaps unintuitive choice was made so that a sensor that is in
looping mode is no different to a client that is expecting a
non-triggered sensor.

In general, `busy` gets set to True when an RPC message which changes
the state of the daemon is called, and is set to False when that change
is complete. This is then used to guard against unexpectedly using the
result of RPC calls when the daemon is in a state of flux or otherwise
is not ready. When possibly, busy can be read directly from the
hardware, though care must be taken to ensure that if a change has been
requested busy never reports False until that change is complete. A
specific (but recurring) instance of this idea is explored in detail
below.

`busy` is a boolean flag that can be read internally by daemon methods
using `self._busy` and by clients over the RPC by using `client.busy()`.
If one wants to wait for a specific state, it is possible to simply poll
the busy state until it is either True or False, whichever is required.
While that is the only mechanism available to clients, internally there
are additional features that allow you to explicitly wait for the rising
or falling edge of `busy` without polling. There is a pair of
[`asyncio.Event`](https://docs.python.org/3/library/asyncio-sync.html)
objects which allow explicit awaiting on
either busy or not busy, `self._busy_sig` and `self._not_busy_sig`.
These provide signals that the Asyncio event loop explicitly knows that
tasks waiting on them are not ready until the associated `event.set()`
method is called. These `set` methods are called (or reset) whenever
`self._busy` is updated, so daemon implementors need only to properly
update that boolean for everything else to work as expected.

Example usage of the `busy` Asyncio features:

```python
async def update_state(self):
    while True:
        await self._not_busy_sig.wait()
        self._logger.info("No longer busy")
        await self._busy_sig.wait()
        self._logger.info("Busy again")
```
