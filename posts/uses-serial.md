## Implementing traits: uses-serial

`uses-serial` is a trait which defines only one message:
`direct_serial_write(bytes message)`. This trait is required by the
`uses-i2c` and `uses-uart` traits. The method provided by this trait is
intended for use as a debugging tool, and not for normal operations.

To implement a `uses-serial` daemon, the programmer needs to simply
implent the method directly. You may wish to include logging data read
from the device as a response to the command, though what makes sense
will depend heavily on the hardware.

```python
class MyDaemon(UsesSerial, IsDaemon):

    ...

    def direct_serial_write(self, message: bytes) -> None:
        self.ser.write(message)
        out = self.ser.readline()
        self.logger.debug(f"direct serial write: {out.decode()}")
```
