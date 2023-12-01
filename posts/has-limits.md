---
title: implementing has-limits
id: has-limits
date: 2023-11-30
authors: Kyle Sunden
tags: traits
---


`has-limits` augments `has-position` by adding boundaries which are
queryable and checked when setting positions. Most of the implementation
is handled by the mix-in class, so the only consideration on the
implementation side is to set the state value `hw_limits`, which defines
the limits imposed by the hardware itself. Sometimes this can be read
from the device, other times it is known through documentation, and
still others there is no actual way to tell and the `hw_limits` should
be set to -infinity to +infinity. Even in the latter case, it can be
useful to include the `has-limits` trait because software limits can be
imposed by users via configuration.
