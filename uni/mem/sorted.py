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

from .._util import ErrorBool, MinIter


def round_up_to_pow2(x):
    assert x > 0
    return 1 << (x-1).bit_length()


def adjacent(left, right, *, step=1):
    try:
        check = left + step
    except TypeError:
        return False
    return check == right


class SortedSet(Set):
    ''' Simple binary-search set.
    '''
    def __init__(self, iterable=None):
        self._len = 0
        self._keys = []
        if iterable is not None:
            iterable = sorted(iterable)
            for key in iterable:
                self._append(key)

    def _append(self, key):
        assert not self._len or self._keys[-1] < key
        self._keys.append(key)
        self._len += 1

    def _pop(self):
        self._keys.pop()
        self._len -= 1

    @classmethod
    def _from_raw(cls, len, keys):
        self = cls.__new__(cls)
        self._len = len
        self._keys = keys
        return self

    def _to_raw(self):
        return self._len, self._keys

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


class RangeSet(Set):
    ''' Compressed binary-search set.
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

    def _to_raw(self):
        return self._len, self._low_keys, self._high_keys

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


class AutoSet(Set):
    ''' Multi-strategy binary-search set.
    '''
    def __init__(self, iterable=None):
        self._simple = SortedSet()
        self._compressed = RangeSet()
        if iterable is not None:
            iterable = sorted(iterable)
            for key in iterable:
                self._append_range(key, key)

    def _append_range(self, low_key, high_key):
        assert not self._simple._len or self._simple._keys[-1] < low_key
        assert not self._compressed._len or self._compressed._high_keys[-1] < low_key
        assert low_key <= high_key
        if self._simple._len and adjacent(self._simple._keys[-1], low_key):
            low_key = self._simple._keys[-1]
            self._simple._pop()
            self._compressed._append_range(low_key, high_key)
            return
        if low_key != high_key or (self._compressed._len and adjacent(self._compressed._high_keys[-1], low_key)):
            self._compressed._append_range(low_key, high_key)
            return
        self._simple._append(low_key)

    @classmethod
    def _from_raw(cls, simple_raw, compressed_raw):
        self = cls.__new__(cls)
        self._simple = SortedSet._from_raw(*simple_raw)
        self._compressed = RangeSet._from_raw(*compressed_raw)
        return self

    def _to_raw(self):
        return self._simple._to_raw(), self._compressed._to_raw()

    def __contains__(self, item):
        return item in self._simple or item in self._compressed

    def __iter__(self):
        return MinIter(self._simple, self._compressed)

    def __len__(self):
        return self._simple._len + self._compressed._len

    def __repr__(self):
        return '%s(simple=%r, compressed=%r)' % (self.__class__.__qualname__, self._simple, self._compressed)


class SortedMap(Mapping):
    ''' Simple binary-search dict.
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
        assert not self._len or self._keys[-1] < key
        self._keys.append(key)
        self._values.append(value)
        self._len += 1

    def _pop(self):
        self._keys.pop()
        self._values.pop()
        self._len -= 1

    @classmethod
    def _from_raw(cls, len, keys, values):
        self = cls.__new__(cls)
        self._len = len
        self._keys = keys
        self._values = values
        return self

    def _to_raw(self):
        return self._len, self._keys, self._values

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


class RangeMap(Mapping):
    ''' Compressed binary-search dict (for equal values).
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

    def _to_raw(self):
        return self._len, self._low_keys, self._high_keys, self._values

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

    def _pop_range(self):
        low_key = self._low_keys.pop()
        high_key = self._high_keys.pop()
        self._values.pop()
        self._len -= high_key - low_key + 1

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


class DeltaMap(Mapping):
    ''' Compressed binary-search dict (for sequential values).
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

    def _to_raw(self):
        return self._len, self._low_keys, self._high_keys, self._values

    def _append_range(self, low_key, high_key, value):
        assert not self._len or self._high_keys[-1] < low_key
        assert low_key <= high_key
        if self._len and self._high_keys[-1] + 1 == low_key and self._values[-1] + (low_key - self._low_keys[-1]) == value:
            self._high_keys[-1] = high_key
        else:
            self._low_keys.append(low_key)
            self._high_keys.append(high_key)
            self._values.append(value)
        self._len += high_key - low_key + 1

    def _pop_range(self):
        low_key = self._low_keys.pop()
        high_key = self._high_keys.pop()
        self._values.pop()
        self._len -= high_key - low_key + 1

    def __getitem__(self, item):
        idx = bisect.bisect_right(self._low_keys, item) - 1
        if idx != -1:
            assert self._low_keys[idx] <= item
            if item <= self._high_keys[idx]:
                return self._values[idx] + (item - self._low_keys[idx])
        raise KeyError(item)

    def __iter__(self):
        for k1, k2, v in zip(self._low_keys, self._high_keys, self._values):
            for k in range(k1, k2+1):
                yield k

    def __len__(self):
        return self._len

    def __repr__(self):
        return '%s(len=%d, low_keys=%r, high_keys=%r, values=%r)' % (self.__class__.__qualname__, self._len, self._low_keys, self._high_keys, self._values)


