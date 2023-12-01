---
title: implementing has-mapping
id: has-mapping
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


`has-mapping` builds upon the `is-sensor` trait by providing access to
parallel arrays, such as the wavelength data for an array detector or
spatial information for a camera. Since `has-mapping` requires
`is-sensor`, all of the details of implementing a sensor apply.
Implementing `has-mapping` requires only the setting of some instance
attributes which are quite similar to how all `is-sensor` devices manage
the channel names, units, and shapes. All of the messages provided by
the trait are implemented by the provided mix-in class, referencing the
expected variables. Mappings have their own names, strings which
identify them as separable arrays. A channel may have multiple mappings,
including multiple mappings along the same axis, this simply means that
all of the arrays are parallel. For instance, a camera may provide a
mapping for both wavelength information and index information, the
latter of which may identify where on the physical camera a selected
area of interest is located, while the former provides information of
interest to plotting. A channel may also have multiple mappings for
different axis, such as the x axis and y axis of a camera.

The three variables are `self._channel_mappings`, `self._mapping_units`,
and `self._mappings`. Each of these is a dictionary which provides
particular information about the mappings. The first,
`self._channel_mappings`, determines which mappings are associated with
each channel. The keys are the channel names, and the values are a list
of mapping names which apply to that channel. Each channel should appear
in this list, but may have zero mappings associated. The second
variable, `self._mapping_units` works much the same as
`self._channel_units` for any sensor, except that the keys are the
mapping names. The values are either `None` for unitless quantities or a
string for the unit. Both `self._channel_mappings` and
`self._mapping_units` should be static and only set once. Finally,
`self._mappings` is a dictionary with the mapping names as keys and the
actual arrays (or scalars, though such usage is uncommon) as values. The
arrays must have shapes which broadcast to all associated channels
identified by `self._channel_mappings`.

If the mapping is entirely static (e.g. it is read from the device and
is not dependent on other inputs) then all of the variables can be set
in the daemon's `__init__` method. If the mappings are dynamic, then
they must be set as a response to updated inputs. The mix-in class
manages the state of a fourth variable, `self._mapping_id`, which is an
integer that simply increments every time new mapping arrays are
provided.

The following snippet shows the relevant portions of a daemon which
implements a camera with an area of interest specified by configuration
variables and mappings which identify the physical indices of the axes:

```python
class MyDaemon(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath):

        ...

        self.x_index = np.arange(
            config["aoi_left"],
            config["aoi_left"] + config["aoi_width"],
            dtype="i2"
        )[None, :]
        self.y_index = np.arange(
            config["aoi_top"],
            config["aoi_top"] + config["aoi_height"],
            dtype="i2"
        )[:, None]

        # populate channels
        self._channel_names = ["image"]
        self._channel_units = {"image": None}
        self._channel_mappings = {"image": ["x_index", "y_index"]}
        self._channel_shapes = {"image": [config["aoi_height"], config["aoi_width"]]}
        self._mappings = {"x_index": self.x_index, "y_index": self.y_index}
```

This example if for a daemon with a static mapping, one with a dynamic
mapping would include a line such as:

```python
self._mappings = self.gen_mapping()
```

Where `self.gen_mapping` is a function which returns a valid mapping
dictionary. This line could appear multiple times and does not need to
be in `__init__`, though it should be called at least once before a
measurement is taken.
