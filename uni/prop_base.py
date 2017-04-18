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
''' Fixed classes used to support uni.alias and its dynamic classes.
'''

import decimal, fractions
from functools import partial
import re
import unicodedata # just for normalize('NFD', ...) during regexes

from . import _util, versioning


def _casefold(s):
    return s.casefold().replace(' ', '_').replace('-', '_')


def _split(s):
    rv = s.split()
    assert set(rv) == set(s.split(' ')) - {''}
    return rv


class _Property:
    ''' Base of all exposed property classes.

        By default, this class is not instantiable.
    '''
    def __new__(cls, *args, **kwargs):
        if not issubclass(cls, _InstantiableProperty):
            raise NotImplementedError('most property classes are not instantiable') # pragma: no cover
        return object.__new__(cls)

    def __init__(self):
        super().__init__()

    @classmethod
    def check(cls, val):
        raise NotImplementedError('Needs to be implemented in subclasses!') # pragma: no cover

    @classmethod
    def convert(cls, val):
        raise NotImplementedError('Needs to be implemented in subclasses!') # pragma: no cover


class List(_Property):
    ''' Properties whose values are a list of 0 or more of another property.

        New subclasses are created dynamically by make_list.
    '''
    @classmethod
    def check(cls, val):
        assert issubclass(cls.element, _Property)
        assert isinstance(val, list)
        for v in val:
            cls.element.check(v)
        return val

    @classmethod
    def convert(cls, val):
        assert issubclass(cls.element, _Property)
        assert isinstance(val, str)
        return cls.check([cls.element.convert(v) for v in _split(val)])


# TODO actually optimize using bitsets when possible.
class Set(_Property):
    ''' Properties whose values are a set of 0 or more of another property.

        New subclasses are created dynamically by make_set.
    '''
    @classmethod
    def check(cls, val):
        assert issubclass(cls.element, _Property)
        assert isinstance(val, set)
        for v in val:
            cls.element.check(v)
        return val

    @classmethod
    def convert(cls, val):
        assert issubclass(cls.element, _Property)
        assert isinstance(val, str)
        rvl = [cls.element.convert(v) for v in _split(val)]
        rv = set(rvl)
        assert len(rv) == len(rvl)
        return cls.check(rv)


class TaggedItem(_Property):
    ''' Properties whose values are of the form `<tag> payload`.

        New subclasses are created dynamically by make_tagged_item.
    '''
    @classmethod
    def check(cls, val):
        assert issubclass(cls.tag, _Property)
        assert issubclass(cls.payload, _Property)
        assert isinstance(val, tuple)
        if val[0] is not None:
            cls.tag.check(val[0])
        cls.payload.check(val[1])
        return val

    @classmethod
    def convert(cls, val):
        assert issubclass(cls.tag, _Property)
        assert issubclass(cls.payload, _Property)
        assert isinstance(val, str)
        if ' ' in val:
            t, p = val.split(' ', 1)
            if t.startswith('<') and t.endswith('>'):
                t = t[1:-1]
                return cls.check((cls.tag.convert(t), cls.payload.convert(p)))
        return cls.check((None, cls.payload.convert(val)))


class _EnumLikeProperty(_Property):
    ''' Base for properties with a fixed number of values.
    '''
    @classmethod
    def check(cls, val):
        #assert isinstance(val, cls)
        assert val in cls.value_set, val
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        by_name = cls.value_by_name
        val = _casefold(val)
        assert val in by_name, (cls.__name__, val)
        return cls.check(by_name[val.casefold()])


class PropertyPerSe(_EnumLikeProperty):
    ''' Property whose values are the set of all properties.
    '''
    # these are filled in by _make_class
    value_by_name = {}
    value_set = set()
    value_list = []


class _InstantiableProperty(_EnumLikeProperty):
    ''' Base for properties whose values are instances thereof.

        New subclasses are created dynamically by make_enum.
    '''
    def __init__(self, index, aliases, *, manual_index):
        super().__init__()
        self.value_aliases = aliases
        self.short_value_name = aliases[manual_index + 0]
        self.long_value_name = aliases[manual_index + (len(aliases) > manual_index + 1)]

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__, self.long_value_name)


