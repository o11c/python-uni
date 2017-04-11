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
import numpy as np
import unittest

from uni.mem.sorted import SortedSet, SortedRangeSet, SortedMap, SortedRangeMap


class TestSortedSet(unittest.TestCase):
    def test_iter(self):
        s = SortedSet()
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedSet(set())
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedSet({2, 1})
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        s = SortedSet({'foo', 'bar'})
        assert s and len(s) == 2
        assert list(s) == ['bar', 'foo']
        s = SortedSet([])
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedSet([2, 1])
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        s = SortedSet(['foo', 'bar'])
        assert s and len(s) == 2
        assert list(s) == ['bar', 'foo']

    def test_lookup(self):
        s = SortedSet()
        assert [x for x in s if x in s] == []
        s = SortedSet({2, 1})
        assert [x for x in s if x in s] == [1, 2]
        s = SortedSet({'foo', 'bar'})
        assert [x for x in s if x in s] == ['bar', 'foo']

    def test_repr(self):
        s = SortedSet()
        repr(s)
        s = SortedSet({2, 1})
        repr(s)
        s = SortedSet({'foo', 'bar'})
        repr(s)

    def test_raw(self):
        s = SortedSet._from_raw(0, np.array([], dtype='>u4'))
        assert not s and len(s) == 0
        assert list(s) == []
        assert [x for x in s if x in s] == []
        s = SortedSet._from_raw(2, np.array([1, 2], dtype='>u4'))
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        assert [x for x in s if x in s] == [1, 2]


class TestSortedRangeSet(unittest.TestCase):
    def test_iter(self):
        s = SortedRangeSet()
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedRangeSet(set())
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedRangeSet({2, 1})
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        s = SortedRangeSet([])
        assert not s and len(s) == 0
        assert list(s) == []
        s = SortedRangeSet([2, 1])
        assert s and len(s) == 2
        assert list(s) == [1, 2]

    def test_lookup(self):
        s = SortedRangeSet()
        assert [x for x in s if x in s] == []
        s = SortedRangeSet({2, 1})
        assert [x for x in s if x in s] == [1, 2]

    def test_repr(self):
        s = SortedRangeSet()
        repr(s)
        s = SortedRangeSet({2, 1})
        repr(s)

    def test_raw(self):
        s = SortedRangeSet._from_raw(0, np.array([], dtype='>u4'), np.array([], dtype='>u4'))
        assert not s and len(s) == 0
        assert list(s) == []
        assert [x for x in s if x in s] == []
        s = SortedRangeSet._from_raw(2, np.array([1], dtype='>u4'), np.array([2], dtype='>u4'))
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        assert [x for x in s if x in s] == [1, 2]


class TestSortedMap(unittest.TestCase):
    def test_iter(self):
        m = SortedMap()
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedMap({})
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedMap({3: 'x', 1: 'y', 2: 'x'})
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        m = SortedMap({'foo': 1, 'bar': 2, 'baz': 1})
        assert m and len(m) == 3
        assert list(m) == ['bar', 'baz', 'foo']
        m = SortedMap([])
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedMap([(3, 'x'), (1, 'y'), (2, 'x')])
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        m = SortedMap([('foo', 1), ('bar', 2), ('baz', 1)])
        assert m and len(m) == 3
        assert list(m) == ['bar', 'baz', 'foo']

    def test_lookup(self):
        m = SortedMap()
        assert list(m.items()) == []
        m = SortedMap({3: 'x', 1: 'y', 2: 'x'})
        assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]
        m = SortedMap({'foo': 1, 'bar': 2, 'baz': 1})
        assert list(m.items()) == [('bar', 2), ('baz', 1), ('foo', 1)]

    def test_repr(self):
        m = SortedMap()
        repr(m)
        m = SortedMap({3: 'x', 1: 'y', 2: 'x'})
        repr(m)
        m = SortedMap({'foo': 1, 'bar': 2, 'baz': 1})
        repr(m)

    def test_raw(self):
        m = SortedMap._from_raw(0, np.array([], dtype='>u4'), np.array([], dtype='O'))
        assert not m and len(m) == 0
        assert list(m) == []
        assert list(m.items()) == []
        m = SortedMap._from_raw(3, np.array([1, 2, 3], dtype='>u4'), np.array(['y', 'x', 'x'], dtype='O'))
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]


class TestSortedRangeMap(unittest.TestCase):
    def test_iter(self):
        m = SortedRangeMap()
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedRangeMap({})
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedRangeMap({3: 'x', 1: 'y', 2: 'x'})
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        m = SortedRangeMap([])
        assert not m and len(m) == 0
        assert list(m) == []
        m = SortedRangeMap([(3, 'x'), (1, 'y'), (2, 'x')])
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]

    def test_lookup(self):
        m = SortedRangeMap()
        assert list(m.items()) == []
        m = SortedRangeMap({3: 'x', 1: 'y', 2: 'x'})
        assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]

    def test_repr(self):
        m = SortedRangeMap()
        repr(m)
        m = SortedRangeMap({3: 'x', 1: 'y', 2: 'x'})
        repr(m)

    def test_raw(self):
        m = SortedRangeMap._from_raw(0, np.array([], dtype='>u4'), np.array([], dtype='>u4'), np.array([], dtype='O'))
        assert not m and len(m) == 0
        assert list(m) == []
        assert list(m.items()) == []
        m = SortedRangeMap._from_raw(3, np.array([1, 2], dtype='>u4'), np.array([1, 3], dtype='>u4'), np.array(['y', 'x'], dtype='O'))
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]
