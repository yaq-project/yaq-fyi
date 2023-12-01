## Daemon patterns: async serial devices

One of the most common hardware interfaces is RS-232 style serial
communication. While the exact protocol for what bytes get sent over the
wire differs greatly, many of these interfaces share common behaviors.
Often there are multiple devices that are addressed and communicated to
over the same serial bus. In some cases, the information provided by
replies from hardware is insufficient to in and of itself identify which
method is being replied to. For this hardware, careful timing control
must be used to correlate the request to the reply. In other cases, the
reply itself contains both information about which device and what
information is contained in the message. Sometimes, these self
describing messages can even originate directly from the hardware, with
no explicit request from the daemon side of the communication.

When the messages are self describing, a good pattern is to allow the
write actions, that is requests for information or commands to move,
etc., to happen in multiple places, but have a centralized task to
interpret the replies. Using this pattern, the code can be more
logically separated, and there is less strict timing considerations
regarding ensuring that you get the reply to the message you requested
specifically. This is because all replies are handled, but with grace
for time between replies being variable, and multiple requests can be
pending.

However, there are some common pitfalls of this approach, for which care
must be taken. Because the Asyncio scheduler does not guarantee order of
execution (and simply because communication with hardware takes time),
there may be replies that are not processed by reading task that
indicate that the device is not busy, even when a move has been
requested. If care is not taken to account for this, the reply handler
will accept that the daemon is not busy and clients may read that it is
not busy and assume it is safe to continue. The same (though potentially
even more avenues for "not busy" to be unintentionally reported) can be
said for homing of motors that communicate in this way. That said, once
you understand what is happening, it is not so difficult to enforce
correct external behavior using a few additional boolean flags.

To put this in concrete terms, I will walk through the Thorlabs Ell
series daemon. This daemon uses a class called a `SerialDispatcher`
which buffers write actions to ensure that the devices have time to
process the commands and does some parsing of all incoming data from
hardware. The dispatcher is responsible for determining that a message
is correctly formed and which specific daemon instance should receive
the message. The dispatcher is not required for all hardware,
particularly if there is never more than one device on the serial bus.

First, the `__init__` method:

``` python
def __init__(self, name, config, config_filepath):
    self._homing = True
    self._homing_sig = asyncio.Event()
    self._move_started = False
    self._address = config["address"]
    if config["serial_port"] in ThorlabsEllx.serial_dispatchers:
        self._serial = ThorlabsEllx.serial_dispatchers[config["serial_port"]]
    else:
        self._serial = SerialDispatcherEll(
            aserial.ASerial(config["serial_port"], config["baud_rate"])
        )
        ThorlabsEllx.serial_dispatchers[config["serial_port"]] = self._serial
    self._read_queue = asyncio.Queue()
    self._serial.workers[self._address] = self._read_queue
    super().__init__(name, config, config_filepath)
    self._units = config["units"]
    self._conversion = config["scalar"]
    self._serial.write(f"{self._address:X}gs\r\n".encode())
    self._state["status"] = ""
    self._tasks.append(self._loop.create_task(self._home()))
    self._tasks.append(self._loop.create_task(self._consume_from_serial()))
```

`_homing` and `_move_started` are the two boolean flag variables that
will help ensure that `busy` is properly reported at all times.
`_homing_sig` is an Asyncio Event, much like those associated with
`busy`. It is used to inform the homing task that homing is complete so
that it can reset the position to the current destination. The
`SerialDispatcher` objects are shared among all daemons that communicate
over the same serial bus, so if it already exists, the instance retains
a reference to the previously made dispatcher, and creates a new one if
it does not already exist.

