---
title: implementing is-sensor and has-measure-trigger
id: is-sensor
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


Most sensor devices in the ecosystem also implement
`has-measure-trigger` for software triggering of process of measurement.
That trait actually simplifies implementation by providing a standard
way of updating the measurements that the generic `is-sensor` daemon
cannot guarantee in order to be flexible to more kinds of sensors.

All `is-sensor` daemons must ensure that a few variables are consistent,
usually in their `__init__` method:

-   `self._channel_names`: a list of string names

-   `self._channel_units`: A mapping of the same names from
    `_channel_names` to string units or None

-   `self._channel_shapes`: A mapping of theh same names from
    `_channel_names` to tuples representing the shape of the channel. If
    all channels are scalar values, this can be ignored and default
    behavior will properly report as much.

If you are implementing a `has-measure-trigger` daemon, then much of
this bookkeeping is provided by the associated mix-in class. The only
thing to do is implement `self._measure()`, a method which returns the
dictionary of channel names to measured values. This is an asynchronous
method, so long running data acquisitions, such as waiting for
integration times, should not block the daemon such that additional
queries are responded to quickly. If the native interface itself must
block in a way that asyncio cannot bypass, then the measurment must be
completed in a separate thread so that the daemon itself is not
completely locked.

```python
class MyDaemon(HasMeasureTrigger, IsSensor, IsDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.device = AsyncDevice()
        self.channel_names = ["ch0", "ch1", "ch2", "ch3"]
        self.channel_units = {x: "V" for x in self.channel_names}

    async def _measure(self):
        out = {}
        for ch in self.channel_names:
            out[ch] = await self.device.read(ch)
        return out
```

If you are implementing a sensor that does not have a software trigger,
such as one that subscribes to updates produced elsewhere, then you are
responsible for updating the `self._measured` dictionary, including
adding the `measurement_id`.
