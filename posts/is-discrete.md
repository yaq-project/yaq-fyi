## Implementing traits: is-discrete

`is-discrete` is an addition to `has-position` which allows you to
provide a set of named positions which can be set by providing the name
instead of the value. The trait provides a standard configuration
option, `identifiers`, which allows users to specify the named positions
in config. However, some hardware natively support the functionality, so
those are allowed to ignore the configuration value and read the list of
identifiers from the device. If you are using the configuration values,
then the only additional implementation consideration is to update the
state value `position_identifier` with the appropriate value (a string
indicating the descrete position or None, indicating that the device is
not at one of the named positions. What it means to be "at" the named
position will vary for the particular details of the hardware. Some
hardware will want a level of tolerance, some will always report an
exact number, and some will not natively have any in-between values that
are even possible.

```python
class MyDaemon(IsDiscrete, HasPosition, IsDaemon):
    ...
    async def update_state(self):
        while True:
            self._state["position"] = self.dev.read()
            self.busy = not self.dev.is_still()
            self._state["position_identifier"] = self.dev.get_position_name()
            await asyncio.sleep(0.1)
```
