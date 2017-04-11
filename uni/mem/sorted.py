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
# TODO replace with cache-friendly bsearch ordering.
import bisect
from collections.abc import Set, Mapping
import itertools
from numbers import Integral


def round_up_to_pow2(x):
    assert x > 0
    return 1 << (x-1).bit_length()


class SortedSet(Set):
    ''' Keys stored as singleton, no values.
    '''
    def __init__(self, iterable=None):
        self._len = 0
        self._keys = []
        if iterable is not None:
            iterable = sorted(iterable)
            for key in iterable:
                self._append(key)

    def _append(self, key):
        self._keys.append(key)
        self._len += 1

    @classmethod
    def _from_raw(cls, len, keys):
        self = cls.__new__(cls)
        self._len = len
        self._keys = keys
        return self

    def __contains__(self, item):
        idx = bisect.bisect_right(self._keys, item) - 1
        if idx != -1:
            assert self._keys[idx] <= item
            if item == self._keys[idx]:
                return True
        return False

    def __iter__(self):
        for k, in zip(self._keys):
            yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, keys=%r)' % (self.__class__.__qualname__, self._len, self._keys)


class SortedRangeSet(Set):
    ''' Key-range stored in pairs, no values.
    '''
    def __init__(self, iterable=None):
        self._len = 0
        self._low_keys = []
        self._high_keys = []
        if iterable is not None:
            iterable = sorted(iterable)
            for key in iterable:
                self._append_range(key, key)

    def _append_range(self, low_key, high_key):
        assert not self._len or self._high_keys[-1] < low_key
        assert low_key <= high_key
        if self._len and self._high_keys[-1] + 1 == low_key:
            self._high_keys[-1] = high_key
        else:
            self._low_keys.append(low_key)
            self._high_keys.append(high_key)
        self._len += high_key - low_key + 1

    @classmethod
    def _from_raw(cls, len, low_keys, high_keys):
        self = cls.__new__(cls)
        self._len = len
        self._low_keys = low_keys
        self._high_keys = high_keys
        return self

    def __contains__(self, item):
        idx = bisect.bisect_right(self._low_keys, item) - 1
        if idx != -1:
            assert self._low_keys[idx] <= item
            if item <= self._high_keys[idx]:
                return True
        return False

    def __iter__(self):
        for k1, k2 in zip(self._low_keys, self._high_keys):
            for k in range(k1, k2+1):
                yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, low_keys=%r, high_keys=%r)' % (self.__class__.__qualname__, self._len, self._low_keys, self._high_keys)


class SortedMap(Mapping):
    ''' Keys stored as first, value as second.
    '''
    def __init__(self, iterable=None):
        self._len = 0
        self._keys = []
        self._values = []
        if iterable is not None:
            if isinstance(iterable, Mapping):
                iterable = iterable.items()
            iterable = sorted(iterable)
            for key, value in iterable:
                self._append(key, value)

    def _append(self, key, value):
        self._keys.append(key)
        self._values.append(value)
        self._len += 1

    @classmethod
    def _from_raw(cls, len, keys, values):
        self = cls.__new__(cls)
        self._len = len
        self._keys = keys
        self._values = values
        return self

    def __getitem__(self, item):
        idx = bisect.bisect_right(self._keys, item) - 1
        if idx != -1:
            assert self._keys[idx] <= item
            if item == self._keys[idx]:
                return self._values[idx]
        raise KeyError(item)

    def __iter__(self):
        for k, v in zip(self._keys, self._values):
            yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, keys=%r, values=%r)' % (self.__class__.__qualname__, self._len, self._keys, self._values)


class SortedRangeMap(Mapping):
    ''' Key-range stored as first and second, value as third.
    '''
    def __init__(self, iterable=None):
        self._len = 0
        self._low_keys = []
        self._high_keys = []
        self._values = []
        if iterable is not None:
            if isinstance(iterable, Mapping):
                iterable = iterable.items()
            iterable = sorted(iterable)
            for key, value in iterable:
                self._append_range(key, key, value)

    @classmethod
    def _from_raw(cls, len, low_keys, high_keys, values):
        self = cls.__new__(cls)
        self._len = len
        self._low_keys = low_keys
        self._high_keys = high_keys
        self._values = values
        return self

    def _append_range(self, low_key, high_key, value):
        assert not self._len or self._high_keys[-1] < low_key
        assert low_key <= high_key
        if self._len and self._high_keys[-1] + 1 == low_key and self._values[-1] == value:
            self._high_keys[-1] = high_key
        else:
            self._low_keys.append(low_key)
            self._high_keys.append(high_key)
            self._values.append(value)
        self._len += high_key - low_key + 1

    def __getitem__(self, item):
        idx = bisect.bisect_right(self._low_keys, item) - 1
        if idx != -1:
            assert self._low_keys[idx] <= item
            if item <= self._high_keys[idx]:
                return self._values[idx]
        raise KeyError(item)

    def __iter__(self):
        for k1, k2, v in zip(self._low_keys, self._high_keys, self._values):
            for k in range(k1, k2+1):
                yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, low_keys=%r, high_keys=%r, values=%r)' % (self.__class__.__qualname__, self._len, self._low_keys, self._high_keys, self._values)
