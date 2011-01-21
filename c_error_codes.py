#!/usr/bin/env python
# This is free and unencumbered software released into the public domain. For
# more information, please refer to http://unlicense.org/.
#
# hugs and kisses,
# ~katmagic

"""This file is the equivalent of <errno.h>. It should only be used when
interfacing with C programs, i.e. through ctypes."""

import re as _re

_INCLUDE_PATH = "/usr/include/asm-generic/"

_DESC = dict()
# This is less complicated than it looks.
_r= _re.compile(r"^#define\s*([A-Z]+)\s*(\d+)\s*/\*\s*(.*?)\s*\*/\s*$")
for _f in (open(_INCLUDE_PATH+_) for _ in ("errno.h", "errno-base.h")):
    for _m in filter(None, (_r.match(_l) for _l in _f)):
        # for every line in <errno.h> and <errno-base.h> that matches _r
        _name, _value, _description = _m.groups()

        if _value.startswith("0x"):
            _value = int(_value, 16)
        else:
            _value = int(_value, 10)

        _DESC[int(_value)] = (_name, _description)

# _DESC now looks something like this:
#   {
#       1: ('EPERM', 'Operation not permitted'),
#       2: ('ENOENT', 'No such file or directory'),
#       3: ('ESRCH', 'No such process'),
#       ...
#   }

class CError(Exception):
    def __init__(self, errno, extra=None):
        self.value = errno
        self.name, self.comment = _DESC[errno]
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
            return type(self)(self.value, msg)
        else:
            return self

for _err in (CError(_) for _ in _DESC):
    globals()[_err.name] = _err
