## Daemon patterns: async interfaces

The Python implementation of makes use of
[AsyncIO](https://docs.python.org/3/library/asyncio.html) to do what
is called "cooperative multitasking". Asyncio is built into the Python
language and provides additional syntax to declare functions which are
called asynchronously. Asyncio has an "event loop" which schedules a
series of tasks, tracking dependencies between tasks and allowing those
tasks that are able to run execution time. The key idea, and the reason
it is called "cooperative", is that each task should not block so as to
allow all of the other tasks to complete. Only one task is ever actually
running at any given instant, though many may be ready to run and
awaiting selection, giving an effect very similar to having multiple
threads, but without as much overhead or risk of invalid shared data.
Asyncio is good for tasks which are mostly waiting for things to happen
such as user input or network traffic. This behavior makes Asyncio an
ideal choice for tasks such as networking or other input-output (IO)
bound tasks, which is why it is used by , a framework that does both
networking and IO with hardware. Conversely, Asyncio is a poor choice
for computation heavy tasks, as it does add overhead and a long running
computation will prevent other tasks from receiving computation time.

While the internals of the core library make extensive use of Asyncio to
manage incoming RPC messages and running multiple daemon instances in
the same process, where possible the usage of Asyncio is not something
that daemon implementors need to spend a lot of time worrying about for
most messages. There are some exceptions, though, as any long running
tasks require at least a little bit of knowledge of Asyncio and best
practices. The actual python function called as a response to an
incoming RPC message is always synchronous. It is expected to itself
return quickly, which is better for both the daemon process itself and
for clients. The synchronous method that is directly called may,
however, initiate an asynchronous task.

Asyncio introduces two additional keywords for the Python language:
`async` and `await`. `async` is used to declare functions as
asynchronous and `await` is used to call such functions, preventing the
calling function from continuing until a result is provided:

```python
async def async_function(self):
    await asyncio.sleep(1)
```

Functions which have the `async` keyword are often referred to as
"coroutines" to indicate that the mechanism by which they are called
differs from standard function calls and that they are part of the
cooperative multitasking. `await` can only be used within an
asynchronous function, so to start a parallel task from a synchronous
method you would do:

```python
def sync_funtion(self):
    self._loop.create_task(async_function)
```

This works in because there is already a running event loop and each
daemon instance holds a reference to the event loop.

When writing an asynchronous method, you must be considerate of other
tasks that may be running. This means that there should not be places
where the code is blocking, waiting for something to happen. Instead,
use an asynchronous equivalent where possible. For instance, instead of
using `time.sleep(1.0)`, use `await asyncio.sleep(1.0)`. An increasing
number of libraries are either implementing an Asyncio interface or have
an alternative dependency that is only Asyncio, consider using these
interfaces if ones built specifically for your hardware exist. The
`await` keyword returns execution control to the scheduler and allows
other tasks to complete rather than holding on to the processing. If
there is a way to wait specifically for something to happen or a result
to be finished, rather than polling, that is preferable. If there is a
loop, especially one that may be an infinite loop, ensure that there is
an `await` statement for every possible code path. Even if you have no
explicit thing to wait for, there should be a line for
`await asyncio.sleep(0)`. This tells the scheduler that other tasks can
run, but if no other tasks are ready, this task can continue
immediately. This ensures that other tasks get an opportunity to run,
rather than having one task which monopolizes the computation time. In
particular, if you are handling exceptions, make sure that an await
happens either before the exception can occur or in the `except` block.

There are three main areas that a daemon implementor needs to think
about Asyncio: monitoring state updates from the daemon that are not in
response to client messages, homing motors, and reading sensors.

### Monitoring state updates

For a lot of hardware, there are messages to determine the state of the
hardware such as position or whether or not it is actively moving, as
read directly from the hardware interface. It is generally good practice
to poll this information to maintain a complete and correct
understanding of the state of the hardware. However, these updates are
not raised as a reaction to direct client RPC calls, and instead have to
happen in parallel, as a separate Asyncio task. By convention, a task
called `update_state` is used for this purpose. There is nothing
actually special about this method other than that it is explicitly
cancelled upon shutdown, automatically. Users are free to start their
own tasks if it makes logical sense to have more than one task running
in parallel. In fact, by adding any created tasks, as returned by
`self._loop.create_task`, to the `self._tasks` list these additional
tasks will be similarly cancelled at when a shutdown is requested. By
default, the method does precisely nothing, simply returning and ending
the task.

When it is used, it almost always has a loop, often one that is
intentionally infinite. Take, for example, the version of the
`update_state` method from the Attune Delay daemon:

```python
async def update_state(self):
    """Continually monitor and update the current daemon state."""
    while True:
        self._busy = self._wrapped_daemon.busy()
        self._state["position"] = self._to_ps(self._wrapped_daemon.get_position())
        if self._busy:
            await asyncio.sleep(0.01)
        else:
            await asyncio.sleep(0.1)
```

This method starts with `while True:`, which is an infinite loop. There
are no `break` statements, nor do we expect in normal operation for
there to be any exceptions raised. The task will not terminate without
being cancelled from another task. Since this particular daemon wraps
another daemon, the busy state is read and updated, along with a small
amount of calculation for the position. Importantly, this is followed by
an `await` statement, though the poll freqency is faster when busy
compared to when it is not busy.

### Homing

An example of this pattern is already shown above in the section on
implementing the `is-homing` trait. Essentially this is a case of the
synchronous method needing to initiate a longer task. For some hardware,
it may make sense to treat simple setting of position in much the same
way, though most manage it by polling the state for updates. There are
often additional flags or Asyncio events that must be managed in
relation to homing, the specifics will vary for particular hardware.

### Reading sensors

The abstract method for all sensors that implement `has-measure-trigger`
is an asynchronous method, `self._measure`. In many cases, the fact of
this being asynchronous can be largely ignored. If the hardware has an
interface which returns quickly and there is no necessary waiting period
such as an integration time, then this method can simply communicate
with the hardware and return. It is not necessary to have an `await`
statement just because it is an `async` function.

The reason the abstract method is asynchronous is so that it generalizes
to hardware which may have either waiting periods or natively
asynchronous communication. If it had been implemented as a synchronous
method, then implementing such interfaces would have been much more
difficult. Conversely, since it is an asynchronous method, those
implementations that would have been served by a synchronous
implementation only have an additional keyword.

Using Asyncio works well for sensors which have a "kickoff" method to
initiate the measurement which is not itself a blocking method call.
These sensors typically also have a method that informs the caller of
whether or not the measurment is done. Such methods can be polled with
an `await asyncio.sleep` call to limit the poll rate and allow other
tasks to complete. Finally, when it is ready the actual data can be read
and returned.

```python
async def _measure(self):
    self.dev.start_measurement()
    while not self.dev.measurement_ready():
        await asyncio.sleep(0.01)
    return {"chan": self.dev.read()}
```

There are some sensors that do not fit well into that pattern, though.
Some sensors only provide fully blocking calls that wait for the entire
acquisition time. In this instance, the blocking method can still be
used, but should be wrapped and called in a way that does not prevent
the Asyncio event loop from running additional tasks. This is done by
using `self._loop.run_in_executor`, which is a method provided by
Asyncio that runs a blocking call in a separate thread, and allows the
calling funtion to `await` the result as if it is an asynchronous
function. This is not preferable behavior, as the standard hazards of
using threads once again apply, even the ones that using Asyncio usually
sidesteps, but it allows for daemons with such hardware interfaces to
behave correctly.

An example of a blocking interface using a thread pool executor:

```python
async def _measure(self):
    arr = await self._loop.run_in_executor(None, self.device.trigger_and_read)
    return {"chan": arr}
```
