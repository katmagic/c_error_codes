c_error_codes
=============

**Homepage**: [GitHub](https://github.com/katmagic/c_error_codes)<br />
**Git**: [GitHub](git://github.com/katmagic/c_error_codes.git)<br />
**License**: [UNLICENSE](http://unlicense.org)<br />
**Author**: [katmagic](mailto:the.magical.kat@gmail.com) ([E51DFE2C][key])<br />
[key]: https://keyserver.pgp.com/vkd/DownloadKey.event?keyid=0xD1EACB65E51DFE2C

About
-----

`c_error_codes` is a small Python module to let you check `errno` against C
constants.

Usage
-----

Check if setuid(0) succeeded.

	from c_error_codes import *
	import ctypes, ctypes.util

	libc_name = ctypes.util.find_library("c")
	ctypes.cdll.LoadLibrary(libc_name)
	libc = ctypes.CDLL(libc_name, use_errno=True)

	libc.setuid(0) # this should fail
	if ctypes.get_errno() == EPERM:
			raise EPERM("We're not good enough to become root!")

	# Maybe we don't know what kind of error we're going to get.
	raise( CError(ctypes.get_errno(), "Couldn't setuid(0).") )
