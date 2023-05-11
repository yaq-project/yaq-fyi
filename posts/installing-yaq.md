---
title: Installing yaq
id: installing-yaq
date: 2023-05-11
---

This page attempts to provide a quickstart guide to brand-new yaq/Python users.
Please note that there are many ways to install yaq, this is just one approach that we find easiest for beginners.
We are assuming Windows here.

This tutorial will take you from a bare [conda installation](https://docs.conda.io/en/latest/miniconda.html) through configuring and running your first yaq daemon.


[TOC]

video tutorial
--------------

<iframe width="100%" height="450" src="https://www.youtube-nocookie.com/embed/J12AuHj3JH0" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

install conda
-------------

On Windows, we prefer to manage Python via Anaconda.
You may already have Anaconda installed, in which case you can skip this step.
Please note that yaq requires Python 3.7 or newer.
Download and install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html).
You'll want the 64-bit version.

Add the [conda-forge](https://conda-forge.org/) channel, which hosts yaq packages.

    > conda config --add channels conda-forge

install yaqd-fakes
------------------

In this tutorial we will be working with the [fake-continuous-hardware](https://yaq.fyi/daemons/fake-continuous-hardware/) daemon, which is provided by the [yaqd-fakes](https://anaconda.org/conda-forge/yaqd-fakes) package.

    > conda install yaqd-fakes

install yaqc
------------

yaqc is a general purpose Python client which will afford you basic communication with any yaq daemon.
Full yaqc documentation is avaliable at [python.yaq.fyi/yaqc](https://python.yaq.fyi/yaqc).

    > conda install yaqc

install yaqd-control
--------------------

yaqd-control is a command line interface for managing and querying installed yaq daemons.
Use `--help` to see all of the commands that yaqd-control offers.

    > conda install yaqd-control
    > yaqd --help

Full yaqd-control documentation is avaliable at [control.yaq.fyi](https://control.yaq.fyi/).

configure your daemon
---------------------

Before running your daemon, you must provide some minimal configuration.

    > yaqd edit-config fake-continuous-hardware

This command will open a blank toml file at the appropriate location in notepad.
You should type the following into the configuration file:

    [mydaemon]
    port = 39000

Here, `mydaemon` is a human-friendly name that you choose, and `port` is the TCP port that the daemon will serve at.
The configuration options for a given daemon are documented on the yaq website, in this case at [yaq.fyi/daemons/fake-continuous-hardware](https://yaq.fyi/daemons/fake-continuous-hardware/#configuration).
Any options without defaults must be provided (in this case, only `port`).
Full specification of yaq daemon configuration can be found in [YEP-102](https://yeps.yaq.fyi/102/).

run your daemon in the foreground
---------------------------------

Simply type `yaqd-<kind>` to run your daemon in the foreground directly within Anaconda Prompt.
You should see some logging information get printed as the daemon runs.

    > yaqd-fake-continuous-hardware

Since this runs the daemon in the foreground, you must keep your Anaconda Prompt window open to continue running your daemon.
To close the daemon, press Ctrl+C or close the Anaconda Prompt window.

communicate with your daemon
----------------------------

Keeping your original Anaconda Prompt window open with the daemon running in the foreground, open a second Anaconda Prompt.
Type:

    > yaqd status

This will print a table of all of the daemons your computer knows about, as well as some quick information about their status.

Let's also use the yaqc Python package we installed earler.
From within Python:

    >>> import yaqc
    >>> c = yaqc.Client(39000)
    >>> c.id()
    >>> c.set_position(0)
    >>> c.get_position()

There are many ways to interact with a running daemon.
Importantly, multiple clients can communicate with the same daemon simultaniously.
Check out all of the client packages at [yaq.fyi/packages](https://yaq.fyi/packages/#clients).

run your daemon in the background
---------------------------------

Now we will properly "enable" our daemon to run in the background.
To do this, we have to register the daemon as a background application (Windows calls this a "process").
If you haven't already, close out of your foreground daemon.

Run Anaconda Prompt as Administrator.
You will be asked for your Windows login password.
These security steps are Window's way of making sure that not just anyone can install invisible applications to run in the background on your machine.

    > yaqd enable fake-continuous-hardware
    > yaqd start fake-continuous-hardware

Now your daemon is running in the background and will restart every time Windows reboots.
You can prove your daemon is online with `yaqd status`, or by using `yaqc` from within Python.

Now that you're familiar with some of the basic tooling, consider installing one of the [many other daemons](https://yaq.fyi/daemons/) that exist with the yaq ecosystem.
Have fun!