class AutoMap(Mapping):
    ''' Multi-strategy binary-search dict.
    '''
    def __init__(self, iterable=None):
        self._simple = SortedMap()
        self._compressed = RangeMap()
        self._sequential = DeltaMap()
        if iterable is not None:
            if isinstance(iterable, Mapping):
                iterable = iterable.items()
            iterable = sorted(iterable)
            for key, value in iterable:
                self._append_range(key, key, value, ErrorBool)

    def _append_range(self, low_key, high_key, value, is_delta):
        assert not self._simple._len or self._simple._keys[-1] < low_key
        assert not self._compressed._len or self._compressed._high_keys[-1] < low_key
        assert not self._sequential._len or self._sequential._high_keys[-1] < low_key
        assert low_key <= high_key
        if self._simple._len and adjacent(self._simple._keys[-1], low_key):
            if (low_key == high_key or not is_delta) and self._simple._values[-1] == value:
                low_key = self._simple._keys[-1]
                self._simple._pop()
                self._compressed._append_range(low_key, high_key, value)
                return
            if (low_key == high_key or is_delta) and adjacent(self._simple._values[-1], value):
                low_key = self._simple._keys[-1]
                value = self._simple._values[-1]
                self._simple._pop()
                self._sequential._append_range(low_key, high_key, value)
                return
        # If both compression and sequential apply, convert (2, 1) into (1, 2)
        # so that later appends can take full advantage of the longer range.
        if low_key == high_key:
            if self._compressed._len and adjacent(self._compressed._low_keys[-1], self._compressed._high_keys[-1]):
                if adjacent(self._compressed._high_keys[-1], low_key) and adjacent(self._compressed._values[-1], value):
                    self._simple._append(self._compressed._low_keys[-1], self._compressed._values[-1])
                    self._sequential._append_range(self._compressed._high_keys[-1], low_key, self._compressed._values[-1])
                    self._compressed._pop_range()
                    return
            if self._sequential._len and adjacent(self._sequential._low_keys[-1], self._sequential._high_keys[-1]):
                # Note: we use adjacent() for the values isntead of ==, since we have to undo the delta.
                if adjacent(self._sequential._high_keys[-1], low_key) and adjacent(self._sequential._values[-1], value):
                    self._simple._append(self._sequential._low_keys[-1], self._sequential._values[-1])
                    self._compressed._append_range(self._sequential._high_keys[-1], low_key, value)
                    self._sequential._pop_range()
                    return
        if low_key == high_key or not is_delta:
            if low_key != high_key or (self._compressed._len and adjacent(self._compressed._high_keys[-1], low_key) and self._compressed._values[-1] == value):
                self._compressed._append_range(low_key, high_key, value)
                return
        if low_key == high_key or is_delta:
            if low_key != high_key or (self._sequential._len and adjacent(self._sequential._high_keys[-1], low_key) and adjacent(self._sequential._values[-1], value, step=(low_key - self._sequential._low_keys[-1]))):
                self._sequential._append_range(low_key, high_key, value)
                return
        assert low_key == high_key
        self._simple._append(low_key, value)

    @classmethod
    def _from_raw(cls, simple_raw, compressed_raw, sequential_raw):
        self = cls.__new__(cls)
        self._simple = SortedMap._from_raw(*simple_raw)
        self._compressed = RangeMap._from_raw(*compressed_raw)
        self._sequential = DeltaMap._from_raw(*sequential_raw)
        return self

    def _to_raw(self):
        return self._simple._to_raw(), self._compressed._to_raw(), self._sequential._to_raw()

    def __getitem__(self, item):
        try:
            return self._simple[item]
        except KeyError:
            pass
        try:
            return self._compressed[item]
        except KeyError:
            pass
        return self._sequential[item]

    def __iter__(self):
        return MinIter(self._simple, self._compressed, self._sequential)

    def __len__(self):
        return self._simple._len + self._compressed._len + self._sequential._len

    def __repr__(self):
        return '%s(simple=%r, compressed=%r, delta=%r)' % (self.__class__.__qualname__, self._simple, self._compressed, self._sequential)
