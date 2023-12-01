## Implementing traits: is-homeable

`is-homeable` is a trait which provides a single method, `home`, which
must be implemented.

Notably, what "home" means in is "Go to your limit to determine your
absolute position, then return to your current destination". This is
often *not* the same as what an individual device will do when homing,
which is often only the first half. Additionally, homing is a task which
takes time to complete, which is contrary to the philosophy which
expects methods to return quickly. As such, there are some common
patterns to homing hardware where the `home` message itself initiates an
asynchronous task that actually accomplishes homing. The details of how
each device knows when to move on will vary, but in general it looks
something like:

```python
class MyDaemon(IsHomeable, HasPosition, IsDaemon):

    ...

    def home(self):
        self._busy = True
        self._loop.create_task(self._home())

    async def _home(self):
        self._homing = True
        self._done_homing = False
        self._busy = True
        self.device.home()
        while not self.device.homed():
            await asyncio.sleep(0.01)
        self.set_position(self._state["destination"])
        self._homing = False
```

Care must be taken to avoid reporting that `busy` is False at any point
during the homing procedure.
