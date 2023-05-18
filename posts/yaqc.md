---
title: yaqc Introduction
id: yaqc
date: 2023-05-11
authors: Kyle Sunden
---

[TOC]

Installation
------------

A generic python yaq client is can be installed via
[PyPI](https://pypi.org/project/yaqc/). The client program works on
Python ≥ 3.6.


    $ pip install yaqc

Or installed via conda:

    conda install -c conda-forge yaqc

You may also install from source:


    $ git clone https://gitlab.com/yaq/yaqc-python
    $ cd yaqc-python
    $ pip install .

Connecting
----------

`yaqc` provides a generic client which dynamically adds methods to match
those provided by the daemon it is connected to. To connect to a daemon
running locally on port 38000:


    >>> import yaqc
    >>> client = yaqc.Client(38000)

If your daemon is running remotely, simply add the host as a paramter:


    >>> import yaqc
    >>> client = yaqc.Client(38000, host="123.123.123.123")

`client` is now a python object which can be used as any other, with all
the expected methods. For example, if the daemon implements the
`has-position` trait, the object will have methods `get_position`,
`set_position` and so on.

The daemon which you are connecting to need not be itself implemented in
python, only has to follow the yaq daemon specification.

Using the Client
----------------

Methods are called on the client object, which handles the daemon
communication layer transparently:


    >>> client.id()
    {'name': 'my-test-daemon', 'kind': 'some-daemon-kind', 'make': None, 'model': None, 'serial': None}


### Subclassing

While the generic client exposes all daemon capabilities, there may be
times where you wish to add some client side computation (e.g. unit
translation, stringing together multiple daemon calls). This is allowed,
and can be accomplished using subclassing. The code which is generates
the dynamic functions will not overwrite your own functions (it will
also not populate the doc string).

The following is an example of a subclass which uses the
[unyt](https://unyt.readthedocs.io/en/stable/) library to provide client
side unit conversion:

```
import unyt
import yaqc

class UnitClient(yaqc.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This assumes the `has_position` trait is implemented
        self._units = self.get_units()

    def set_position(self, position, units=None):
        """Set the position to a value in units.

        Parameters
        ----------
        position: float or unyt.unyt_quantity
	    The position to set.
        units: string or unyt.Unit
	    The units for the number.
        """
        if units is not None:
           position = unyt.unyt_quantity(position, units)
        if isinstance(position, unyt.unyt_quantity):
           position.convert_to_units(self._units)
        return self.send("set_position", float(position))
```

In this example, the `set_position` method will not be overwritten. A
similar function could be written for `get_position`.

Links
-----

-   [Source Code](https://gitlab.com/yaq/yaqc-python)
-   [Issue Tracker](https://gitlab.com/yaq/yaqc-python)
-   [PyPi](https://pypi.org/project/yaqc/)
