#! /usr/bin/env python3

import sys

if __name__ == "__main__":
	# Check if the user is using the correct version of Python
	python_version = sys.version.split()[0]

	if sys.version_info < (3, 10):
		sys.exit(1)

	from clitemnestra import clitemnestra
	clitemnestra.main()