`read_queue` is an [Asyncio Queue](https://docs.python.org/3/library/asyncio-queue.html)
object which is a
first-in first-out (FIFO) queue that is appended to by the dispatcher,
and consumed by the daemon. It is added to the serial dispatcher with
the address as a key.

At startup, the daemon requests the initial status using `gs`. It also
requests a Home operation and initiates the `_consume_from_serial` task,
each of which are added to the list of `self._tasks` which are properly
cancelled upon shutdown.

`_consume_from_serial` is the task which waits for messages from the
hardware and properly updates the daemon's internal state accordingly:

```python
async def _consume_from_serial(self):
    while True:
        comm, val = await self._read_queue.get()
        self.logger.debug(f"incoming serial: {comm} {val}")

        if "PO" == comm:
            position = struct.unpack(">l", bytes.fromhex(val))[0]
            position /= self._conversion
            self._state["position"] = position
        elif "GS" == comm:
            self._busy = (int(val, 16) != 0) or self._homing or self._move_started
            self._state["status"] = self.error_dict.get(int(val, 16), "")
            if int(val, 16) not in (0, 9):
                # ignore normal busy/ready mode, log any other error
                self.logger.error(f"ERROR CODE: {self._state['status']}")
        else:
            self.logger.warning(f"Unhandled serial response: {comm}{val}")

        self._read_queue.task_done()
        if self._read_queue.empty():
            self._move_started = False
```

The `await` for this `async` method is not a simple poll frequency, but
rather waiting for a preprocessed message from the dispatcher. The
message comes as a tuple of the command ID and the remaining unparsed
contents, which contain the actual information. Unrecognized messages
are logged, as well as reported error states from the hardware.
Importantly, the line which sets `self._busy` does not only account for
the hardware busy state, but also for the daemon's own knowledge of
whether a home or set position has been initiated, using the boolean
flags. At the bottom, the queue marks the task as processed and resets
the `_move_started` flag if there are no messages left to process. This
works specifically because the problem of having unprocessed messages
which contradict the correct `busy` state is no longer possible once
there are no active messages. The hardware has been informed to move,
and will correctly report `busy` in any messages received *after* the
write is complete.

However, processing incoming information only happens for this device if
it has been requested, so this daemon uses `self.update_state` to
request updates for the status and position:

```python
    async def update_state(self):
        while True:
            if not self._homing and not self._move_started:
                self._serial.write(f"{self._address:X}gs\r\n".encode())
                self._serial.write(f"{self._address:X}gp\r\n".encode())
            await asyncio.sleep(0.2)
```

The poll frequency matters, as if you ask faster than you can parse the
replies, the queue will never empty. A faster polling frequency will
give finer grained updates in position. Ideally, the polling is at a
rate where it does not matter if you are one polling period later for
the purposes of timing control, but that the replies are always
processed before new requests are made. To fully ensure that the queue
empties when the timing control requires it, fewer additional replies
are requested when the boolean flags are set, though homing does rely on
the status being updated. Note that in this case, `update_state` does
*cause* the state to be updated, but the actual updates are in
`_consume_from_serial`.

Finally, `home` and `set_position` take into account the added
variables:

```python
def _set_position(self, position):
    self._move_started = True
    if not self._homing:
        pos = round(position * (self._conversion))
        pos1 = struct.pack(">l", pos).hex().upper()
        self._serial.write(f"{self._address:X}ma{pos1}\r\n".encode())

def home(self):
    self._busy = True
    self._loop.create_task(self._home())

async def _home(self):
    self._homing = True
    await self._serial.write_queue.join()
    await asyncio.sleep(0.2)
    await self._read_queue.join()
    self._serial.write(f"{self._address:X}ho0\r\n".encode())
    self._homing = False
    await asyncio.sleep(0.2)
    await self._read_queue.join()
    self._busy = True
    await self._not_busy_sig.wait()
    self.set_position(self._state["destination"])
```

`_set_position` flips `_move_started` to True and does not preempt an
active home. If a home is occurring, the position will be properly set
at the end of the home operation anyway.

Homing may seem complicated at first, but is actually only a few simple
ideas. First, there is the homing flag, which surrounds all of the
homing operation, set to true at the start and False at the end of the
method. This ensures that `busy` never goes False during this method
(and the behavior of `set_position` itself ensures it never goes False
until that move is complete as well). Next, the method actually writes
the home command, and waits a short bit to ensure that the message gets
sent since the Serial Dispatcher buffers those commands and writes them
asynchronously. Third, it clears the incoming message buffer, ensuring
that any messages that had outdated `busy` state information are
processed while the homing flag prevents `busy` from being False. Next
it resets the signal used to determine if homing is complete and waits
for it to be set by `_consume_from_serial`. Finally, it sets the
position to the expected destination.
