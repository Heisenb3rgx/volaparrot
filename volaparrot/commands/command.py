"""
The MIT License (MIT)
Copyright © 2015 RealDolos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
# pylint: disable=missing-docstring,broad-except,too-few-public-methods
# pylint: disable=bad-continuation,star-args,too-many-lines

import logging

from random import shuffle
from time import time

from volapi.arbritrator import ARBITRATOR


__all__ = ["Command", "FileCommand", "PulseCommand"]

logger = logging.getLogger(__name__)

class Dong:
    dongs = ["Dong is a homo",
             "Dong is a refugee",
             "Dong did not confess",
             "Dongmaster is the new MercWMouth",
             "Dong supports loli in /v/",
             "Dongmaster is cancer",
             "This notifies Dongmaster",
             "Dong has 60 OT accounts",
             "Dongmaster is such a cuck, even Swedes hate him",
             "Dongmaster eats nigger semen",
             "Dongmaster drinks buckets of muslim semen",
             "Dongmaster's mom installed Parental Controls",
             ]

    def __init__(self):
        self.cool = 0
        self.current = None

    def dong(self, msg):
        if len(msg) > 280:
            return None
        now = time()
        if self.cool + 10*60 > now:
            return None
        self.cool = now
        dong = None
        try:
            dong = self.current.pop()
        except Exception:
            self.current = self.dongs[:]
            shuffle(self.current)
            dong = self.current.pop()
        return dong


class Command:
    active = True
    shitposting = False
    greens = False
    dong = Dong()


    def __init__(self, room, admins, *args, **kw):
        args, kw = kw, args
        self.room = room
        #if not hasattr(self.room, "dong"):
        #    self.room.dong = Dong()

        self.admins = admins
        handlers = getattr(self, "handlers", list())
        if isinstance(handlers, str):
            handlers = handlers,
        self._handlers = list(i.casefold() for i in handlers)

    def handles(self, cmd):
        return cmd in self._handlers

    def post(self, msg, *args, **kw):
        if self.room.name == "x33JTJR":
            return
        msg = msg.format(*args, **kw)[:300]
        #dong = self.room.dong.dong(msg)
        #if dong:
        #    msg = msg + "\n" + dong
        #    msg = msg[:300]

        if not self.active:
            logger.info("Swallowed %s", msg)
            return
        self.room.post_chat(msg)

    @staticmethod
    def nonotify(nick):
        return "{}\u2060{}".format(nick[0], nick[1:])

    def isadmin(self, msg):
        return msg.logged_in and msg.nick in self.admins

    def allowed(self, msg):
        return not self.greens or msg.logged_in

    def call_later(self, delay, callback, *args, **kw):
        # pylint: disable=no-member
        ARBITRATOR.call_later(self.room, delay, callback, *args, **kw)


class FileCommand(Command):
    def __call__(self, cmd, remainder, msg):
        return False


class PulseCommand(Command):
    interval = 0

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.last_interval = 0
        if self.interval <= 0:
            raise RuntimeError("No valid interval")

    def __call__(self, cmd, remainder, msg):
        return False

    def check_interval(self, current, interval=1.0):
        result = current >= self.last_interval + interval
        if result:
            self.last_interval = current
        return result

