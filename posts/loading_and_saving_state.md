## Daemon patterns: loading and saving state

Daemon state management is usually fairly automated such that individual
daemon authors rarely need to think deeply on the subject. State files
are stored in a standard location as a TOML file as specified by
[YEP 103](https://yeps.yaq.fyi/103/).
At initialization time, the file is read if it exists, and
missing values are filled with the default value from the protocol
definition.

These values are held in memory in a dictionary called `self._state`,
which is updated by the daemon when the daemons state changes, either
due to user interaction or due to changes read from the hardware itself.

On a regular schedule (approximately 10 Hz when a daemon is busy, and
approximately 1 Hz when a daemon is not busy) the daemon will write out
the contents of its in-memory state, if it has been updated. Note that
the daemon will acknowledge that the state is updated automatically only
if the top level keys or values have been updated. If you have a
complicated state such as a nested dictionary, then you may wish to
explicitly mark the state as updated by including
`self._state.updated = True` when the dictionary is updated without
updating the top level of the state.
