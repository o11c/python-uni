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

    def test_raw(self):
        s = SortedSet(raw=np.array([], dtype=SortedSet.typical_dtype))
        assert not s and len(s) == 0
        assert list(s) == []
        assert [x for x in s if x in s] == []
        s = SortedSet(raw=np.array([(1,), (2,)], dtype=SortedSet.typical_dtype))
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

    def test_raw(self):
        s = SortedRangeSet(raw_len=0, raw=np.array([], dtype=SortedRangeSet.typical_dtype))
        assert not s and len(s) == 0
        assert list(s) == []
        assert [x for x in s if x in s] == []
        s = SortedRangeSet(raw_len=2, raw=np.array([(1, 2)], dtype=SortedRangeSet.typical_dtype))
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

    def test_raw(self):
        m = SortedMap(raw=np.array([], dtype=SortedMap.typical_dtype))
        assert not m and len(m) == 0
        assert list(m) == []
        assert list(m.items()) == []
        m = SortedMap(raw=np.array([(1, 'y'), (2, 'x'), (3, 'x')], dtype=SortedMap.typical_dtype))
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

    def test_raw(self):
        m = SortedRangeMap(raw_len=0, raw=np.array([], dtype=SortedRangeMap.typical_dtype))
        assert not m and len(m) == 0
        assert list(m) == []
        assert list(m.items()) == []
        m = SortedRangeMap(raw_len=3, raw=np.array([(1, 1, 'y'), (2, 3, 'x')], dtype=SortedRangeMap.typical_dtype))
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]
