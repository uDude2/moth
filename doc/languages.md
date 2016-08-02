Languages We Use, And Why
==================

Whenever possible, we use Python 3,
because just about everybody can read and write Python.

Python 3 has a nice distinction between strings and bytestreams.
You might not like it,
but it forces you to think about which one you're dealing with,
which is a good thing now that printable characters are no longer always 8 bits.


On The Server
-------------------

Things that have to run on the contest server can be written in:

* Vanilla Bourne shell (not BASH)
* Awk
* Lua

These are chosen because they come on OpenWRT.
Python is a real pain in the rear to cross-compile,
plus it's huge,
so we don't have anything use it on the server.


On The Client
------------------

JavaScript, baby.
