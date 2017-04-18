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
import collections.abc
import os


class ClassDict(collections.abc.MutableMapping):
    ''' Wrapper for cls.__dict__ that supports assignment.
    '''
    def __init__(self, cls):
        self.cls = cls
        self.dct = cls.__dict__

    def __getitem__(self, k):
        return self.dct[k]

    def __setitem__(self, k, v):
        setattr(self.cls, k, v)

    def __delitem__(self, k):
        delattr(self.cls, k)

    def __iter__(self):
        return iter(self.dct)

    def __len__(self):
        return len(self.dct)


class MinIter:
    def __init__(self, *iterables):
        self._iterators = []
        self._values = []
        for iterable in iterables:
            iterator = iter(iterable)
            try:
                value = next(iterator)
            except StopIteration:
                continue
            self._iterators.append(iterator)
            self._values.append(value)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._values:
            raise StopIteration
        idx = min(range(len(self._values)), key=lambda i: self._values[i])
        rv = self._values[idx]
        try:
            self._values[idx] = next(self._iterators[idx])
        except StopIteration:
            del self._iterators[idx]
            del self._values[idx]
        return rv


class ProgrammerIsAnIdiotError(AssertionError):
    pass


class ErrorBoolType:
    def __new__(cls):
        return ErrorBool

    def __repr__(self):
        return 'ErrorBool'

    def __bool__(self):
        raise ProgrammerIsAnIdiotError('I should not be used as a bool!')


ErrorBool = object.__new__(ErrorBoolType)


def ordered_sample(col, k):
    ''' Like random.sample, but preserving order.
    '''
    import random
    indices = random.sample(range(len(col)), k)
    indices.sort()
    return [col[i] for i in indices]


# There are more, but these are the only common ones.
_recursive_extensions = {
    '.Z',
    '.bz2',
    '.gz',
    '.xz',
}


def split_ext_harder(fn):
    base = fn
    exts = []
    while True:
        base, ext = os.path.splitext(base)
        if ext:
            exts.append(ext)
        if ext not in _recursive_extensions:
            break
    exts.reverse()
    return base, exts
