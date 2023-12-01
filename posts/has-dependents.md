## Implementing traits: has-dependents

`has-dependents` provides a mechanism to discover relationships between
daemons. It provides a single method, `get_dependent_hardware`, which
returns a map of names to host:port strings.

``` python
class MyDaemon(HasDependents, IsDaemon):

    ...

    def get_dependent_hardware(self):
        return {"child": f"{self._wrapped_daemon._host}:{self._wrapped_daemon._port}"}
```
