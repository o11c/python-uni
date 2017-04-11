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
import itertools
import os

from .. import prop_base as base, prop_alias as alias, versioning
from ..versioning import parse as v


_schemas = {}


class _ref:
    def __init__(self, n):
        self.n = n


def _fix_ref(cls_or_ref, fields):
    if isinstance(cls_or_ref, _ref):
        cls_or_ref = fields[cls_or_ref.n]
        assert isinstance(cls_or_ref, type) and issubclass(cls_or_ref, base._Property)
    return cls_or_ref


class Schema:
    def __init__(self, aliases, required, *, opt=[], repeat=[], separator=';', missing=None, comments=True, spaces=True, terminator=False, min, max=versioning.INFINITY):
        self.aliases = aliases
        self.name = aliases[0]
        self.required_fields = required
        assert required or repeat, self.name
        self.opt_fields = opt # for when a column is dropped *entirely*.
        self.repeat_fields = repeat
        assert len(repeat) <= 1
        assert not (opt and repeat), self.name
        self.separator = separator
        self.missing = missing
        self.comments = comments
        self.spaces = spaces
        self.terminator = terminator
        self.min_unicode_version = min
        self.max_unicode_version = max

    def __repr__(self):
        num_fields = '%d' % len(self.required_fields)
        if self.opt_fields:
            num_fields += '+%d?' % len(self.opt_fields)
        if self.repeat_fields:
            num_fields += '+%d*' % len(self.repeat_fields)
        return '<Schema (%s) since %r for %r>' % (num_fields, self.min_unicode_version, self.name)

    def load(self, fo, version):
        assert self.min_unicode_version <= version <= self.max_unicode_version, (fo.name, version)
        for line in fo:
            assert line[-1] == '\n' or (line, self.name, version) in (
                ('\t', 'Blocks', v('0.0.0')),
                ('U+', 'Unihan', v('0.0.0')),
            ), (fo.name, line)
            line = line[:-1]
            if line.endswith('\r') and False:
                line = line[:-1]
            assert '\r' not in line, (fo.name, line)
            if self.comments or (self.name, version) in (
                    ('UnicodeData', v('1.0.0')),
                    ('UnicodeData', v('1.0.1')),
                    ('UnicodeData', v('1.1.5')),
            ):
                line, _, comment = line.partition('#')
                line = line.rstrip()
                if not line:
                    continue
            else:
                assert '#' not in line, (fo.name, line)
            assert '"' not in line, (fo.name, line)
            fields = line.split(self.separator)
            if self.spaces or (self.name, version) in (
                    ('UnicodeData', v('1.1.5')),
                    ('UnicodeData', v('4.0.0')),
                    ('Index', v('3.2.0')),
                    ('Index', v('4.0.0')),
                    ('Index', v('4.0.1')),
                    ('Index', v('4.1.0')),
            ):
                fields = [f.strip() for f in fields]
            else:
                assert all([f == f.strip() for f in fields]), (fo.name, line)
            if self.terminator:
                assert fields[-1] == ''
                fields.pop()
            assert len(self.required_fields) <= len(fields), (fo.name, line)
            if not self.repeat_fields:
                assert len(fields) <= len(self.required_fields) + len(self.opt_fields), (fo.name, line)
            i = 0
            if self.required_fields:
                for i, c in enumerate(self.required_fields, 0):
                    c = _fix_ref(c, fields)
                    fields[i] = c.convert(fields[i]) if fields[i] != self.missing else None
                i += 1
            if self.opt_fields:
                for i, c in enumerate(self.opt_fields, i):
                    c = _fix_ref(c, fields)
                    if i == len(fields):
                        fields.append(None)
                        continue
                    fields[i] = c.convert(fields[i]) if fields[i] != self.missing else None
                i += 1
            if self.repeat_fields:
                i0 = i
                for i, c in enumerate(itertools.cycle(self.repeat_fields), i):
                    c = _fix_ref(c, fields)
                    if i == len(fields):
                        break
                    assert fields[i]
                    fields[i] = c.convert(fields[i])
                i = i0
                fields[i:] = [fields[i:]] # ensure that the result is fixed-length
                i += 1
            assert i == len(fields), (i, len(fields), fo.name, line)
            if self.name == 'UnicodeData':
                if fields[1].endswith(', First>'):
                    # See how much simpler it is when we don't have to deal with everything?
                    fields2 = [c.convert(f) if f != '' else None for c, f in zip(self.required_fields, next(fo).rstrip().split(';'))]
                    assert fields[2:] == fields2[2:]
                    fields[0] = (fields[0], fields2[0])
                    fields[1] = fields[1][:-len(', First>')] + '>'
                else:
                    fields[0] = (fields[0], fields[0])
                if fields[5] is None:
                    fields[5] = (None, None)
            yield fields