class Enum(_InstantiableProperty):
    ''' Property whose values rarely expand in future versions.

        As a result, they can meaningfully be used with bitsets.
    '''
    def __init__(self, index, aliases, *, manual_index):
        super().__init__(index, aliases, manual_index=manual_index)
        if manual_index:
            index = int(aliases[0])
        self.index = index


class Catalog(_InstantiableProperty):
    ''' Property whose values commonly expand in future versions.

        As a result, they *cannot* meaningfully be used with bitsets.
    '''


class Bool(_EnumLikeProperty):
    ''' Property whose values are true/false.
    '''
    value_by_name = {
        k.casefold(): v
        for keys, v in [
            (('N', 'No', 'F', 'False'), False),
            (('Y', 'Yes', 'T', 'True'), True),
        ]
        for k in keys
    }
    value_set = set(value_by_name.values())
    value_list = [False, True]


class Int(_Property):
    ''' Property whose values are an integer, encoded in base 10.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, int)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(int(val))


class Rational(_Property):
    ''' Property whose values are a ratio of integers, encoded with a slash.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, fractions.Fraction)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(fractions.Fraction(val))


class Decimal(_Property):
    ''' Property whose values are a ratio of integers, encoded as decimal.

        May be inexact.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, decimal.Decimal)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(decimal.Decimal(val))


class RawString(_Property):
    ''' Property whose values are unencoded strings.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, str)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(val)


class X_Version(_Property):
    ''' Property whose values are full x.y.z versions.

        For x.y versions, use prop_alias.Age.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, versioning.Version)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        val.count('.') == 2
        return cls.check(versioning.parse(val))


class Regex(_Property):
    ''' Property whose values limited by a regex.
    '''
    @classmethod
    def check(cls, val):
        val = unicodedata.normalize('NFD', val)
        assert isinstance(val, str) and cls.regex.fullmatch(val), (cls.__name__, cls.regex, val)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(val)


class Codepoint(_Property):
    ''' Property whose values are single codepoints.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, int)
        assert 0 <= val < 0x110000
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        assert 4 <= len(val) <= 6, val
        return cls.check(int(val, 16))


class CodepointGlob(_Property):
    ''' Product of some sadist's imagination.
    '''
    known_globs = {
        '*FFFE': [x * 0x10000 + 0xFFFE for x in range(0, 0x10 + 1)],
        '*FFFF': [x * 0x10000 + 0xFFFE for x in range(0, 0x10 + 1)],
        'FDD*': [0xFDD0 + x for x in range(0xF + 1)],
        'FDE*': [0xFDE0 + x for x in range(0xF + 1)],
    }

    @classmethod
    def check(cls, val):
        assert isinstance(val, list)
        for v in val:
            Codepoint.check(v)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        if '*' in val:
            return cls.known_globs[val]
        return cls.check([Codepoint.convert(val)])


class CodepointRange(_Property):
    ''' Property whose values are ranges of codepoints.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, tuple)
        assert len(val) == 2
        assert isinstance(Codepoint.check(val[0]), int)
        assert isinstance(Codepoint.check(val[1]), int)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        if '..' in val:
            low, high = val.split('..')
            assert low != high
        else:
            low = high = val
        return cls.check((Codepoint.convert(low), Codepoint.convert(high)))


class CodepointSequence(_Property):
    ''' Property whose values are strings, encoded as a sequence of codepoints.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, str)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        return cls.check(''.join([chr(Codepoint.convert(cp)) for cp in _split(val)]))


class U_Codepoint(_Property):
    ''' Property whose values are single codepoints, encoded with U+ out front.
    '''
    @classmethod
    def check(cls, val):
        assert isinstance(val, int)
        return val

    @classmethod
    def convert(cls, val):
        assert isinstance(val, str)
        assert val.startswith('U+'), val
        return cls.check(Codepoint.convert(val[2:]))


