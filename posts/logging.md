---
title: logging
id: logging
date: 2023-11-30
authors: Kyle Sunden
tags: patterns
---


Logging can be a powerful tool for decyphering what a daemon is doing.
In the Python implementation, the logging system of is integrated with
the standard library [logging](https://docs.python.org/3/library/logging.html) module
defines a few extra logging levels to conform to a non-python specific standard initially
provided by [sd-daemon](https://systemd.network/sd-daemon.html) and syslog. In
practice, however, the extra levels are rarely used.

Each daemon instance has its own logger, `self.logger`, which is set up
to properly format the log messages and print to STDERR and, if
configured, output to a file as well. Daemon implementors are encouraged
to sprinkle helpful log messages where it makes sense. Messages which
are only useful in debugging specific contexts, particularly those that
are verbose to the point of obscuring other log messages, should be
included using `self.logger.debug(message)`. By default, these messages
will not be displayed, but by passing `–verbose` to the daemon command
or editing the configuration file the debug logs will be included.
Messages about ordinary operations, particularly information provided at
start up or shut down should be logged with `self.logger.info(message)`.
Logs related to errors, such as errors being reported by the hardware,
or errors in communication with the hardware itself should be logged
using `self.logger.error(message)` Additionally, while less comonly
used, `self.logger.warning(message)` exists for warning users of
potential unexpected behavior, such as that caused by falling back to
default values.

```python
class MyDaemon(IsDaemon):

    ...

    def test_logging(self):
        self.logger.debug("This is a debug message")
        self.logger.info("This is an informational message")
        self.logger.warning("This is a warning message")
        self.logger.error("This is an error message")
:::
