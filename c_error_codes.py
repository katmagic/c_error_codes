#!/usr/bin/env python
# This is free and unencumbered software released into the public domain. For
# more information, please refer to http://unlicense.org/.
#
# hugs and kisses,
# ~katmagic

"""This file is the equivalent of <errno.h>. It should only be used when
interfacing with C programs, i.e. through ctypes."""

import re as _re

class CError(Exception):
    def __init__(self, name, value, comment, extra=None):
        self.value = int(value)
        self.name = name
        self.comment = comment
        self.extra = extra

        super().__init__(str(self))

    def __str__(self):
        if self.extra:
            return "{0.extra} ({0.name}: {0.comment})".format(self)
        else:
            return "{0.name}: {0.comment}".format(self)

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __req__(self, other):
        return self.value == other

    def __call__(self, msg=None):
        if msg:
            return type(self)(self.name, self.value, self.comment, msg)
        else:
            return self


# This is less complicated than it looks.
_regexp = _re.compile( r"^#define\s*([A-Z]+)\s*(\d+)\s*/\*\s*(.*?)\s*\*/\s*$" )

for _ in ("errno.h", "errno-base.h"):
    with open("/usr/include/asm-generic/"+_) as _f:
        for _l in _f:
            _m = _regexp.match(_l)
            if _m:
                _name, _value, _comment = _m.groups()
                globals()[_name] = CError(_name, _value, _comment)
