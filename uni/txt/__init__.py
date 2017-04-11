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
''' Text format I/O and helpers.

The text format is one of two formats (the other being xml) shipped by the
Unicode Consortium, and the only format that contains some of the data.

However, correctly accessing the text format is often unintuitive due to
the need to combine data from multiple sources, and *always* slow due to
the lack of random access. Additionally, the formats often change subtly
between versions and/or they have quirks due to backward compatibility.

Approximate data size: 42 MB, 8 MB zipped.
'''
