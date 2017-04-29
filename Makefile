PYTHON = python3

default: test-fast test-coverage-fast

test-fast:
test-slow:
test: test-fast test-slow

test-fast: test-unittest
test-coverage: test-unittest
test-coverage-fast: test-unittest
test-unittest:
	${PYTHON} -m coverage run -p --source=. -m unittest

test-fast: test-nose
test-nose:
	${PYTHON} -m nose

test-fast: test-pytest
test-pytest: clean-coverage
	${PYTHON} -m pytest

test-fast: test-copyright
test-copyright:
	find -name '*.py' -print0 | xargs -0 -n 1 grep -L -w Copyright

test-slow: test-schema
test-coverage: test-schema
test-schema: clean-coverage
	${PYTHON} -m coverage run -p --source=. -m uni.txt.schema --sample www.unicode.org/Public/9.0.0/ucd/ArabicShaping.txt > /dev/null
	${PYTHON} -m coverage run -p --source=. -m uni.txt.schema `find www.unicode.org/ -type f | sort` > /dev/null

test-coverage-fast: test-schema-fast
test-schema-fast: clean-coverage
	${PYTHON} -m coverage run -p --source=. -m uni.txt.schema --sample `find www.unicode.org/ -type f | sort` > /dev/null

test-slow: test-coverage
test-coverage:
	${PYTHON} -m coverage combine
	${PYTHON} -m coverage html
	${PYTHON} -m coverage report --fail-under=100
# not usually called, but useful for development
test-coverage-fast:
	${PYTHON} -m coverage combine
	${PYTHON} -m coverage html --skip-covered
	${PYTHON} -m coverage report --skip-covered --fail-under=100

clean-coverage:
	rm -f .coverage*
	rm -rf htmlcov
