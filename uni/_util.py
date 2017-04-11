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
