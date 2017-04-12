test-fast:
test-slow:
test: test-fast test-slow

test-fast: test-unittest
test-unittest:
	python3 -m unittest

test-fast: test-nose
test-nose:
	python3 -m nose

test-fast: test-pytest
test-pytest:
	python3 -m pytest --cov=.
	coverage html

test-fast: test-copyright
test-copyright:
	find -name '*.py' -print0 | xargs -0 -n 1 grep -L -w Copyright

test-slow: test-schema
test-schema:
	python3 -m uni.txt.schema ucd/**/*.txt > /dev/null
