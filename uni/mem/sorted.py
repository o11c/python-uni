# TODO replace with cache-friendly bsearch ordering.
import bisect
from collections.abc import Set, Mapping
import itertools
from numbers import Integral
import numpy as np


def bisect_right_key(a, x, lo=0, hi=None, *, key=None):
    if key is None:
        return bisect.bisect_right(a, x, lo, hi)
    key_of_x = key(x)

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key_of_x < key(a[mid]): hi = mid
        else: lo = mid+1
    return lo


def _bisect_with_tuples(arr, item, *, singleton):
    idx = bisect_right_key(arr, (item,), key=lambda t: t[0])
    assert 0 <= idx <= len(arr)
    assert idx == 0 or arr[idx - 1][0] <= item
    assert idx == len(arr) or item < arr[idx][0]
    return idx - 1


class SortedSet(Set):
    ''' Keys stored as singleton, no values.
    '''
    typical_dtype = np.dtype([('key', '>i4')])

    def __init__(self, iterable=None, *, raw=None, check=True):
        if raw is None:
            if iterable is None:
                raw = []
            else:
                raw = sorted((k,) for k in iterable)
        else:
            assert iterable is None
        self._len = len(raw)
        self._data = raw
        if check:
            assert all(isinstance(x, (tuple, np.void)) and len(x) == 1 for x in raw)
            assert all(x[0] < y[0] for (x, y) in zip(raw, itertools.islice(raw, 1, None)))

    def __contains__(self, item):
        idx = _bisect_with_tuples(self._data, item, singleton=True)
        if idx == -1:
            return False
        tup = self._data[idx]
        return tup[0] == item

    def __iter__(self):
        for k, in self._data:
            yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, raw=%r)' % (self.__class__.__qualname__, self._len, self._data)


class SortedRangeSet(Set):
    ''' Key-range stored in pairs, no values.
    '''
    typical_dtype = np.dtype([('low_key', '>i4'), ('high_key', '>i4')])

    def __init__(self, iterable=None, *, raw=None, raw_len=None, check=True):
        if raw is None:
            assert raw_len is None
            if iterable is None:
                iterable = []
            else:
                iterable = sorted((k,) for k in iterable)
            self._len = len(iterable)
            if check:
                assert all(isinstance(x, (tuple, np.void)) and len(x) == 1 and isinstance(x[0], Integral) for x in iterable)
                assert all(x[0] < y[0] for (x, y) in zip(iterable, itertools.islice(iterable, 1, None)))
            raw = []
            for k, in iterable:
                if raw and raw[-1][1] == k - 1:
                    raw[-1] = (raw[-1][0], k)
                    continue
                raw.append((k, k))
        else:
            assert iterable is None
            assert raw_len is not None
            self._len = raw_len
        self._data = raw
        if check:
            assert all(isinstance(x, (tuple, np.void)) and len(x) == 2 and isinstance(x[0], Integral) and isinstance(x[1], Integral) for x in raw)
            assert all(x[1] < y[0] for (x, y) in zip(raw, itertools.islice(raw, 1, None)))
            assert len(self) == len(list(self))

    def __contains__(self, item):
        idx = _bisect_with_tuples(self._data, item, singleton=False)
        if idx == -1:
            return False
        tup = self._data[idx]
        return tup[0] <= item <= tup[1]

    def __iter__(self):
        for k1, k2 in self._data:
            for k in range(k1, k2+1):
                yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, raw=%r)' % (self.__class__.__qualname__, self._len, self._data)


class SortedMap(Mapping):
    ''' Keys stored as first, value as second.
    '''
    typical_dtype = np.dtype([('key', '>i4'), ('value', 'O')])

    def __init__(self, iterable=None, *, raw=None, check=True):
        if raw is None:
            if iterable is None:
                raw = []
            else:
                if isinstance(iterable, Mapping):
                    iterable = iterable.items()
                raw = sorted(iterable)
        else:
            assert iterable is None
        self._len = len(raw)
        self._data = raw
        if check:
            assert all(isinstance(x, (tuple, np.void)) and len(x) == 2 for x in raw)
            assert all(x[0] < y[0] for (x, y) in zip(raw, itertools.islice(raw, 1, None)))

    def __getitem__(self, item):
        idx = _bisect_with_tuples(self._data, item, singleton=False)
        if idx != -1:
            tup = self._data[idx]
            if tup[0] == item:
                return tup[1]
        raise KeyError(item)

    def __iter__(self):
        for k, v in self._data:
            yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, raw=%r)' % (self.__class__.__qualname__, self._len, self._data)


class SortedRangeMap(Mapping):
    ''' Key-range stored as first and second, value as third.
    '''
    typical_dtype = np.dtype([('low_key', '>i4'), ('high_key', '>i4'), ('value', 'O')])

    def __init__(self, iterable=None, *, raw=None, raw_len=None, check=True):
        if raw is None:
            assert raw_len is None
            if iterable is None:
                iterable = []
            else:
                if isinstance(iterable, Mapping):
                    iterable = iterable.items()
                iterable = sorted(iterable)
            self._len = len(iterable)
            if check:
                assert all(isinstance(x, (tuple, np.void)) and len(x) == 2 and isinstance(x[0], Integral) for x in iterable)
                assert all(x[0] < y[0] for (x, y) in zip(iterable, itertools.islice(iterable, 1, None)))
            raw = []
            for k, v in iterable:
                if raw and raw[-1][1] == k - 1 and raw[-1][2] == v:
                    raw[-1] = (raw[-1][0], k, v)
                    continue
                raw.append((k, k, v))
        else:
            assert iterable is None
            assert raw_len is not None
            self._len = raw_len
        self._data = raw
        if check:
            assert all(isinstance(x, (tuple, np.void)) and len(x) == 3 and isinstance(x[0], Integral) and isinstance(x[1], Integral) for x in raw)
            assert all(x[1] < y[0] for (x, y) in zip(raw, itertools.islice(raw, 1, None)))
            assert len(self) == len(list(self))

    def __getitem__(self, item):
        idx = _bisect_with_tuples(self._data, item, singleton=False)
        if idx != -1:
            tup = self._data[idx]
            if tup[0] <= item <= tup[1]:
                return tup[2]
        raise KeyError(item)

    def __iter__(self):
        for k1, k2, v in self._data:
            for k in range(k1, k2+1):
                yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, raw=%r)' % (self.__class__.__qualname__, self._len, self._data)