def unique_aliases(aliases, *, casefold):
    aliases = list(aliases)
    aliases_folded = [a.casefold() for a in aliases]
    seen_orig = set()
    seen_fold = set()
    remove = []
    for i, a in enumerate(aliases):
        f = a.casefold()
        if a in seen_orig:
            assert (i == 1 and len(set(aliases_folded)) == 1) or (i == 2 and len(aliases) == 3 and a.startswith('CCC')), a
            remove.append(i)
        elif f in seen_fold:
            assert f in aliases_folded[:2], f
            if casefold:
                remove.append(i)
        seen_orig.add(a)
        seen_fold.add(f)
    while remove:
        aliases.pop(remove.pop())
    return aliases


def _make_aliases(g, aliases, cls, *, casefold):
    for a in unique_aliases(aliases, casefold=casefold):
        assert a not in g, a
        if casefold:
            a = a.casefold()
        g[a] = cls


def _make_class(g, aliases, cls, *, doc='', status, scope, deprecated=None, stabilized=None, obsolete=None, min, max=versioning.INFINITY):
    # TODO make doc mandatory
    cls.__module__ = g['__name__']
    cls.__doc__ = doc
    cls.status = status
    cls.scope = scope
    cls.min_unicode_version = min
    cls.max_unicode_version = max
    cls.aliases = aliases
    cls.short_name = aliases[0]
    cls.long_name = aliases[len(aliases) > 1]
    cls.__qualname__ = cls.__name__ = cls.long_name
    _make_aliases(g, aliases, cls, casefold=False)
    g['__all__'].append(cls.__name__)
    public_aliases = [a for a in aliases if not a.startswith('X_')]
    if public_aliases:
        _make_aliases(PropertyPerSe.value_by_name, public_aliases, cls, casefold=True)
        #_make_aliases(_util.ClassDict(PropertyPerSe), public_aliases, cls, casefold=False)
        PropertyPerSe.value_set.add(cls)
        PropertyPerSe.value_list.append(cls)


def _make_subclass(g, aliases, cls, **kwargs):
    class C(cls):
        pass
    _make_class(g, aliases, C, **kwargs)


def make_list(g, aliases, elem, **kwargs):
    class L(List):
        element = elem
    _make_class(g, aliases, L, **kwargs)


def make_set(g, aliases, elem, **kwargs):
    class S(Set):
        element = elem
    _make_class(g, aliases, S, **kwargs)


def make_tagged_item(g, aliases, tag_, payload_, **kwargs):
    class TI(TaggedItem):
        tag = tag_
        payload = payload_
    _make_class(g, aliases, TI, **kwargs)


def make_enum(g, aliases, values, *, catalog=False, manual_index=False, **kwargs):
    class E(Catalog if catalog else Enum):
        value_by_name = {}
        value_set = set()
        value_list = []
    _make_class(g, aliases, E, **kwargs)
    for i, pvas in enumerate(values):
        v = E(i, pvas, manual_index=manual_index)
        E.value_list.append(v)
        _make_aliases(E.value_by_name, pvas, v, casefold=True)
        _make_aliases(_util.ClassDict(E), pvas, v, casefold=False)
    E.value_set = set(E.value_by_name.values())


def make_re(g, aliases, regexp, sep, **kwargs):
    class R(Regex):
        regex = re.compile(regexp)
    elem_aliases = aliases if sep is None else ['X_Element_of_' + aliases[len(aliases) > 1]]
    _make_class(g, elem_aliases, R, **kwargs)
    if sep is not None:
        assert sep == ' '
        make_list(g, aliases, R, **kwargs)


make_bool = partial(_make_subclass, cls=Bool)
make_int = partial(_make_subclass, cls=Int)
make_rational = partial(_make_subclass, cls=Rational)
make_decimal = partial(_make_subclass, cls=Decimal)
make_raw = partial(_make_subclass, cls=RawString)
make_code = partial(_make_subclass, cls=Codepoint)
make_code_range = partial(_make_subclass, cls=CodepointRange)
make_code_seq = partial(_make_subclass, cls=CodepointSequence)
make_u_code = partial(_make_subclass, cls=U_Codepoint)
