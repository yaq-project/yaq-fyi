---
title: implementing uses-i2c
id: uses-i2c
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


`uses-i2c` is a trait which exists solely to standardize the name of the
config value for the I2C address, `i2c_addr`.

I2C (inter-integrated circuit) is a low-level communication protocol for
serial communication designed for communication between two devices such
as microcontollers. SMBus is a similar protocol that is
slightly more strict, but largely is interoperable with I2C, and is thus
included for the purposes of the trait. I2C typically exists on a
network with one primary device and a series of secondary devices. The
primary device controls the timing and generates requests for data from
the secondary devices. The address is an integer which is used to
designate which secondary device should accept the data and write
responses.

Most of the devices that currently exist in the ecosystem which
implement this trait are intended to work with a Raspberry Pi, which
provides direct access to an I2C bus via the General Purpose Input
Output (GPIO) pins.

As I2C is a serial protocol, use of this trait requires the use and
implementation of the `uses-serial` trait.

You can add a default value to your particular configuration if one
makes sense for your hardware, though often it is reasonable to say that
the address is required in all cases.