def _add_schema(*args, **kwargs):
    aliases = args[0]
    schema = Schema(*args, **kwargs)
    for name in aliases:
        _schemas[name] = schema
        globals()[name] = schema


def _init_schemas():
    _add_schema(['ArabicShaping'], [
        base.Codepoint,
        alias.X_Schematic_Name,
        alias.Joining_Type,
        alias.Joining_Group,
    ], min=v('2.0.0'))
    _add_schema(['BidiBrackets'], [
        base.Codepoint,
        alias.Bidi_Paired_Bracket,
        alias.Bidi_Paired_Bracket_Type,
    ], min=v('6.3.0'))
    _add_schema(['BidiMirroring'], [
        base.Codepoint,
        alias.Bidi_Mirroring_Glyph,
    ], min=v('3.0.1'))
    _add_schema(['Blocks'], [
        base.CodepointRange,
        alias.Block,
    ], min=v('2.0.0'))
    _add_schema(['CJKRadicals'], [
        base.RawString,
        base.Codepoint,
        base.Codepoint,
    ], min=v('5.2.0'))
    _add_schema(['CJKXREF'], [
#      Empty fields contain the single character '*'.
        base.Codepoint,
        base.RawString, # GB
        base.RawString, # Big5
        base.RawString, # CNS
        base.RawString, # JIS
        base.RawString, # KSC
        base.RawString, # EACC
        base.RawString, # CCCII
        base.RawString, # Xerox
    ], missing='*', separator='\t', min=v('1.1.0'))
    _add_schema(['CaseFolding'], [
        base.Codepoint,
        alias.X_Casefold_Status,
        alias.Case_Folding, # stored separately by status.
    ], terminator=True, min=v('3.0.1'))
    _add_schema(['CompositionExclusions'], [
        base.Codepoint,
    ], min=v('3.0.0'))
    _add_schema(['DerivedAge'], [
        base.CodepointRange,
        alias.Age,
    ], min=v('3.2.0'))
    _add_schema(['DerivedBidiClass'], [
        base.CodepointRange,
        alias.Bidi_Class,
    ], min=v('3.1.1'))
    _add_schema(['DerivedCombiningClass'], [
        base.CodepointRange,
        alias.Canonical_Combining_Class,
    ], min=v('3.1.0'))
    _add_schema(['DerivedDecompositionType'], [
        base.CodepointRange,
        alias.Decomposition_Type,
    ], min=v('3.1.0'))
    _add_schema(['DerivedEastAsianWidth'], [
        base.CodepointRange,
        alias.East_Asian_Width,
    ], min=v('3.1.0'))
    _add_schema(['DerivedGeneralCategory'], [
        base.CodepointRange,
        alias.General_Category,
    ], min=v('3.1.0'))
    _add_schema(['DerivedJoiningGroup'], [
        base.CodepointRange,
        alias.Joining_Group,
    ], min=v('3.1.0'))
    _add_schema(['DerivedJoiningType'], [
        base.CodepointRange,
        alias.Joining_Type,
    ], min=v('3.1.0'))
    _add_schema(['DerivedLineBreak'], [
        base.CodepointRange,
        alias.Line_Break,
    ], min=v('3.1.0'))
    _add_schema(['DerivedNormalizationProps', 'DerivedNormalizationProperties'], [
        base.CodepointRange,
        base.PropertyPerSe,
    ], opt=[
        _ref(1),
    ], min=v('3.1.0'))
    _add_schema(['DerivedNumericType'], [
        base.CodepointRange,
        alias.Numeric_Type,
    ], min=v('3.1.0'))
    _add_schema(['DerivedNumericValues'], [
        base.CodepointRange,
        alias.X_Approx_Numeric_Value,
    ], opt=[
        alias.Numeric_Type,
        alias.Numeric_Value,
    ], missing='', min=v('3.1.0'))
    _add_schema(['EastAsianWidth'], [
        base.CodepointRange,
        alias.East_Asian_Width,
    ], spaces=False, min=v('3.0.0'))
    _add_schema(['EmojiSources'], [
        base.CodepointSequence,
        alias.X_DoCoMo_ShiftJIS,
        alias.X_KDDI_ShiftJIS,
        alias.X_SoftBank_ShiftJIS,
    ], missing='', min=v('6.0.0'))
    _add_schema(['GraphemeBreakProperty'], [
        base.CodepointRange,
        alias.Grapheme_Cluster_Break,
    ], min=v('4.1.0'))
    _add_schema(['HangulSyllableType'], [
        base.CodepointRange,
        alias.Hangul_Syllable_Type,
    ], min=v('4.0.0'))
    _add_schema(['Index'], [
        alias.Name,
        base.CodepointGlob,
    ], separator='\t', comments=False, spaces=False, min=v('2.0.0'))
    _add_schema(['IndicPositionalCategory', 'IndicMatraCategory'], [
        base.CodepointRange,
        alias.Indic_Positional_Category,
    ], min=v('6.0.0'))
    _add_schema(['IndicSyllabicCategory'], [
        base.CodepointRange,
        alias.Indic_Syllabic_Category,
    ], min=v('6.0.0'))
    _add_schema(['Jamo'], [
        base.CodepointRange,
        alias.Jamo_Short_Name,
    ], min=v('2.0.0'))
    _add_schema(['LineBreak'], [
        base.CodepointRange,
        alias.Line_Break,
    ], spaces=False, min=v('3.0.0'))
    _add_schema(['NameAliases'], [
        base.CodepointRange,
        alias.Name_Alias,
        alias.X_Name_Alias_Type,
    ], min=v('5.0.0'))
    _add_schema(['NamedSequences', 'NamedSequencesProv'], [
        alias.Name_Alias,
        base.CodepointSequence,
    ], min=v('4.1.0'))
    _add_schema(['NormalizationCorrections'], [
        base.Codepoint,
        alias.Decomposition_Mapping,
        alias.Decomposition_Mapping,
        base.X_Version, # with a .0, unlike Age
    ], min=v('3.2.0'))
    _add_schema(['PropList', 'DerivedBinaryProperties', 'DerivedCoreProperties'], [
        base.CodepointRange,
        base.PropertyPerSe,
    ], min=v('2.0.14'))
    _add_schema(['PropertyAliases'], [
    ], repeat=[
        base.PropertyPerSe,
    ], min=v('3.2.0'))
    _add_schema(['PropertyValueAliases'], [
        base.PropertyPerSe,
    ], repeat=[
        _ref(0),
    ], min=v('3.2.0'))
    _add_schema(['ScriptExtensions'], [
        base.CodepointRange,
        alias.Script_Extensions,
    ], min=v('6.0.0'))
    _add_schema(['Scripts'], [
        base.CodepointRange,
        alias.Script,
    ], min=v('3.1.0'))
    _add_schema(['SentenceBreakProperty'], [
        base.CodepointRange,
        alias.Sentence_Break,
    ], min=v('4.1.0'))
    _add_schema(['SpecialCasing'], [
        base.Codepoint,
        alias.Lowercase_Mapping,
        alias.Titlecase_Mapping,
        alias.Uppercase_Mapping,
    ], opt=[
        alias.X_Casing_Conditions,
    ], terminator=True, min=v('2.1.3'))
    _add_schema(['StandardizedVariants'], [
        base.CodepointSequence,
        base.RawString,
        alias.X_Shaping_Environment_Set,
    ], min=v('4.0.0'))
    _add_schema(['USourceData'], [
        base.RawString, # id
        alias.X_USource_Status,
        base.RawString, # U_Codepoint or UTC-\d{5}
        base.RawString, # radical stroke count
        base.RawString, # kangxi position
        base.RawString, # ids
        base.RawString, # sources
    ], missing='', min=v('6.2.0'))
    _add_schema(['UnicodeData'], [
        base.Codepoint, # with legacy ranges
        alias.Name,
        alias.General_Category,
        alias.Canonical_Combining_Class,
        alias.Bidi_Class,
        alias.X_Decomposition_Type_and_Mapping,
        alias.Numeric_Value,
        alias.Numeric_Value,
        alias.Numeric_Value,
        alias.Bidi_Mirrored,
        alias.Unicode_1_Name,
        alias.ISO_Comment,
        alias.Simple_Uppercase_Mapping,
        alias.Simple_Lowercase_Mapping,
        alias.Simple_Titlecase_Mapping,
    ], missing='', comments=False, spaces=False, min=v('1.0.0'))
    _add_schema(['Unihan', 'Unihan_DictionaryIndices', 'Unihan_DictionaryLikeData', 'Unihan_IRGSources', 'Unihan_NumericValues', 'Unihan_OtherMappings', 'Unihan_RadicalStrokeCounts', 'Unihan_Readings', 'Unihan_Variants', 'TangutSources'], [
        base.U_Codepoint,
        base.PropertyPerSe,
        _ref(1),
    ], separator='\t', min=v('2.0.0'))
    _add_schema(['WordBreakProperty'], [
        base.CodepointRange,
        alias.Word_Break,
    ], min=v('4.1.0'))
    _schemas['BidiTest'] = None
    _schemas['BidiCharacterTest'] = None
    _schemas['GraphemeBreakTest'] = None
    _schemas['LineBreakTest'] = None
    _schemas['NamesList'] = None
    _schemas['NormalizationTest'] = None
    _schemas['Props'] = None
    _schemas['ReadMe'] = None
    _schemas['SentenceBreakTest'] = None
    _schemas['WordBreakTest'] = None
    _schemas['charts/Readme'] = None
    _schemas['charts/readme'] = None
    _schemas['ucdxml/readme'] = None
    _schemas['ucdxml/ucdxml.readme'] = None
