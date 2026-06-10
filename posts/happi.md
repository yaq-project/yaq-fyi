---
title: yaq and happi
id: happi
date: 2023-05-11
authors: Blaise Thompson
tags: bluesky howto
---

[Happi](https://github.com/pcdshub/happi) (Heuristic Access to Positioning of Photon Instrumentation), is a Python package developed at the [Linac Coherent Light Source](https://lcls.slac.stanford.edu/).
Happi is part of the [Bluesky ecosystem](https://blueskyproject.io/).

Happi provides an interface for discovering hardware interfaces.
Despite the name containing "photon", Happi's interface is generic.
It's somewhat like a database for [Bluesky interface](https://blueskyproject.io/bluesky/hardware.html) objects.
Tools like [Typhos](https://github.com/pcdshub/typhos) can automatically use Happi to discover what hardware is avaliable on a given machine.

yaq integrates with Happi via the [yaqc-bluesky](https://github.com/bluesky/yaqc-bluesky) package.
yaq users may add yaqc-bluesky instances to the Happi database.
Importantly, yaqc-bluesky instances exist seamlessly in Happi alongside other Bluesky interface providers.

# backends

We recommend using Happi's JSON backend in user data directory.
Here's how to make a Happi client using this path.

```
import appdirs
import pathlib
import happi

# make happi client
db_path = pathlib.Path(appdirs.user_data_dir("happi")) / "db.json"
happi_backend = happi.backends.backend(db_path)
happi_client = happi.Client(database=happi_backend)
```

We'll be using this as our backend example for the rest of this discussion.
Of-course any Happi-supported backend will work, see [Happi's documentation on selecting a backend](https://pcdshub.github.io/happi/client.html#selecting-a-backend).

# adding

Let's add a new yaqc-bluesky instance to Happi.
In this case we have a daemon locally at port 38500.

```
>>> import yaqc_bluesky
>>> item = yaqc_bluesky.happi_containers.YAQItem(name="test", port=38500)
>>> happi_client.add_device(item)
`test`
```

# searching

Once a device has been added to Happi we can search for it.

```
>>> happi_client.find_device(name="test")
```

# loading

Loading gives back the yaqc-bluesky device itself.

```
>>> happi_client.load_device(name="test")
<yaqc_bluesky._device.YAQDevice object at 0x7f227963e790>
```
