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
import collections
from .mem.sorted import SortedSet


Version = collections.namedtuple('Version', 'major minor patch')
Version.__repr__ = lambda self: 'v%d.%d.%d' % self


def parse(v):
    assert isinstance(v, str)
    assert v.count('.') == 2, v
    return Version(*[int(x) for x in v.split('.')])


INFINITY = parse('9999.0.0')


ucd_versions = SortedSet([
    parse(v)
    for v in [
        '1.0.0',
        '1.0.1',
        '1.1.5',
        '2.0.0',
        '2.1.2',
        '2.1.5',
        '2.1.8',
        '2.1.9',
        '3.0.0',
        '3.0.1',
        '3.1.0',
        '3.1.1',
        '3.2.0',
        '4.0.0',
        '4.0.1',
        '4.1.0',
        '5.0.0',
        '5.1.0',
        '5.2.0',
        '6.0.0',
        '6.1.0',
        '6.2.0',
        '6.3.0',
        '7.0.0',
        '8.0.0',
        '9.0.0',
    ]
])


# TODO cldr_versions = [ ... ]