_init_schemas()


# There are more, but these are the only common ones.
_recursive_extensions = {
    '.Z',
    '.bz2',
    '.gz',
    '.xz',
}
def split_ext_harder(fn, ext2=''):
    base, ext = os.path.splitext(fn)
    if ext in _recursive_extensions:
        return split_ext_harder(base, ext + ext2)
    return base, ext + ext2


def get_schema_info(fn):
    ''' Return a tuple (schema_name, file_extension, version)
    '''
    fn = os.path.realpath(fn)
    sn = os.path.basename(fn)
    sn, ext = split_ext_harder(sn)
    ver = ''
    if '-' in sn:
        sn, ver = sn.split('-', 1)
    if ver.count('.') != 2:
        d = os.path.dirname(fn)
        ver = os.path.basename(d)
        if ver in ('charts', 'images', 'ucdxml'):
            sn = '%s/%s' % (ver, sn)
            d = os.path.dirname(d)
            ver = os.path.basename(d)
        elif ver in ('auxiliary', 'extracted'):
            d = os.path.dirname(d)
            ver = os.path.basename(d)
        if ver == ('ucd'):
            d = os.path.dirname(d)
            ver = os.path.basename(d)
        ver = ver.replace('-Update', '.0') # DTRT for `-Update` and `-Update1`
    assert ver.count('.') == 2, fn
    ver = v(ver)
    return sn, ext, ver


