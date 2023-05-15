---
title: SciPy 2020 Recap
id: scipy-2020-recap
date: 2023-05-11
---

[TOC]

## Virtual 'Poster'

[Here](https://python.yaq.fyi/scipy-2020/) is a link to our SciPy 2020 virtual 'poster'.

## Hardware Birds-Of-a-Feather session

Blaise Thompson and Kyle Sunden (the lead developers of yaq) hosted a BOF at Scipy 2020, the [recording](https://www.youtube.com/watch?v=6HxVbK14EDI) is available on youtube.

## Projects we learned about

### [bluesky](https://blueskyproject.io/)

- Collection of sub projects
- [ophyd](https://bluesky.github.io/ophyd) for hardware abstraction
- [bluesky](https://bluesky.github.io/bluesky) for acquisition orchestration
- [suitcase](https://bluesky.github.io/suitcase) for data recording/serialization
- [databroker](https://bluesky.github.io/databroker) for data management
- Runs large scale facilities (including [NSLS-II](https://www.bnl.gov/ps/)
- Explicitly designed to scale down to single PI labs

### [Mjolnir](https://github.com/hamma-dev/mjolnir-hamma)

- "Scientific IOT" sensor management
- [SciPy Talk](https://www.youtube.com/watch?v=s1V1_M8ani8&list=PLYx7XA2nY5GezZTawXyl76LqVf3qbn-5E&index=7)

### [1000x Lab](https://www.1000xlab.com/)

- Enthought initiative for open hardware and lab automation
- Includes a "Congress" (think small conference)
- [SciPy Talk](https://www.youtube.com/watch?v=6JIhviWYYAg)

## [yaqc-bluesky](https://github.com/bluesky/yaqc-bluesky)


After attending SciPy 2020 and talking to the developers of Bluesky, we at yaq have decided to push forward with a first class bridge from yaq into bluesky.
This will enable users of yaq to tap into the powerful data acquisition pipeline provided by Bluesky.


