#   python-uni - complete access to the Unicode® database
#   Copyright © 2017  Ben Longbons
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import random
import string
import unittest

from uni._util import (
    ClassDict,
    MinIter,
    ErrorBoolType,
    ErrorBool,
    ProgrammerIsAnIdiotError,
    ordered_sample,
    split_ext_harder,
)


class Foo:
    pass


class TestClassDict(unittest.TestCase):
    def setUp(self):
        foo = Foo()
        foo.bar = 'baz'
        foo.qux = 3
        self.foo_obj = foo
        self.foo_cd = ClassDict(foo)

    def test_iter(self):
        assert set(self.foo_cd) == {'bar', 'qux'}
        assert dict(self.foo_cd) == {'bar': 'baz', 'qux': 3}
        assert len(self.foo_cd) == 2

    def test_mut(self):
        del self.foo_cd['bar']
        self.foo_cd['qux'] += 1
        assert dict(self.foo_cd) == {'qux': 4}


class TestMinIter(unittest.TestCase):
    def test_hardcoded(self):
        lr10 = list(range(10))
        assert list(MinIter([0, 1, 2, 3, 4], [5, 6, 7, 8, 9])) == lr10
        assert list(MinIter([5, 6, 7, 8, 9], [0, 1, 2, 3, 4])) == lr10
        assert list(MinIter([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])) == lr10
        assert list(MinIter([1, 3, 5, 7, 9], [0, 2, 4, 6, 8])) == lr10
        assert list(MinIter([0], [0])) == [0, 0]

    def test_random(self):
        for _ in range(100):
            num_samples = random.randint(0, 4)
            expected = []
            samples = []
            for _ in range(num_samples):
                sample_size = random.randint(0, 26)
                s = ordered_sample(string.ascii_lowercase, sample_size)
                expected.extend(s)
                samples.append(s)
            expected.sort()
            assert list(MinIter(*samples)) == expected


class TestErrorBool(unittest.TestCase):
    def test_id(self):
        assert ErrorBoolType() is ErrorBool

    def test_repr(self):
        assert repr(ErrorBool) == 'ErrorBool'

    def test_use(self):
        self.assertRaises(ProgrammerIsAnIdiotError, bool, ErrorBool)


class TestOrderedSample(unittest.TestCase):
    def test_edge(self):
        x = list(reversed(string.ascii_lowercase))
        assert ordered_sample(x, 0) == []
        assert ordered_sample(x, 26) == x

    def test_random(self):
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        for _ in range(100):
            k = random.randint(0, len(x))
            s = ordered_sample(x, k)
            indices = [x.index(v) for v in s]
            assert all([indices[i-1] < indices[i] for i in range(1, k)])


class TestSplitExtHarder(unittest.TestCase):
    def test_stuff(self):
        assert split_ext_harder('') == ('', [])
        assert split_ext_harder('Z') == ('Z', [])
        assert split_ext_harder('Z.Z') == ('Z', ['.Z'])
        assert split_ext_harder('Z.a') == ('Z', ['.a'])
        assert split_ext_harder('a') == ('a', [])
        assert split_ext_harder('a.Z') == ('a', ['.Z'])
        assert split_ext_harder('a.a') == ('a', ['.a'])
        assert split_ext_harder('.') == ('.', [])
        assert split_ext_harder('.Z') == ('.Z', [])
        assert split_ext_harder('.Z.Z') == ('.Z', ['.Z'])
        assert split_ext_harder('.Z.a') == ('.Z', ['.a'])
        assert split_ext_harder('.a') == ('.a', [])
        assert split_ext_harder('.a.Z') == ('.a', ['.Z'])
        assert split_ext_harder('.a.a') == ('.a', ['.a'])
        assert split_ext_harder('..') == ('..', [])
        assert split_ext_harder('..Z') == ('..Z', [])
        assert split_ext_harder('..Z.Z') == ('..Z', ['.Z'])
        assert split_ext_harder('..Z.a') == ('..Z', ['.a'])
        assert split_ext_harder('..a') == ('..a', [])
        assert split_ext_harder('..a.Z') == ('..a', ['.Z'])
        assert split_ext_harder('..a.a') == ('..a', ['.a'])
        assert split_ext_harder('...') == ('...', [])
        assert split_ext_harder('...Z') == ('...Z', [])
        assert split_ext_harder('...Z.Z') == ('...Z', ['.Z'])
        assert split_ext_harder('...Z.a') == ('...Z', ['.a'])
        assert split_ext_harder('...a') == ('...a', [])
        assert split_ext_harder('...a.Z') == ('...a', ['.Z'])
        assert split_ext_harder('...a.a') == ('...a', ['.a'])

        assert split_ext_harder('foo.Z.Z.gz.Z') == ('foo', ['.Z', '.Z', '.gz', '.Z'])
        assert split_ext_harder('foo.Z.Z.gz.txt') == ('foo.Z.Z.gz', ['.txt'])
        assert split_ext_harder('foo.Z.Z.txt.Z') == ('foo.Z.Z', ['.txt', '.Z'])
        assert split_ext_harder('foo.Z.txt.gz.Z') == ('foo.Z', ['.txt', '.gz', '.Z'])
        assert split_ext_harder('foo.txt.Z.gz.Z') == ('foo', ['.txt', '.Z', '.gz', '.Z'])
