test-fast:
test-slow:
test: test-fast test-slow

test-fast: test-pytest
test-pytest:
	python3 -m pytest

test-fast: test-copyright
test-copyright:
	find -name '*.py' -print0 | xargs -0 -n 1 grep -L -w Copyright

test-slow: test-schema
test-schema:
	python3 -m uni.txt.schema ucd/**/*.txt > /dev/null
