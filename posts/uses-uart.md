## Implementing traits: uses-uart

`uses-uart` is a trait which exists solely to standardize the names
provided to common configuration values among Universal Asynchronous
Receiver-Transmitter (UART) style communication. Common examples of UART
style communication are RS-232 and RS-485.

As UART is a serial protocol, use of this trait requires the use and
implementation of the `uses-serial` trait.

These devices will typically appear as a `COM<n>` port in Windows or
something similar to `/dev/ttyACM0` in Linux. The operating system
specific identifier is the first config field specified by the
`uses-uart` trait, `serial_port`. The second configuration value,
`baud_rate`, indicates the speed of data transmission, which must be the
same for both devices on either end of the transmission. Some devices
have variable baud rates, while others have fixed baud rates. In the
latter case (or even if it is variable, but the device itself has a
default) it often makes sense to add a default value for `baud_rate` in
the TOML file for the protocol.

```toml
traits = ["uses-uart", "uses-serial", "is-daemon"]

[config]
baud_rate.default = 19200
```

As a python implementation, the `UsesUart` class does nothing other than
ensure that the required `UsesSerial` class is included in the class
inheritance. The config values defined by `uses-uart` are accessed in
the normal fashion.

While devices using this trait may wish to consider using some of the
more advanced patterns below, it is entirely valid to start with a
simple [PySerial](https://pyserial.readthedocs.io/) implementation as shown here:

```python
import serial
from yaqd_core import UsesUart, UsesSerial, IsDaemon

class MyDaemon(UsesUart, UsesSerial, IsDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._ser = serial.Serial(config["serial_port"], config["baud_rate"])

    def close(self):
        self._ser.close()
:::