_old_encodings = {
    'CaseFolding': ('iso-8859-1', v('4.1.0')),
    'Index': ('iso-8859-1', v('5.1.0')),
    'NamesList': ('iso-8859-1', v('6.2.0')),
    'Unihan': ('mac-roman', v('3.1.0')), # v3.1.0 itself is broken
    'charts/readme': ('iso-8859-1', v('5.0.0')),
    # these have no comments, thus will remain ascii forever
    'Index': ('ascii', versioning.INFINITY),
    'UnicodeData': ('ascii', versioning.INFINITY),
}
_extensions = {
    '.gif': False,
    '.html': False, # Treat HTML as binary, it has its own ways of encoding.
    '.jpg': False,
    '.pdf': False,
    '.txt.Z': False,
    '.txt.gz': False,
    '.xml': False, # Treat XML as binary, it has its own ways of encoding.
    '.zip': False,
    '.C': True,
    '.TXT': True,
    '.txt': True,
}
def get_encoding(sn, ext, ver):
    ''' Calculate the encoding for old files. New text files are all UTF-8.

    Returns a 2-tuple, the first of which is one of:
      * None: for files that should be opened as binary (e.g. PDF).
      * 'ascii'
      * 'utf-8'
      * 'iso-8859-1': (some old files)
      * 'mac-roman': (some old files)
    and the second of which is one of:
      * 'strict' (for most files)
      * 'replace' (for one broken old file)
    '''
    errors = 'strict'
    if (sn, ext, ver) == ('Unihan', '.txt', v('3.1.0')):
        errors = 'replace'
    x = _extensions.get(ext)
    assert x is not None, (sn, ext, ver)
    if not x:
        return None, errors
    # 9.0.0 added utf-8 to the comments in all files that have them.
    enc, fix_ver = _old_encodings.get(sn, ('ascii', v('9.0.0')))
    if ver < fix_ver:
        return enc, errors
    return 'utf-8', errors


def main_dump_file(fn):
    sn, ext, ver = get_schema_info(fn)
    encoding, errors = get_encoding(sn, ext, ver)
    print('#', sn, ver, encoding)
    if 1: return
    if encoding is None:
        return
    if sn.startswith('diff') or ext.lower() != '.txt':
        return
    schema = _schemas[sn]
    if schema is None:
        return
    with open(fn, encoding=encoding, errors=errors, newline='') as fo:
        for fields in schema.load(fo, ver):
            print(*[repr(f) for f in fields])


def main(files=None, exe=None):
    import sys
    if files is None:
        files = sys.argv[1:]
    if exe is None:
        exe = sys.argv[0]
    if not files or any([fn.startswith('-') for fn in files]):
        sys.exit('Usage: %s ucd/*.txt' % exe)
    for fn in files:
        main_dump_file(fn)


if __name__ == '__main__':
    main()
