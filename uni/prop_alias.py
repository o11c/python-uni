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
# Contents of PropertyAliases.txt and PropertyValueAliases.txt are
# hard-coded here, then just checked during UCD loading.
#
# Also other internal stuff! This turns out to be really useful.
# (there's no reason a "property" has to apply to a single codepoint)

from . import prop_base as prop, versioning
from .versioning import parse as v

__all__ = []


def _init_classes():
    g = globals()

    # implementation internals (names all of the form X_*)
    prop.make_enum(g, ['X_Property_Status'], [
        ('Normative',),
        ('Informative',),
        ('Normative_and_Informative',),
        ('Contributory',),
        ('Provisional',),
        #('Deprecated',),
    ], status=None, scope=None, min=versioning.INFINITY)
    if 1:
        status = X_Property_Status
        Normative = status.Normative
        Informative = status.Informative
        Normative_and_Informative = status.Normative_and_Informative
        Provisional = status.Provisional
    prop.make_enum(g, ['X_Property_Category', 'X_Property_Scope'], [
        ('General',),
        ('Case',),
        ('Numeric_Values', 'Numeric'),
        ('Normalization',),
        ('Shaping_and_Rendering',),
        ('Bidirectional',),
        ('Identifiers',),
        ('CJK',),
        ('Miscellaneous',),
        ('Contributory',),
        ('Dictionary_Indices', 'CJK_Dictionary_Indices'),
        ('Dictionary_like_Data', 'CJK_Dictionary_like_Data'),
        ('IRG_Sources', 'CJK_IRG_Sources'),
        ('Other_Mappings', 'CJK_Other_Mappings'),
        ('Radical_Stroke_Counts', 'CJK_Radical_Stroke_Counts'),
        ('Readings', 'CJK_Readings'),
        ('Variants', 'CJK_Variants'),
    ], status=None, scope=None, min=versioning.INFINITY)
    if 1:
        scope = X_Property_Category
        General = scope.General
        Case = scope.Case
        Numeric = scope.Numeric
        Normalization = scope.Normalization
        Shaping_and_Rendering = scope.Shaping_and_Rendering
        Bidirectional = scope.Bidirectional
        Identifiers = scope.Identifiers
        CJK = scope.CJK
        Miscellaneous = scope.Miscellaneous
        Dictionary_Indices = scope.Dictionary_Indices
        Dictionary_like_Data = scope.Dictionary_like_Data
        IRG_Sources = scope.IRG_Sources
        Other_Mappings = scope.Other_Mappings
        Radical_Stroke_Counts = scope.Radical_Stroke_Counts
        Readings = scope.Readings
        Variants = scope.Variants
    prop.make_enum(g, ['X_Named_Unicode_Algorithm'], [
        # All of these should be implemented as code.
        # (there are *also* properties-for-strings)
        ('Canonical_Ordering',),
        ('Canonical_Composition',),
        ('Normalization',),
        ('Hangul_Syllable_Composition',),
        ('Hangul_Syllable_Decomposition',),
        ('Hangul_Syllable_Name_Generation',),
        ('Default_Case_Conversion',),
        ('Default_Case_Detection',),
        ('Default_Caseless_Matching',),
        ('Bidirectional_Algorithm',),
        ('Line_Breaking_Algorithm',),
        ('Character_Segmentation',),
        ('Word_Segmentation',),
        ('Sentence_Segmentation',),
        ('Hangul_Syllable_Boundary_Determination',),
        ('Default_Identifier_Determination',),
        ('Alternative_Identifier_Determination',),
        ('Pattern_Syntax_Determination',),
        ('Identifier_Normalization',),
        ('Identifier_Case_Folding',),
        ('Standard_Compression_Scheme_for_Unicode',),
        ('Unicode_Collation_Algorithm',),
    ], status=None, scope=None, min=versioning.INFINITY)
    prop.make_raw(g, ['X_Schematic_Name'], status=None, scope=Shaping_and_Rendering, min=versioning.INFINITY)
    prop.make_enum(g, ['X_Shaping_Environment'], [
        ('isolate',),
        ('initial',),
        ('medial',),
        ('final',),
    ], status=None, scope=Shaping_and_Rendering, min=versioning.INFINITY)
    prop.make_set(g, ['X_Shaping_Environment_Set'], X_Shaping_Environment, status=None, scope=Shaping_and_Rendering, min=versioning.INFINITY)
    prop.make_enum(g, ['X_Casefold_Status'], [
        ('C', 'Common'),
        ('F', 'Full'),
        ('S', 'Simple'),
        ('T', 'Turkic'),
    ], status=None, scope=Case, min=versioning.INFINITY)
    prop.make_enum(g, ['X_Name_Alias_Type'], [
        ('correction',),
        ('control',),
        ('alternate',),
        ('figment',),
        ('abbreviation',),
    ], status=None, scope=General, min=versioning.INFINITY)
    prop.make_decimal(g, ['X_Approx_Numeric_Value'], status=None, scope=Numeric, min=v('3.1.0'))
    prop.make_re(g, ['X_DoCoMo_ShiftJIS'], r'[0-9A-F]{4}', None, status=None, scope=None, min=versioning.INFINITY)
    prop.make_re(g, ['X_KDDI_ShiftJIS'], r'[0-9A-F]{4}', None, status=None, scope=None, min=versioning.INFINITY)
    prop.make_re(g, ['X_SoftBank_ShiftJIS'], r'[0-9A-F]{4}', None, status=None, scope=None, min=versioning.INFINITY)
    prop.make_enum(g, ['X_Casing_Condition_Part'], [
        ('After_I',),
        ('After_Soft_Dotted',),
        ('Final_Sigma',),
        ('More_Above',),
        ('Not_Before_Dot',),
        ('az',),
        ('lt',),
        ('tr',),
    ], status=None, scope=Case, min=versioning.INFINITY)
    prop.make_set(g, ['X_Casing_Conditions'], X_Casing_Condition_Part, status=None, scope=Case, min=versioning.INFINITY)
    prop.make_re(g, ['X_USource_Status'], r'[CDEFHNUVWX]|UNC-201[35]|UK-2015|UTC-[0-9]{5}|UCI-[0-9]{5}', None, status=None, scope=CJK, min=versioning.INFINITY) # enum-like, but also arbitrary values
    # Must be after dm and dt
    #prop.make_tagged_item(g, ['X_Decomposition_Type_and_Mapping'], ...)
    # Numeric Properties
    # (unihan properties moved to bottom)
    prop.make_rational(g, ['nv', 'Numeric_Value'], status=Normative_and_Informative, scope=Numeric, min=v('1.0.0'))
    # String Properties
    prop.make_code_seq(g, ['cf', 'Case_Folding'], status=Normative, scope=Case, min=v('3.0.1')) # special: sometimes only C or F, not S or T
    prop.make_code_seq(g, ['dm', 'Decomposition_Mapping'], status=Normative, scope=Case, min=v('1.0.0')) # stored in file with <dt> ahead
    prop.make_code_seq(g, ['FC_NFKC', 'FC_NFKC_Closure'], status=Normative, scope=Case, deprecated=v('6.0.0'), min=v('3.2.0'))
    prop.make_code_seq(g, ['lc', 'Lowercase_Mapping'], status=Informative, scope=Case, min=v('2.1.3'))
    prop.make_code_seq(g, ['NFKC_CF', 'NFKC_Casefold'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_code(g, ['scf', 'Simple_Case_Folding', 'sfc'], status=Normative, scope=Case, min=v('3.0.1'))
    prop.make_code(g, ['slc', 'Simple_Lowercase_Mapping'], status=Normative, scope=Case, min=v('1.0.0'))
    prop.make_code(g, ['stc', 'Simple_Titlecase_Mapping'], status=Normative, scope=Case, min=v('1.0.0'))
    prop.make_code(g, ['suc', 'Simple_Uppercase_Mapping'], status=Normative, scope=Case, min=v('1.0.0'))
    prop.make_code_seq(g, ['tc', 'Titlecase_Mapping'], status=Informative, scope=Case, min=v('2.1.3'))
    prop.make_code_seq(g, ['uc', 'Uppercase_Mapping'], status=Informative, scope=Case, min=v('2.1.3'))
    # Miscellaneous Properties
    # (unihan properties moved to bottom)
    prop.make_code(g, ['bmg', 'Bidi_Mirroring_Glyph'], status=Informative, scope=Bidirectional, min=v('3.0.1'))
    prop.make_code(g, ['bpb', 'Bidi_Paired_Bracket'], status=Normative, scope=Bidirectional, min=v('6.3.0'))
    prop.make_raw(g, ['isc', 'ISO_Comment'], status=Normative, scope=Miscellaneous, deprecated=v('6.0.0'), stabilized=v('6.0.0'), obsolete=v('5.2.0'), min=v('1.0.0'))
    prop.make_enum(g, ['JSN', 'Jamo_Short_Name'], [
        # This special case is not listed in PropertyValueAliases.txt,
        # but is used in the Jamo file.
        ('', ''),

        ('A', 'A'),
        ('AE', 'AE'),
        ('B', 'B'),
        ('BB', 'BB'),
        ('BS', 'BS'),
        ('C', 'C'),
        ('D', 'D'),
        ('DD', 'DD'),
        ('E', 'E'),
        ('EO', 'EO'),
        ('EU', 'EU'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('GS', 'GS'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
        ('JJ', 'JJ'),
        ('K', 'K'),
        ('L', 'L'),
        ('LB', 'LB'),
        ('LG', 'LG'),
        ('LH', 'LH'),
        ('LM', 'LM'),
        ('LP', 'LP'),
        ('LS', 'LS'),
        ('LT', 'LT'),
        ('M', 'M'),
        ('N', 'N'),
        ('NG', 'NG'),
        ('NH', 'NH'),
        ('NJ', 'NJ'),
        ('O', 'O'),
        ('OE', 'OE'),
        ('P', 'P'),
        ('R', 'R'),
        ('S', 'S'),
        ('SS', 'SS'),
        ('T', 'T'),
        ('U', 'U'),
        ('WA', 'WA'),
        ('WAE', 'WAE'),
        ('WE', 'WE'),
        ('WEO', 'WEO'),
        ('WI', 'WI'),
        ('YA', 'YA'),
        ('YAE', 'YAE'),
        ('YE', 'YE'),
        ('YEO', 'YEO'),
        ('YI', 'YI'),
        ('YO', 'YO'),
        ('YU', 'YU'),
    ], status=status.Contributory, scope=scope.Contributory, min=v('2.0.0'))
    prop.make_raw(g, ['na', 'Name'], status=Normative, scope=General, min=v('2.0.0'))
    prop.make_raw(g, ['na1', 'Unicode_1_Name'], status=Informative, scope=General, obsolete=v('6.2.0'), min=v('1.0.0'))
    prop.make_raw(g, ['Name_Alias', 'Name_Alias'], status=Normative, scope=General, min=v('5.0.0'))
    # Moved to be *after* Script
    #prop.make_set(g, ['scx', 'Script_Extensions'], Script, ...)
    # Catalog Properties
    prop.make_enum(g, ['age', 'Age'], [
        ('1.1', 'V1_1'),
        ('2.0', 'V2_0'),
        ('2.1', 'V2_1'),
        ('3.0', 'V3_0'),
        ('3.1', 'V3_1'),
        ('3.2', 'V3_2'),
        ('4.0', 'V4_0'),
        ('4.1', 'V4_1'),
        ('5.0', 'V5_0'),
        ('5.1', 'V5_1'),
        ('5.2', 'V5_2'),
        ('6.0', 'V6_0'),
        ('6.1', 'V6_1'),
        ('6.2', 'V6_2'),
        ('6.3', 'V6_3'),
        ('7.0', 'V7_0'),
        ('8.0', 'V8_0'),
        ('9.0', 'V9_0'),
        ('NA', 'Unassigned'),
    ], catalog=True, status=Normative_and_Informative, scope=General, min=v('3.2.0'))
    prop.make_enum(g, ['blk', 'Block'], [
        ('Adlam', 'Adlam'),
        ('Aegean_Numbers', 'Aegean_Numbers'),
        ('Ahom', 'Ahom'),
        ('Alchemical', 'Alchemical_Symbols'),
        ('Alphabetic_PF', 'Alphabetic_Presentation_Forms'),
        ('Anatolian_Hieroglyphs', 'Anatolian_Hieroglyphs'),
        ('Ancient_Greek_Music', 'Ancient_Greek_Musical_Notation'),
        ('Ancient_Greek_Numbers', 'Ancient_Greek_Numbers'),
        ('Ancient_Symbols', 'Ancient_Symbols'),
        ('Arabic', 'Arabic'),
        ('Arabic_Ext_A', 'Arabic_Extended_A'),
        ('Arabic_Math', 'Arabic_Mathematical_Alphabetic_Symbols'),
        ('Arabic_PF_A', 'Arabic_Presentation_Forms_A', 'Arabic_Presentation_Forms-A'),
        ('Arabic_PF_B', 'Arabic_Presentation_Forms_B'),
        ('Arabic_Sup', 'Arabic_Supplement'),
        ('Armenian', 'Armenian'),
        ('Arrows', 'Arrows'),
        ('ASCII', 'Basic_Latin'),
        ('Avestan', 'Avestan'),
        ('Balinese', 'Balinese'),
        ('Bamum', 'Bamum'),
        ('Bamum_Sup', 'Bamum_Supplement'),
        ('Bassa_Vah', 'Bassa_Vah'),
        ('Batak', 'Batak'),
        ('Bengali', 'Bengali'),
        ('Bhaiksuki', 'Bhaiksuki'),
        ('Block_Elements', 'Block_Elements'),
        ('Bopomofo', 'Bopomofo'),
        ('Bopomofo_Ext', 'Bopomofo_Extended'),
        ('Box_Drawing', 'Box_Drawing'),
        ('Brahmi', 'Brahmi'),
        ('Braille', 'Braille_Patterns'),
        ('Buginese', 'Buginese'),
        ('Buhid', 'Buhid'),
        ('Byzantine_Music', 'Byzantine_Musical_Symbols'),
        ('Carian', 'Carian'),
        ('Caucasian_Albanian', 'Caucasian_Albanian'),
        ('Chakma', 'Chakma'),
        ('Cham', 'Cham'),
        ('Cherokee', 'Cherokee'),
        ('Cherokee_Sup', 'Cherokee_Supplement'),
        ('CJK', 'CJK_Unified_Ideographs'),
        ('CJK_Compat', 'CJK_Compatibility'),
        ('CJK_Compat_Forms', 'CJK_Compatibility_Forms'),
        ('CJK_Compat_Ideographs', 'CJK_Compatibility_Ideographs'),
        ('CJK_Compat_Ideographs_Sup', 'CJK_Compatibility_Ideographs_Supplement'),
        ('CJK_Ext_A', 'CJK_Unified_Ideographs_Extension_A'),
        ('CJK_Ext_B', 'CJK_Unified_Ideographs_Extension_B'),
        ('CJK_Ext_C', 'CJK_Unified_Ideographs_Extension_C'),
        ('CJK_Ext_D', 'CJK_Unified_Ideographs_Extension_D'),
        ('CJK_Ext_E', 'CJK_Unified_Ideographs_Extension_E'),
        ('CJK_Radicals_Sup', 'CJK_Radicals_Supplement'),
        ('CJK_Strokes', 'CJK_Strokes'),
        ('CJK_Symbols', 'CJK_Symbols_And_Punctuation'),
        ('Compat_Jamo', 'Hangul_Compatibility_Jamo'),
        ('Control_Pictures', 'Control_Pictures'),
        ('Coptic', 'Coptic'),
        ('Coptic_Epact_Numbers', 'Coptic_Epact_Numbers'),
        ('Counting_Rod', 'Counting_Rod_Numerals'),
        ('Cuneiform', 'Cuneiform'),
        ('Cuneiform_Numbers', 'Cuneiform_Numbers_And_Punctuation'),
        ('Currency_Symbols', 'Currency_Symbols'),
        ('Cypriot_Syllabary', 'Cypriot_Syllabary'),
        ('Cyrillic', 'Cyrillic'),
        ('Cyrillic_Ext_A', 'Cyrillic_Extended_A'),
        ('Cyrillic_Ext_B', 'Cyrillic_Extended_B'),
        ('Cyrillic_Ext_C', 'Cyrillic_Extended_C'),
        ('Cyrillic_Sup', 'Cyrillic_Supplement', 'Cyrillic_Supplementary'),
        ('Deseret', 'Deseret'),
        ('Devanagari', 'Devanagari'),
        ('Devanagari_Ext', 'Devanagari_Extended'),
        ('Diacriticals', 'Combining_Diacritical_Marks'),
        ('Diacriticals_Ext', 'Combining_Diacritical_Marks_Extended'),
        ('Diacriticals_For_Symbols', 'Combining_Diacritical_Marks_For_Symbols', 'Combining_Marks_For_Symbols'),
        ('Diacriticals_Sup', 'Combining_Diacritical_Marks_Supplement'),
        ('Dingbats', 'Dingbats'),
        ('Domino', 'Domino_Tiles'),
        ('Duployan', 'Duployan'),
        ('Early_Dynastic_Cuneiform', 'Early_Dynastic_Cuneiform'),
        ('Egyptian_Hieroglyphs', 'Egyptian_Hieroglyphs'),
        ('Elbasan', 'Elbasan'),
        ('Emoticons', 'Emoticons'),
        ('Enclosed_Alphanum', 'Enclosed_Alphanumerics'),
        ('Enclosed_Alphanum_Sup', 'Enclosed_Alphanumeric_Supplement'),
        ('Enclosed_CJK', 'Enclosed_CJK_Letters_And_Months'),
        ('Enclosed_Ideographic_Sup', 'Enclosed_Ideographic_Supplement'),
        ('Ethiopic', 'Ethiopic'),
        ('Ethiopic_Ext', 'Ethiopic_Extended'),
        ('Ethiopic_Ext_A', 'Ethiopic_Extended_A'),
        ('Ethiopic_Sup', 'Ethiopic_Supplement'),
        ('Geometric_Shapes', 'Geometric_Shapes'),
        ('Geometric_Shapes_Ext', 'Geometric_Shapes_Extended'),
        ('Georgian', 'Georgian'),
        ('Georgian_Sup', 'Georgian_Supplement'),
        ('Glagolitic', 'Glagolitic'),
        ('Glagolitic_Sup', 'Glagolitic_Supplement'),
        ('Gothic', 'Gothic'),
        ('Grantha', 'Grantha'),
        ('Greek', 'Greek_And_Coptic'),
        ('Greek_Ext', 'Greek_Extended'),
        ('Gujarati', 'Gujarati'),
        ('Gurmukhi', 'Gurmukhi'),
        ('Half_And_Full_Forms', 'Halfwidth_And_Fullwidth_Forms'),
        ('Half_Marks', 'Combining_Half_Marks'),
        ('Hangul', 'Hangul_Syllables'),
        ('Hanunoo', 'Hanunoo'),
        ('Hatran', 'Hatran'),
        ('Hebrew', 'Hebrew'),
        ('High_PU_Surrogates', 'High_Private_Use_Surrogates'),
        ('High_Surrogates', 'High_Surrogates'),
        ('Hiragana', 'Hiragana'),
        ('IDC', 'Ideographic_Description_Characters'),
        ('Ideographic_Symbols', 'Ideographic_Symbols_And_Punctuation'),
        ('Imperial_Aramaic', 'Imperial_Aramaic'),
        ('Indic_Number_Forms', 'Common_Indic_Number_Forms'),
        ('Inscriptional_Pahlavi', 'Inscriptional_Pahlavi'),
        ('Inscriptional_Parthian', 'Inscriptional_Parthian'),
        ('IPA_Ext', 'IPA_Extensions'),
        ('Jamo', 'Hangul_Jamo'),
        ('Jamo_Ext_A', 'Hangul_Jamo_Extended_A'),
        ('Jamo_Ext_B', 'Hangul_Jamo_Extended_B'),
        ('Javanese', 'Javanese'),
        ('Kaithi', 'Kaithi'),
        ('Kana_Sup', 'Kana_Supplement'),
        ('Kanbun', 'Kanbun'),
        ('Kangxi', 'Kangxi_Radicals'),
        ('Kannada', 'Kannada'),
        ('Katakana', 'Katakana'),
        ('Katakana_Ext', 'Katakana_Phonetic_Extensions'),
        ('Kayah_Li', 'Kayah_Li'),
        ('Kharoshthi', 'Kharoshthi'),
        ('Khmer', 'Khmer'),
        ('Khmer_Symbols', 'Khmer_Symbols'),
        ('Khojki', 'Khojki'),
        ('Khudawadi', 'Khudawadi'),
        ('Lao', 'Lao'),
        ('Latin_1_Sup', 'Latin_1_Supplement', 'Latin_1'),
        ('Latin_Ext_A', 'Latin_Extended_A'),
        ('Latin_Ext_Additional', 'Latin_Extended_Additional'),
        ('Latin_Ext_B', 'Latin_Extended_B'),
        ('Latin_Ext_C', 'Latin_Extended_C'),
        ('Latin_Ext_D', 'Latin_Extended_D'),
        ('Latin_Ext_E', 'Latin_Extended_E'),
        ('Lepcha', 'Lepcha'),
        ('Letterlike_Symbols', 'Letterlike_Symbols'),
        ('Limbu', 'Limbu'),
        ('Linear_A', 'Linear_A'),
        ('Linear_B_Ideograms', 'Linear_B_Ideograms'),
        ('Linear_B_Syllabary', 'Linear_B_Syllabary'),
        ('Lisu', 'Lisu'),
        ('Low_Surrogates', 'Low_Surrogates'),
        ('Lycian', 'Lycian'),
        ('Lydian', 'Lydian'),
        ('Mahajani', 'Mahajani'),
        ('Mahjong', 'Mahjong_Tiles'),
        ('Malayalam', 'Malayalam'),
        ('Mandaic', 'Mandaic'),
        ('Manichaean', 'Manichaean'),
        ('Marchen', 'Marchen'),
        ('Math_Alphanum', 'Mathematical_Alphanumeric_Symbols'),
        ('Math_Operators', 'Mathematical_Operators'),
        ('Meetei_Mayek', 'Meetei_Mayek'),
        ('Meetei_Mayek_Ext', 'Meetei_Mayek_Extensions'),
        ('Mende_Kikakui', 'Mende_Kikakui'),
        ('Meroitic_Cursive', 'Meroitic_Cursive'),
        ('Meroitic_Hieroglyphs', 'Meroitic_Hieroglyphs'),
        ('Miao', 'Miao'),
        ('Misc_Arrows', 'Miscellaneous_Symbols_And_Arrows'),
        ('Misc_Math_Symbols_A', 'Miscellaneous_Mathematical_Symbols_A'),
        ('Misc_Math_Symbols_B', 'Miscellaneous_Mathematical_Symbols_B'),
        ('Misc_Pictographs', 'Miscellaneous_Symbols_And_Pictographs'),
        ('Misc_Symbols', 'Miscellaneous_Symbols'),
        ('Misc_Technical', 'Miscellaneous_Technical'),
        ('Modi', 'Modi'),
        ('Modifier_Letters', 'Spacing_Modifier_Letters'),
        ('Modifier_Tone_Letters', 'Modifier_Tone_Letters'),
        ('Mongolian', 'Mongolian'),
        ('Mongolian_Sup', 'Mongolian_Supplement'),
        ('Mro', 'Mro'),
        ('Multani', 'Multani'),
        ('Music', 'Musical_Symbols'),
        ('Myanmar', 'Myanmar'),
        ('Myanmar_Ext_A', 'Myanmar_Extended_A'),
        ('Myanmar_Ext_B', 'Myanmar_Extended_B'),
        ('Nabataean', 'Nabataean'),
        ('NB', 'No_Block'),
        ('New_Tai_Lue', 'New_Tai_Lue'),
        ('Newa', 'Newa'),
        ('NKo', 'NKo'),
        ('Number_Forms', 'Number_Forms'),
        ('OCR', 'Optical_Character_Recognition'),
        ('Ogham', 'Ogham'),
        ('Ol_Chiki', 'Ol_Chiki'),
        ('Old_Hungarian', 'Old_Hungarian'),
        ('Old_Italic', 'Old_Italic'),
        ('Old_North_Arabian', 'Old_North_Arabian'),
        ('Old_Permic', 'Old_Permic'),
        ('Old_Persian', 'Old_Persian'),
        ('Old_South_Arabian', 'Old_South_Arabian'),
        ('Old_Turkic', 'Old_Turkic'),
        ('Oriya', 'Oriya'),
        ('Ornamental_Dingbats', 'Ornamental_Dingbats'),
        ('Osage', 'Osage'),
        ('Osmanya', 'Osmanya'),
        ('Pahawh_Hmong', 'Pahawh_Hmong'),
        ('Palmyrene', 'Palmyrene'),
        ('Pau_Cin_Hau', 'Pau_Cin_Hau'),
        ('Phags_Pa', 'Phags_Pa'),
        ('Phaistos', 'Phaistos_Disc'),
        ('Phoenician', 'Phoenician'),
        ('Phonetic_Ext', 'Phonetic_Extensions'),
        ('Phonetic_Ext_Sup', 'Phonetic_Extensions_Supplement'),
        ('Playing_Cards', 'Playing_Cards'),
        ('Psalter_Pahlavi', 'Psalter_Pahlavi'),
        ('PUA', 'Private_Use_Area', 'Private_Use'),
        ('Punctuation', 'General_Punctuation'),
        ('Rejang', 'Rejang'),
        ('Rumi', 'Rumi_Numeral_Symbols'),
        ('Runic', 'Runic'),
        ('Samaritan', 'Samaritan'),
        ('Saurashtra', 'Saurashtra'),
        ('Sharada', 'Sharada'),
        ('Shavian', 'Shavian'),
        ('Shorthand_Format_Controls', 'Shorthand_Format_Controls'),
        ('Siddham', 'Siddham'),
        ('Sinhala', 'Sinhala'),
        ('Sinhala_Archaic_Numbers', 'Sinhala_Archaic_Numbers'),
        ('Small_Forms', 'Small_Form_Variants'),
        ('Sora_Sompeng', 'Sora_Sompeng'),
        ('Specials', 'Specials'),
        ('Sundanese', 'Sundanese'),
        ('Sundanese_Sup', 'Sundanese_Supplement'),
        ('Sup_Arrows_A', 'Supplemental_Arrows_A'),
        ('Sup_Arrows_B', 'Supplemental_Arrows_B'),
        ('Sup_Arrows_C', 'Supplemental_Arrows_C'),
        ('Sup_Math_Operators', 'Supplemental_Mathematical_Operators'),
        ('Sup_PUA_A', 'Supplementary_Private_Use_Area_A'),
        ('Sup_PUA_B', 'Supplementary_Private_Use_Area_B'),
        ('Sup_Punctuation', 'Supplemental_Punctuation'),
        ('Sup_Symbols_And_Pictographs', 'Supplemental_Symbols_And_Pictographs'),
        ('Super_And_Sub', 'Superscripts_And_Subscripts'),
        ('Sutton_SignWriting', 'Sutton_SignWriting'),
        ('Syloti_Nagri', 'Syloti_Nagri'),
        ('Syriac', 'Syriac'),
        ('Tagalog', 'Tagalog'),
        ('Tagbanwa', 'Tagbanwa'),
        ('Tags', 'Tags'),
        ('Tai_Le', 'Tai_Le'),
        ('Tai_Tham', 'Tai_Tham'),
        ('Tai_Viet', 'Tai_Viet'),
        ('Tai_Xuan_Jing', 'Tai_Xuan_Jing_Symbols'),
        ('Takri', 'Takri'),
        ('Tamil', 'Tamil'),
        ('Tangut', 'Tangut'),
        ('Tangut_Components', 'Tangut_Components'),
        ('Telugu', 'Telugu'),
        ('Thaana', 'Thaana'),
        ('Thai', 'Thai'),
        ('Tibetan', 'Tibetan'),
        ('Tifinagh', 'Tifinagh'),
        ('Tirhuta', 'Tirhuta'),
        ('Transport_And_Map', 'Transport_And_Map_Symbols'),
        ('UCAS', 'Unified_Canadian_Aboriginal_Syllabics', 'Canadian_Syllabics'),
        ('UCAS_Ext', 'Unified_Canadian_Aboriginal_Syllabics_Extended'),
        ('Ugaritic', 'Ugaritic'),
        ('Vai', 'Vai'),
        ('Vedic_Ext', 'Vedic_Extensions'),
        ('Vertical_Forms', 'Vertical_Forms'),
        ('VS', 'Variation_Selectors'),
        ('VS_Sup', 'Variation_Selectors_Supplement'),
        ('Warang_Citi', 'Warang_Citi'),
        ('Yi_Radicals', 'Yi_Radicals'),
        ('Yi_Syllables', 'Yi_Syllables'),
        ('Yijing', 'Yijing_Hexagram_Symbols'),
    ], catalog=True, status=Normative, scope=General, min=v('2.0.0'))
    prop.make_enum(g, ['sc', 'Script'], [
        ('Adlm', 'Adlam'),
        ('Aghb', 'Caucasian_Albanian'),
        ('Ahom', 'Ahom'),
        ('Arab', 'Arabic'),
        ('Armi', 'Imperial_Aramaic'),
        ('Armn', 'Armenian'),
        ('Avst', 'Avestan'),
        ('Bali', 'Balinese'),
        ('Bamu', 'Bamum'),
        ('Bass', 'Bassa_Vah'),
        ('Batk', 'Batak'),
        ('Beng', 'Bengali'),
        ('Bhks', 'Bhaiksuki'),
        ('Bopo', 'Bopomofo'),
        ('Brah', 'Brahmi'),
        ('Brai', 'Braille'),
        ('Bugi', 'Buginese'),
        ('Buhd', 'Buhid'),
        ('Cakm', 'Chakma'),
        ('Cans', 'Canadian_Aboriginal'),
        ('Cari', 'Carian'),
        ('Cham', 'Cham'),
        ('Cher', 'Cherokee'),
        ('Copt', 'Coptic', 'Qaac'),
        ('Cprt', 'Cypriot'),
        ('Cyrl', 'Cyrillic'),
        ('Deva', 'Devanagari'),
        ('Dsrt', 'Deseret'),
        ('Dupl', 'Duployan'),
        ('Egyp', 'Egyptian_Hieroglyphs'),
        ('Elba', 'Elbasan'),
        ('Ethi', 'Ethiopic'),
        ('Geor', 'Georgian'),
        ('Glag', 'Glagolitic'),
        ('Goth', 'Gothic'),
        ('Gran', 'Grantha'),
        ('Grek', 'Greek'),
        ('Gujr', 'Gujarati'),
        ('Guru', 'Gurmukhi'),
        ('Hang', 'Hangul'),
        ('Hani', 'Han'),
        ('Hano', 'Hanunoo'),
        ('Hatr', 'Hatran'),
        ('Hebr', 'Hebrew'),
        ('Hira', 'Hiragana'),
        ('Hluw', 'Anatolian_Hieroglyphs'),
        ('Hmng', 'Pahawh_Hmong'),
        ('Hrkt', 'Katakana_Or_Hiragana'),
        ('Hung', 'Old_Hungarian'),
        ('Ital', 'Old_Italic'),
        ('Java', 'Javanese'),
        ('Kali', 'Kayah_Li'),
        ('Kana', 'Katakana'),
        ('Khar', 'Kharoshthi'),
        ('Khmr', 'Khmer'),
        ('Khoj', 'Khojki'),
        ('Knda', 'Kannada'),
        ('Kthi', 'Kaithi'),
        ('Lana', 'Tai_Tham'),
        ('Laoo', 'Lao'),
        ('Latn', 'Latin'),
        ('Lepc', 'Lepcha'),
        ('Limb', 'Limbu'),
        ('Lina', 'Linear_A'),
        ('Linb', 'Linear_B'),
        ('Lisu', 'Lisu'),
        ('Lyci', 'Lycian'),
        ('Lydi', 'Lydian'),
        ('Mahj', 'Mahajani'),
        ('Mand', 'Mandaic'),
        ('Mani', 'Manichaean'),
        ('Marc', 'Marchen'),
        ('Mend', 'Mende_Kikakui'),
        ('Merc', 'Meroitic_Cursive'),
        ('Mero', 'Meroitic_Hieroglyphs'),
        ('Mlym', 'Malayalam'),
        ('Modi', 'Modi'),
        ('Mong', 'Mongolian'),
        ('Mroo', 'Mro'),
        ('Mtei', 'Meetei_Mayek'),
        ('Mult', 'Multani'),
        ('Mymr', 'Myanmar'),
        ('Narb', 'Old_North_Arabian'),
        ('Nbat', 'Nabataean'),
        ('Newa', 'Newa'),
        ('Nkoo', 'Nko'),
        ('Ogam', 'Ogham'),
        ('Olck', 'Ol_Chiki'),
        ('Orkh', 'Old_Turkic'),
        ('Orya', 'Oriya'),
        ('Osge', 'Osage'),
        ('Osma', 'Osmanya'),
        ('Palm', 'Palmyrene'),
        ('Pauc', 'Pau_Cin_Hau'),
        ('Perm', 'Old_Permic'),
        ('Phag', 'Phags_Pa'),
        ('Phli', 'Inscriptional_Pahlavi'),
        ('Phlp', 'Psalter_Pahlavi'),
        ('Phnx', 'Phoenician'),
        ('Plrd', 'Miao'),
        ('Prti', 'Inscriptional_Parthian'),
        ('Rjng', 'Rejang'),
        ('Runr', 'Runic'),
        ('Samr', 'Samaritan'),
        ('Sarb', 'Old_South_Arabian'),
        ('Saur', 'Saurashtra'),
        ('Sgnw', 'SignWriting'),
        ('Shaw', 'Shavian'),
        ('Shrd', 'Sharada'),
        ('Sidd', 'Siddham'),
        ('Sind', 'Khudawadi'),
        ('Sinh', 'Sinhala'),
        ('Sora', 'Sora_Sompeng'),
        ('Sund', 'Sundanese'),
        ('Sylo', 'Syloti_Nagri'),
        ('Syrc', 'Syriac'),
        ('Tagb', 'Tagbanwa'),
        ('Takr', 'Takri'),
        ('Tale', 'Tai_Le'),
        ('Talu', 'New_Tai_Lue'),
        ('Taml', 'Tamil'),
        ('Tang', 'Tangut'),
        ('Tavt', 'Tai_Viet'),
        ('Telu', 'Telugu'),
        ('Tfng', 'Tifinagh'),
        ('Tglg', 'Tagalog'),
        ('Thaa', 'Thaana'),
        ('Thai', 'Thai'),
        ('Tibt', 'Tibetan'),
        ('Tirh', 'Tirhuta'),
        ('Ugar', 'Ugaritic'),
        ('Vaii', 'Vai'),
        ('Wara', 'Warang_Citi'),
        ('Xpeo', 'Old_Persian'),
        ('Xsux', 'Cuneiform'),
        ('Yiii', 'Yi'),
        ('Zinh', 'Inherited', 'Qaai'),
        ('Zyyy', 'Common'),
        ('Zzzz', 'Unknown'),
    ], catalog=True, status=Informative, scope=General, min=v('3.1.0'))
    # Moved to be *after* Script
    prop.make_set(g, ['scx', 'Script_Extensions'], Script, status=Informative, scope=General, min=v('6.0.0'))
    # Enumerated Properties
    prop.make_enum(g, ['bc', 'Bidi_Class'], [
        ('AL', 'Arabic_Letter'),
        ('AN', 'Arabic_Number'),
        ('B', 'Paragraph_Separator'),
        ('BN', 'Boundary_Neutral'),
        ('CS', 'Common_Separator'),
        ('EN', 'European_Number'),
        ('ES', 'European_Separator'),
        ('ET', 'European_Terminator'),
        ('FSI', 'First_Strong_Isolate'),
        ('L', 'Left_To_Right'),
        ('LRE', 'Left_To_Right_Embedding'),
        ('LRI', 'Left_To_Right_Isolate'),
        ('LRO', 'Left_To_Right_Override'),
        ('NSM', 'Nonspacing_Mark'),
        ('ON', 'Other_Neutral'),
        ('PDF', 'Pop_Directional_Format'),
        ('PDI', 'Pop_Directional_Isolate'),
        ('R', 'Right_To_Left'),
        ('RLE', 'Right_To_Left_Embedding'),
        ('RLI', 'Right_To_Left_Isolate'),
        ('RLO', 'Right_To_Left_Override'),
        ('S', 'Segment_Separator'),
        ('WS', 'White_Space'),
    ], status=Normative, scope=Bidirectional, min=v('1.0.0'))
    prop.make_enum(g, ['bpt', 'Bidi_Paired_Bracket_Type'], [
        ('c', 'Close'),
        ('n', 'None'),
        ('o', 'Open'),
    ], status=Normative, scope=Bidirectional, min=v('6.3.0'))
    prop.make_enum(g, ['ccc', 'Canonical_Combining_Class'], [
        ('0', 'NR', 'Not_Reordered'),
        ('1', 'OV', 'Overlay'),
        ('7', 'NK', 'Nukta'),
        ('8', 'KV', 'Kana_Voicing'),
        ('9', 'VR', 'Virama'),
        ('10', 'CCC10', 'CCC10'),
        ('11', 'CCC11', 'CCC11'),
        ('12', 'CCC12', 'CCC12'),
        ('13', 'CCC13', 'CCC13'),
        ('14', 'CCC14', 'CCC14'),
        ('15', 'CCC15', 'CCC15'),
        ('16', 'CCC16', 'CCC16'),
        ('17', 'CCC17', 'CCC17'),
        ('18', 'CCC18', 'CCC18'),
        ('19', 'CCC19', 'CCC19'),
        ('20', 'CCC20', 'CCC20'),
        ('21', 'CCC21', 'CCC21'),
        ('22', 'CCC22', 'CCC22'),
        ('23', 'CCC23', 'CCC23'),
        ('24', 'CCC24', 'CCC24'),
        ('25', 'CCC25', 'CCC25'),
        ('26', 'CCC26', 'CCC26'),
        ('27', 'CCC27', 'CCC27'),
        ('28', 'CCC28', 'CCC28'),
        ('29', 'CCC29', 'CCC29'),
        ('30', 'CCC30', 'CCC30'),
        ('31', 'CCC31', 'CCC31'),
        ('32', 'CCC32', 'CCC32'),
        ('33', 'CCC33', 'CCC33'),
        ('34', 'CCC34', 'CCC34'),
        ('35', 'CCC35', 'CCC35'),
        ('36', 'CCC36', 'CCC36'),
        ('84', 'CCC84', 'CCC84'),
        ('91', 'CCC91', 'CCC91'),
        ('103', 'CCC103', 'CCC103'),
        ('107', 'CCC107', 'CCC107'),
        ('118', 'CCC118', 'CCC118'),
        ('122', 'CCC122', 'CCC122'),
        ('129', 'CCC129', 'CCC129'),
        ('130', 'CCC130', 'CCC130'),
        ('132', 'CCC132', 'CCC132'),
        ('133', 'CCC133', 'CCC133'),
        ('200', 'ATBL', 'Attached_Below_Left'),
        ('202', 'ATB', 'Attached_Below'),
        ('214', 'ATA', 'Attached_Above'),
        ('216', 'ATAR', 'Attached_Above_Right'),
        ('218', 'BL', 'Below_Left'),
        ('220', 'B', 'Below'),
        ('222', 'BR', 'Below_Right'),
        ('224', 'L', 'Left'),
        ('226', 'R', 'Right'),
        ('228', 'AL', 'Above_Left'),
        ('230', 'A', 'Above'),
        ('232', 'AR', 'Above_Right'),
        ('233', 'DB', 'Double_Below'),
        ('234', 'DA', 'Double_Above'),
        ('240', 'IS', 'Iota_Subscript'),
    ], manual_index=True, status=Normative, scope=Normalization, min=v('1.0.0'))
    prop.make_enum(g, ['dt', 'Decomposition_Type'], [
        ('Can', 'Canonical', 'can'),
        ('Com', 'Compat', 'com'),
        ('Enc', 'Circle', 'enc'),
        ('Fin', 'Final', 'fin'),
        ('Font', 'Font', 'font'),
        ('Fra', 'Fraction', 'fra'),
        ('Init', 'Initial', 'init'),
        ('Iso', 'Isolated', 'iso'),
        ('Med', 'Medial', 'med'),
        ('Nar', 'Narrow', 'nar'),
        ('Nb', 'Nobreak', 'nb'),
        ('None', 'None', 'none'),
        ('Sml', 'Small', 'sml'),
        ('Sqr', 'Square', 'sqr'),
        ('Sub', 'Sub', 'sub'),
        ('Sup', 'Super', 'sup'),
        ('Vert', 'Vertical', 'vert'),
        ('Wide', 'Wide', 'wide'),
    ], status=Normative_and_Informative, scope=Normalization, min=v('1.0.0'))
    # Must be after dm and dt
    prop.make_tagged_item(g, ['X_Decomposition_Type_and_Mapping'], Decomposition_Type, Decomposition_Mapping, status=None, scope=Normalization, min=versioning.INFINITY)
    prop.make_enum(g, ['ea', 'East_Asian_Width'], [
        ('A', 'Ambiguous'),
        ('F', 'Fullwidth'),
        ('H', 'Halfwidth'),
        ('N', 'Neutral'),
        ('Na', 'Narrow'),
        ('W', 'Wide'),
    ], status=Informative, scope=Shaping_and_Rendering, min=v('3.0.0'))
    prop.make_enum(g, ['gc', 'General_Category'], [
        ('C', 'Other'),
        ('Cc', 'Control', 'cntrl'),
        ('Cf', 'Format'),
        ('Cn', 'Unassigned'),
        ('Co', 'Private_Use'),
        ('Cs', 'Surrogate'),
        ('L', 'Letter'),
        ('LC', 'Cased_Letter'),
        ('Ll', 'Lowercase_Letter'),
        ('Lm', 'Modifier_Letter'),
        ('Lo', 'Other_Letter'),
        ('Lt', 'Titlecase_Letter'),
        ('Lu', 'Uppercase_Letter'),
        ('M', 'Mark', 'Combining_Mark'),
        ('Mc', 'Spacing_Mark'),
        ('Me', 'Enclosing_Mark'),
        ('Mn', 'Nonspacing_Mark'),
        ('N', 'Number'),
        ('Nd', 'Decimal_Number', 'digit'),
        ('Nl', 'Letter_Number'),
        ('No', 'Other_Number'),
        ('P', 'Punctuation', 'punct'),
        ('Pc', 'Connector_Punctuation'),
        ('Pd', 'Dash_Punctuation'),
        ('Pe', 'Close_Punctuation'),
        ('Pf', 'Final_Punctuation'),
        ('Pi', 'Initial_Punctuation'),
        ('Po', 'Other_Punctuation'),
        ('Ps', 'Open_Punctuation'),
        ('S', 'Symbol'),
        ('Sc', 'Currency_Symbol'),
        ('Sk', 'Modifier_Symbol'),
        ('Sm', 'Math_Symbol'),
        ('So', 'Other_Symbol'),
        ('Z', 'Separator'),
        ('Zl', 'Line_Separator'),
        ('Zp', 'Paragraph_Separator'),
        ('Zs', 'Space_Separator'),
    ], status=Normative, scope=General, min=v('1.0.0'))
    prop.make_enum(g, ['GCB', 'Grapheme_Cluster_Break'], [
        ('CN', 'Control'),
        ('CR', 'CR'),
        ('EB', 'E_Base'),
        ('EBG', 'E_Base_GAZ'),
        ('EM', 'E_Modifier'),
        ('EX', 'Extend'),
        ('GAZ', 'Glue_After_Zwj'),
        ('L', 'L'),
        ('LF', 'LF'),
        ('LV', 'LV'),
        ('LVT', 'LVT'),
        ('PP', 'Prepend'),
        ('RI', 'Regional_Indicator'),
        ('SM', 'SpacingMark'),
        ('T', 'T'),
        ('V', 'V'),
        ('XX', 'Other'),
        ('ZWJ', 'ZWJ'),
    ], status=Informative, scope=Shaping_and_Rendering, min=v('4.1.0'))
    prop.make_enum(g, ['hst', 'Hangul_Syllable_Type'], [
        ('L', 'Leading_Jamo'),
        ('LV', 'LV_Syllable'),
        ('LVT', 'LVT_Syllable'),
        ('NA', 'Not_Applicable'),
        ('T', 'Trailing_Jamo'),
        ('V', 'Vowel_Jamo'),
    ], status=Normative, scope=General, min=v('4.0.0'))
    prop.make_enum(g, ['InPC', 'Indic_Positional_Category'], [
        ('Bottom', 'Bottom'),
        ('Bottom_And_Right', 'Bottom_And_Right'),
        ('Left', 'Left'),
        ('Left_And_Right', 'Left_And_Right'),
        ('NA', 'NA'),
        ('Overstruck', 'Overstruck'),
        ('Right', 'Right'),
        ('Top', 'Top'),
        ('Top_And_Bottom', 'Top_And_Bottom'),
        ('Top_And_Bottom_And_Right', 'Top_And_Bottom_And_Right'),
        ('Top_And_Left', 'Top_And_Left'),
        ('Top_And_Left_And_Right', 'Top_And_Left_And_Right'),
        ('Top_And_Right', 'Top_And_Right'),
        ('Visual_Order_Left', 'Visual_Order_Left'),
    ], status=Informative, scope=Miscellaneous, min=v('6.0.0'))
    prop.make_enum(g, ['InSC', 'Indic_Syllabic_Category'], [
        ('Avagraha', 'Avagraha'),
        ('Bindu', 'Bindu'),
        ('Brahmi_Joining_Number', 'Brahmi_Joining_Number'),
        ('Cantillation_Mark', 'Cantillation_Mark'),
        ('Consonant', 'Consonant'),
        ('Consonant_Dead', 'Consonant_Dead'),
        ('Consonant_Final', 'Consonant_Final'),
        ('Consonant_Head_Letter', 'Consonant_Head_Letter'),
        ('Consonant_Killer', 'Consonant_Killer'),
        ('Consonant_Medial', 'Consonant_Medial'),
        ('Consonant_Placeholder', 'Consonant_Placeholder'),
        ('Consonant_Preceding_Repha', 'Consonant_Preceding_Repha'),
        ('Consonant_Prefixed', 'Consonant_Prefixed'),
        ('Consonant_Subjoined', 'Consonant_Subjoined'),
        ('Consonant_Succeeding_Repha', 'Consonant_Succeeding_Repha'),
        ('Consonant_With_Stacker', 'Consonant_With_Stacker'),
        ('Gemination_Mark', 'Gemination_Mark'),
        ('Invisible_Stacker', 'Invisible_Stacker'),
        ('Joiner', 'Joiner'),
        ('Modifying_Letter', 'Modifying_Letter'),
        ('Non_Joiner', 'Non_Joiner'),
        ('Nukta', 'Nukta'),
        ('Number', 'Number'),
        ('Number_Joiner', 'Number_Joiner'),
        ('Other', 'Other'),
        ('Pure_Killer', 'Pure_Killer'),
        ('Register_Shifter', 'Register_Shifter'),
        ('Syllable_Modifier', 'Syllable_Modifier'),
        ('Tone_Letter', 'Tone_Letter'),
        ('Tone_Mark', 'Tone_Mark'),
        ('Virama', 'Virama'),
        ('Visarga', 'Visarga'),
        ('Vowel', 'Vowel'),
        ('Vowel_Dependent', 'Vowel_Dependent'),
        ('Vowel_Independent', 'Vowel_Independent'),
    ], status=Informative, scope=Miscellaneous, min=v('6.0.0'))
    prop.make_enum(g, ['jg', 'Joining_Group'], [
        ('African_Feh', 'African_Feh'),
        ('African_Noon', 'African_Noon'),
        ('African_Qaf', 'African_Qaf'),
        ('Ain', 'Ain'),
        ('Alaph', 'Alaph'),
        ('Alef', 'Alef'),
        ('Beh', 'Beh'),
        ('Beth', 'Beth'),
        ('Burushaski_Yeh_Barree', 'Burushaski_Yeh_Barree'),
        ('Dal', 'Dal'),
        ('Dalath_Rish', 'Dalath_Rish'),
        ('E', 'E'),
        ('Farsi_Yeh', 'Farsi_Yeh'),
        ('Fe', 'Fe'),
        ('Feh', 'Feh'),
        ('Final_Semkath', 'Final_Semkath'),
        ('Gaf', 'Gaf'),
        ('Gamal', 'Gamal'),
        ('Hah', 'Hah'),
        ('He', 'He'),
        ('Heh', 'Heh'),
        ('Heh_Goal', 'Heh_Goal'),
        ('Heth', 'Heth'),
        ('Kaf', 'Kaf'),
        ('Kaph', 'Kaph'),
        ('Khaph', 'Khaph'),
        ('Knotted_Heh', 'Knotted_Heh'),
        ('Lam', 'Lam'),
        ('Lamadh', 'Lamadh'),
        ('Manichaean_Aleph', 'Manichaean_Aleph'),
        ('Manichaean_Ayin', 'Manichaean_Ayin'),
        ('Manichaean_Beth', 'Manichaean_Beth'),
        ('Manichaean_Daleth', 'Manichaean_Daleth'),
        ('Manichaean_Dhamedh', 'Manichaean_Dhamedh'),
        ('Manichaean_Five', 'Manichaean_Five'),
        ('Manichaean_Gimel', 'Manichaean_Gimel'),
        ('Manichaean_Heth', 'Manichaean_Heth'),
        ('Manichaean_Hundred', 'Manichaean_Hundred'),
        ('Manichaean_Kaph', 'Manichaean_Kaph'),
        ('Manichaean_Lamedh', 'Manichaean_Lamedh'),
        ('Manichaean_Mem', 'Manichaean_Mem'),
        ('Manichaean_Nun', 'Manichaean_Nun'),
        ('Manichaean_One', 'Manichaean_One'),
        ('Manichaean_Pe', 'Manichaean_Pe'),
        ('Manichaean_Qoph', 'Manichaean_Qoph'),
        ('Manichaean_Resh', 'Manichaean_Resh'),
        ('Manichaean_Sadhe', 'Manichaean_Sadhe'),
        ('Manichaean_Samekh', 'Manichaean_Samekh'),
        ('Manichaean_Taw', 'Manichaean_Taw'),
        ('Manichaean_Ten', 'Manichaean_Ten'),
        ('Manichaean_Teth', 'Manichaean_Teth'),
        ('Manichaean_Thamedh', 'Manichaean_Thamedh'),
        ('Manichaean_Twenty', 'Manichaean_Twenty'),
        ('Manichaean_Waw', 'Manichaean_Waw'),
        ('Manichaean_Yodh', 'Manichaean_Yodh'),
        ('Manichaean_Zayin', 'Manichaean_Zayin'),
        ('Meem', 'Meem'),
        ('Mim', 'Mim'),
        ('No_Joining_Group', 'No_Joining_Group'),
        ('Noon', 'Noon'),
        ('Nun', 'Nun'),
        ('Nya', 'Nya'),
        ('Pe', 'Pe'),
        ('Qaf', 'Qaf'),
        ('Qaph', 'Qaph'),
        ('Reh', 'Reh'),
        ('Reversed_Pe', 'Reversed_Pe'),
        ('Rohingya_Yeh', 'Rohingya_Yeh'),
        ('Sad', 'Sad'),
        ('Sadhe', 'Sadhe'),
        ('Seen', 'Seen'),
        ('Semkath', 'Semkath'),
        ('Shin', 'Shin'),
        ('Straight_Waw', 'Straight_Waw'),
        ('Swash_Kaf', 'Swash_Kaf'),
        ('Syriac_Waw', 'Syriac_Waw'),
        ('Tah', 'Tah'),
        ('Taw', 'Taw'),
        ('Teh_Marbuta', 'Teh_Marbuta'),
        ('Teh_Marbuta_Goal', 'Hamza_On_Heh_Goal'),
        ('Teth', 'Teth'),
        ('Waw', 'Waw'),
        ('Yeh', 'Yeh'),
        ('Yeh_Barree', 'Yeh_Barree'),
        ('Yeh_With_Tail', 'Yeh_With_Tail'),
        ('Yudh', 'Yudh'),
        ('Yudh_He', 'Yudh_He'),
        ('Zain', 'Zain'),
        ('Zhain', 'Zhain'),
    ], status=Normative, scope=Shaping_and_Rendering, min=v('2.0.0'))
    prop.make_enum(g, ['jt', 'Joining_Type'], [
        ('C', 'Join_Causing'),
        ('D', 'Dual_Joining'),
        ('L', 'Left_Joining'),
        ('R', 'Right_Joining'),
        ('T', 'Transparent'),
        ('U', 'Non_Joining'),
    ], status=Normative, scope=Shaping_and_Rendering, min=v('2.0.0'))
    prop.make_enum(g, ['lb', 'Line_Break'], [
        ('AI', 'Ambiguous'),
        ('AL', 'Alphabetic'),
        ('B2', 'Break_Both'),
        ('BA', 'Break_After'),
        ('BB', 'Break_Before'),
        ('BK', 'Mandatory_Break'),
        ('CB', 'Contingent_Break'),
        ('CJ', 'Conditional_Japanese_Starter'),
        ('CL', 'Close_Punctuation'),
        ('CM', 'Combining_Mark'),
        ('CP', 'Close_Parenthesis'),
        ('CR', 'Carriage_Return'),
        ('EB', 'E_Base'),
        ('EM', 'E_Modifier'),
        ('EX', 'Exclamation'),
        ('GL', 'Glue'),
        ('H2', 'H2'),
        ('H3', 'H3'),
        ('HL', 'Hebrew_Letter'),
        ('HY', 'Hyphen'),
        ('ID', 'Ideographic'),
        ('IN', 'Inseparable', 'Inseperable'),
        ('IS', 'Infix_Numeric'),
        ('JL', 'JL'),
        ('JT', 'JT'),
        ('JV', 'JV'),
        ('LF', 'Line_Feed'),
        ('NL', 'Next_Line'),
        ('NS', 'Nonstarter'),
        ('NU', 'Numeric'),
        ('OP', 'Open_Punctuation'),
        ('PO', 'Postfix_Numeric'),
        ('PR', 'Prefix_Numeric'),
        ('QU', 'Quotation'),
        ('RI', 'Regional_Indicator'),
        ('SA', 'Complex_Context'),
        ('SG', 'Surrogate'),
        ('SP', 'Space'),
        ('SY', 'Break_Symbols'),
        ('WJ', 'Word_Joiner'),
        ('XX', 'Unknown'),
        ('ZW', 'ZWSpace'),
        ('ZWJ', 'ZWJ'),
    ], status=Normative, scope=Shaping_and_Rendering, min=v('3.0.0'))
    prop.make_enum(g, ['NFC_QC', 'NFC_Quick_Check'], [
        ('M', 'Maybe'),
        ('N', 'No'),
        ('Y', 'Yes'),
    ], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_enum(g, ['NFD_QC', 'NFD_Quick_Check'], [
        ('N', 'No'),
        ('Y', 'Yes'),
    ], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_enum(g, ['NFKC_QC', 'NFKC_Quick_Check'], [
        ('M', 'Maybe'),
        ('N', 'No'),
        ('Y', 'Yes'),
    ], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_enum(g, ['NFKD_QC', 'NFKD_Quick_Check'], [
        ('N', 'No'),
        ('Y', 'Yes'),
    ], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_enum(g, ['nt', 'Numeric_Type'], [
        ('De', 'Decimal'),
        ('Di', 'Digit'),
        ('None', 'None'),
        ('Nu', 'Numeric'),
    ], status=Normative_and_Informative, scope=Numeric, min=v('1.0.0'))
    prop.make_enum(g, ['SB', 'Sentence_Break'], [
        ('AT', 'ATerm'),
        ('CL', 'Close'),
        ('CR', 'CR'),
        ('EX', 'Extend'),
        ('FO', 'Format'),
        ('LE', 'OLetter'),
        ('LF', 'LF'),
        ('LO', 'Lower'),
        ('NU', 'Numeric'),
        ('SC', 'SContinue'),
        ('SE', 'Sep'),
        ('SP', 'Sp'),
        ('ST', 'STerm'),
        ('UP', 'Upper'),
        ('XX', 'Other'),
    ], status=Informative, scope=Shaping_and_Rendering, min=v('4.1.0'))
    prop.make_enum(g, ['WB', 'Word_Break'], [
        ('CR', 'CR'),
        ('DQ', 'Double_Quote'),
        ('EB', 'E_Base'),
        ('EBG', 'E_Base_GAZ'),
        ('EM', 'E_Modifier'),
        ('EX', 'ExtendNumLet'),
        ('Extend', 'Extend'),
        ('FO', 'Format'),
        ('GAZ', 'Glue_After_Zwj'),
        ('HL', 'Hebrew_Letter'),
        ('KA', 'Katakana'),
        ('LE', 'ALetter'),
        ('LF', 'LF'),
        ('MB', 'MidNumLet'),
        ('ML', 'MidLetter'),
        ('MN', 'MidNum'),
        ('NL', 'Newline'),
        ('NU', 'Numeric'),
        ('RI', 'Regional_Indicator'),
        ('SQ', 'Single_Quote'),
        ('XX', 'Other'),
        ('ZWJ', 'ZWJ'),
    ], status=Informative, scope=Shaping_and_Rendering, min=v('4.1.0'))
    # Binary Properties
    prop.make_bool(g, ['AHex', 'ASCII_Hex_Digit'], status=Normative, scope=Numeric, min=v('3.1.1'))
    prop.make_bool(g, ['Alpha', 'Alphabetic'], status=Informative, scope=General, min=v('2.0.14'))
    prop.make_bool(g, ['Bidi_C', 'Bidi_Control'], status=Normative, scope=Bidirectional, min=v('3.1.0'))
    prop.make_bool(g, ['Bidi_M', 'Bidi_Mirrored'], status=Normative, scope=Bidirectional, min=v('3.2.0'))
    prop.make_bool(g, ['Cased', 'Cased'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['CE', 'Composition_Exclusion'], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_bool(g, ['CI', 'Case_Ignorable'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['Comp_Ex', 'Full_Composition_Exclusion'], status=Normative, scope=Normalization, min=v('3.1.0'))
    prop.make_bool(g, ['CWCF', 'Changes_When_Casefolded'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['CWCM', 'Changes_When_Casemapped'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['CWKCF', 'Changes_When_NFKC_Casefolded'], status=Informative, scope=Normalization, min=v('5.2.0'))
    prop.make_bool(g, ['CWL', 'Changes_When_Lowercased'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['CWT', 'Changes_When_Titlecased'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['CWU', 'Changes_When_Uppercased'], status=Informative, scope=Case, min=v('5.2.0'))
    prop.make_bool(g, ['Dash', 'Dash'], status=Informative, scope=Miscellaneous, min=v('2.0.14'))
    prop.make_bool(g, ['Dep', 'Deprecated'], status=Normative, scope=General, min=v('3.2.0'))
    prop.make_bool(g, ['DI', 'Default_Ignorable_Code_Point'], status=Normative, scope=General, min=v('3.1.0'))
    prop.make_bool(g, ['Dia', 'Diacritic'], status=Informative, scope=Miscellaneous, min=v('2.0.14'))
    prop.make_bool(g, ['Ext', 'Extender'], status=Informative, scope=Miscellaneous, min=v('2.0.14'))
    prop.make_bool(g, ['Gr_Base', 'Grapheme_Base'], status=Normative, scope=Miscellaneous, min=v('3.2.0'))
    prop.make_bool(g, ['Gr_Ext', 'Grapheme_Extend'], status=Normative, scope=Miscellaneous, min=v('3.2.0'))
    prop.make_bool(g, ['Gr_Link', 'Grapheme_Link'], status=Informative, scope=Miscellaneous, deprecated=v('5.0.0'), min=v('3.2.0'))
    prop.make_bool(g, ['Hex', 'Hex_Digit'], status=Informative, scope=Numeric, min=v('2.0.14'))
    prop.make_bool(g, ['Hyphen', 'Hyphen'], status=Informative, scope=Miscellaneous, deprecated=v('6.0.0'), stabilized=v('4.0.0'), min=v('2.0.14'))
    prop.make_bool(g, ['IDC', 'ID_Continue'], status=Informative, scope=Identifiers, min=v('3.1.0'))
    prop.make_bool(g, ['Ideo', 'Ideographic'], status=Informative, scope=CJK, min=v('2.0.14'))
    prop.make_bool(g, ['IDS', 'ID_Start'], status=Informative, scope=Identifiers, min=v('3.1.0'))
    prop.make_bool(g, ['IDSB', 'IDS_Binary_Operator'], status=Normative, scope=CJK, min=v('3.2.0'))
    prop.make_bool(g, ['IDST', 'IDS_Trinary_Operator'], status=Normative, scope=CJK, min=v('3.2.0'))
    prop.make_bool(g, ['Join_C', 'Join_Control'], status=Normative, scope=Shaping_and_Rendering, min=v('3.1.0'))
    prop.make_bool(g, ['LOE', 'Logical_Order_Exception'], status=Normative, scope=General, min=v('3.2.0'))
    prop.make_bool(g, ['Lower', 'Lowercase'], status=Informative, scope=Case, min=v('3.0.0'))
    prop.make_bool(g, ['Math', 'Math'], status=Informative, scope=Miscellaneous, min=v('2.0.14'))
    prop.make_bool(g, ['NChar', 'Noncharacter_Code_Point'], status=Normative, scope=General, min=v('3.1.0'))
    prop.make_bool(g, ['OAlpha', 'Other_Alphabetic'], status=status.Contributory, scope=scope.Contributory, min=v('3.1.0'))
    prop.make_bool(g, ['ODI', 'Other_Default_Ignorable_Code_Point'], status=status.Contributory, scope=scope.Contributory, min=v('3.2.0'))
    prop.make_bool(g, ['OGr_Ext', 'Other_Grapheme_Extend'], status=status.Contributory, scope=scope.Contributory, min=v('3.2.0'))
    prop.make_bool(g, ['OIDC', 'Other_ID_Continue'], status=status.Contributory, scope=scope.Contributory, min=v('4.1.0'))
    prop.make_bool(g, ['OIDS', 'Other_ID_Start'], status=status.Contributory, scope=scope.Contributory, min=v('4.0.0'))
    prop.make_bool(g, ['OLower', 'Other_Lowercase'], status=status.Contributory, scope=scope.Contributory, min=v('3.1.0'))
    prop.make_bool(g, ['OMath', 'Other_Math'], status=status.Contributory, scope=scope.Contributory, min=v('3.1.0'))
    prop.make_bool(g, ['OUpper', 'Other_Uppercase'], status=status.Contributory, scope=scope.Contributory, min=v('3.1.0'))
    prop.make_bool(g, ['Pat_Syn', 'Pattern_Syntax'], status=Normative, scope=Identifiers, min=v('4.1.0'))
    prop.make_bool(g, ['Pat_WS', 'Pattern_White_Space'], status=Normative, scope=Identifiers, min=v('4.1.0'))
    prop.make_bool(g, ['PCM', 'Prepended_Concatenation_Mark'], status=Informative, scope=Shaping_and_Rendering, min=v('9.0.0'))
    prop.make_bool(g, ['QMark', 'Quotation_Mark'], status=Informative, scope=Miscellaneous, min=v('3.1.0'))
    prop.make_bool(g, ['Radical', 'Radical'], status=Normative, scope=CJK, min=v('3.1.0'))
    prop.make_bool(g, ['SD', 'Soft_Dotted'], status=Normative, scope=Case, min=v('3.2.0'))
    prop.make_bool(g, ['STerm', 'Sentence_Terminal'], status=Informative, scope=Miscellaneous, min=v('4.0.1'))
    prop.make_bool(g, ['Term', 'Terminal_Punctuation'], status=Informative, scope=Miscellaneous, min=v('3.1.0'))
    prop.make_bool(g, ['UIdeo', 'Unified_Ideograph'], status=Normative, scope=CJK, min=v('3.2.0'))
    prop.make_bool(g, ['Upper', 'Uppercase'], status=Informative, scope=Case, min=v('3.0.0'))
    prop.make_bool(g, ['VS', 'Variation_Selector'], status=Normative, scope=General, min=v('4.0.1'))
    prop.make_bool(g, ['WSpace', 'White_Space', 'space'], status=Normative, scope=General, min=v('2.0.14'))
    prop.make_bool(g, ['XIDC', 'XID_Continue'], status=Informative, scope=Identifiers, min=v('3.1.0'))
    prop.make_bool(g, ['XIDS', 'XID_Start'], status=Informative, scope=Identifiers, min=v('3.1.0'))
    prop.make_bool(g, ['XO_NFC', 'Expands_On_NFC'], status=Normative, scope=Normalization, deprecated=v('6.0.0'), min=v('3.1.0'))
    prop.make_bool(g, ['XO_NFD', 'Expands_On_NFD'], status=Normative, scope=Normalization, deprecated=v('6.0.0'), min=v('3.1.0'))
    prop.make_bool(g, ['XO_NFKC', 'Expands_On_NFKC'], status=Normative, scope=Normalization, deprecated=v('6.0.0'), min=v('3.1.0'))
    prop.make_bool(g, ['XO_NFKD', 'Expands_On_NFKD'], status=Normative, scope=Normalization, deprecated=v('6.0.0'), min=v('3.1.0'))
    # Unihan Properties
    prop.make_int(g, ['kDefaultSortKey'], status=Informative, scope=CJK, min=v('6.1.0'))
    prop.make_int(g, ['cjkAccountingNumeric', 'kAccountingNumeric'], status=Informative, scope=Numeric, min=v('3.2.0'))
    prop.make_re(g, ['kBigFive'], r'[0-9A-F]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kCangjie'], r'[A-Z]+', None, status=Provisional, scope=Dictionary_like_Data, min=v('3.1.1'))
    prop.make_re(g, ['kCantonese'], r'[a-z]{1,6}[1-6]', ' ', status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kCCCII'], r'[0-9A-F]{6}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kCheungBauer'], r'[0-9]{3}/[0-9]{2};[A-Z]*;[][a-z1-6/,]+', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('5.0.0'))
    prop.make_re(g, ['kCheungBauerIndex'], r'[0-9]{3}\.[01][0-9]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('5.0.0'))
    prop.make_re(g, ['kCihaiT'], r'[1-9][0-9]{0,3}\.[0-9]{3}', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('3.2.0'))
    prop.make_re(g, ['kCNS1986'], r'[12E]-[0-9A-F]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kCNS1992'], r'[1-9]-[0-9A-F]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_u_code(g, ['cjkCompatibilityVariant', 'kCompatibilityVariant'], status=Normative, scope=IRG_Sources, min=v('3.2.0'))
    prop.make_re(g, ['kCowles'], r'[0-9]{1,4}(\.[0-9]{1,2})?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.1.1'))
    prop.make_re(g, ['kDaeJaweon'], r'[0-9]{4}\.[0-9]{2}[01]', None, status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_re(g, ['kDefinition'], r'[^\t"]*', None, status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kEACC'], r'[0-9A-F]{6}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kFenn'], r'[0-9]+a?[A-KP*]', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('3.1.1'))
    prop.make_re(g, ['kFennIndex'], r'[0-9][0-9]{0,2}\.[01][0-9]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('4.1.0'))
    prop.make_re(g, ['kFourCornerCode'], r'[0-9]{4}(\.[0-9])?', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('5.0.0'))
    prop.make_re(g, ['kFrequency'], r'[1-5]', None, status=Provisional, scope=Dictionary_like_Data, min=v('3.2.0'))
    prop.make_re(g, ['kGB0'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGB1'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGB3'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGB5'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGB7'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGB8'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kGradeLevel'], r'[1-6]', None, status=Provisional, scope=Dictionary_like_Data, min=v('3.2.0'))
    prop.make_re(g, ['kGSR'], r"[0-9]{4}[a-vx-z]'?", ' ', status=Provisional, scope=Dictionary_Indices, min=v('4.0.1'))
    prop.make_re(g, ['kHangul'], r'[\u1100-\u11FF]{2,3}', ' ', status=Provisional, scope=Readings, min=v('5.0.0'))
    prop.make_re(g, ['kHanYu'], r'[1-8][0-9]{4}\.[0-3][0-9][0-3]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_re(g, ['kHanyuPinlu'], r'[a-z\u0300-\u0302\u0304\u0308\u030C]+\([0-9]+\)', ' ', status=Provisional, scope=Readings, min=v('4.0.1'))
    prop.make_re(g, ['kHanyuPinyin'], r'([0-9]{5}\.[0-9]{2}0,)*[0-9]{5}\.[0-9]{2}0:([a-z\u0300-\u0302\u0304\u0308\u030C]+,)*[a-z\u0300-\u0302\u0304\u0308\u030C]+', ' ', status=Provisional, scope=Readings, min=v('5.2.0'))
    prop.make_re(g, ['kHDZRadBreak'], r'[\u2F00-\u2FD5]\[U\+2F[0-9A-D][0-9A-F]\]:[1-8][0-9]{4}\.[0-3][0-9]0', None, status=Provisional, scope=Dictionary_like_Data, min=v('4.1.0'))
    prop.make_re(g, ['kHKGlyph'], r'[0-9]{4}', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('3.1.1'))
    prop.make_re(g, ['kHKSCS'], r'[0-9A-F]{4}', None, status=Provisional, scope=Other_Mappings, min=v('3.1.1'))
    prop.make_re(g, ['kIBMJapan'], r'F[ABC][0-9A-F]{2}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['cjkIICore', 'kIICore'], r'[ABC][GHJKMPT]{1,7}', ' ', status=Normative, scope=IRG_Sources, min=v('4.1.0'))
    prop.make_re(g, ['kIRGDaeJaweon'], r'[0-9]{4}\.[0-9]{2}[01]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.0.0'))
    prop.make_re(g, ['kIRGDaiKanwaZiten'], r'[0-9]{5}\'?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.0.0'))
    prop.make_re(g, ['kIRGHanyuDaZidian'], r'[1-8][0-9]{4}\.[0-3][0-9][01]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.0.0'))
    prop.make_re(g, ['kIRGKangXi'], r'[01][0-9]{3}\.[0-7][0-9][01]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.0.0'))
    prop.make_re(g, ['cjkIRG_GSource', 'kIRG_GSource'], r'G(4K|BK|CH|CY|FZ|HC|HZ|((BK|CH|CY|DZ|GH|HC|RM|WZ|XC|XH|ZH)-[0-9]{4}\.[0-9]{2})|HZ-[0-9]{5}\.[0-9]{2}|(KX-[01][0-9]{3}\.1?[0-9]{2})|((CYY|FZ|JZ|ZFY|ZJW)-[0-9]{5})|([0135789ES]-[0-9A-F]{4})|(IDC-[0-9]{3})|(K-[0-9A-F]{4})|(H-\d{4})|(G?F[CZ]-\d{3,6}))', None, status=Normative, scope=IRG_Sources, min=v('3.0.0'))
    prop.make_re(g, ['cjkIRG_HSource', 'kIRG_HSource'], r'H(B[012])?-[0-9A-F]{4}', None, status=Normative, scope=IRG_Sources, min=v('3.1.0'))
    prop.make_re(g, ['cjkIRG_JSource', 'kIRG_JSource'], r'J1?((([0134AK]|A[34]|3A|ARIB)-[0-9A-F]{4,5})|(H-(((IB|JT|[0-9]{2})[0-9A-F]{4}S?))))', None, status=Normative, scope=IRG_Sources, min=v('3.0.0'))
    prop.make_re(g, ['cjkIRG_KPSource', 'kIRG_KPSource'], r'KP[01]-[0-9A-F]{4}', None, status=Normative, scope=IRG_Sources, min=v('3.1.1'))
    prop.make_re(g, ['cjkIRG_KSource', 'kIRG_KSource'], r'K[0-57]-[0-9A-F]{4}', None, status=Normative, scope=IRG_Sources, min=v('3.0.0'))
    prop.make_re(g, ['cjkIRG_MSource', 'kIRG_MSource'], r'MAC-[0-9]{5}', None, status=Normative, scope=IRG_Sources, min=v('5.2.0'))
    prop.make_re(g, ['cjkIRG_TSource', 'kIRG_TSource'], r'T[1-7B-F]-[0-9A-F]{4}', None, status=Normative, scope=IRG_Sources, min=v('3.0.0'))
    prop.make_re(g, ['cjkIRG_USource', 'kIRG_USource'], r'U(TC|CI|SAT)-[0-9]{5}', None, status=Normative, scope=IRG_Sources, min=v('4.0.1'))
    prop.make_re(g, ['cjkIRG_VSource', 'kIRG_VSource'], r'V[0-4]-[0-9A-F]{4}', None, status=Normative, scope=IRG_Sources, min=v('3.0.0'))
    prop.make_re(g, ['kJa'], r'[0-9A-F]{4}S?', ' ', status=Provisional, scope=Other_Mappings, min=v('8.0.0'))
    prop.make_re(g, ['kJapaneseKun'], r'[A-Z]+', ' ', status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kJapaneseOn'], r'[A-Z]+', ' ', status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kJis0'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kJis0213'], r'[12],[0-9]{2},[0-9]{1,2}', ' ', status=Provisional, scope=Other_Mappings, min=v('3.1.1'))
    prop.make_re(g, ['kJis1'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kKangXi'], r'[0-9]{4}\.[0-9]{2}[01]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_re(g, ['kKarlgren'], r'[1-9][0-9]{0,3}[A*]?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.1.1'))
    prop.make_re(g, ['kKorean'], r'[A-Z]+', ' ', status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kKPS0'], r'[0-9A-F]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('3.1.1'))
    prop.make_re(g, ['kKPS1'], r'[0-9A-F]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('3.1.1'))
    prop.make_re(g, ['kKSC0'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kKSC1'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kLau'], r'[1-9][0-9]{0,3}', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.1.1'))
    prop.make_re(g, ['kMainlandTelegraph'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kMandarin'], r'[a-z\u0300-\u0302\u0304\u0308\u030C]+', ' ', status=Informative, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kMatthews'], r'[1-9][0-9]{0,3}(a|\.5)?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_re(g, ['kMeyerWempe'], r'[1-9][0-9]{0,3}[a-t*]?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.1.0'))
    prop.make_re(g, ['kMorohashi'], r'[0-9]{5}\'?', ' ', status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_re(g, ['kNelson'], r'[0-9]{4}', ' ', status=Provisional, scope=Dictionary_Indices, min=v('2.0.0'))
    prop.make_int(g, ['cjkOtherNumeric', 'kOtherNumeric'], status=Informative, scope=Numeric, min=v('3.2.0'))
    prop.make_re(g, ['kPhonetic'], r'[1-9][0-9]{0,3}[A-D]?\*?', ' ', status=Provisional, scope=Dictionary_like_Data, min=v('3.1.0'))
    prop.make_int(g, ['cjkPrimaryNumeric', 'kPrimaryNumeric'], status=Informative, scope=Numeric, min=v('3.2.0'))
    prop.make_re(g, ['kPseudoGB1'], r'[0-9]{4}', None, status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kRSAdobe_Japan1_6'], r'[CV]\+[0-9]{1,5}\+[1-9][0-9]{0,2}\.[1-9][0-9]?\.[0-9]{1,2}', ' ', status=Provisional, scope=Radical_Stroke_Counts, min=v('4.1.0'))
    prop.make_re(g, ['kRSJapanese'], r'[1-9][0-9]{0,2}\.[0-9]{1,2}', ' ', status=Provisional, scope=Radical_Stroke_Counts, min=v('2.0.0'))
    prop.make_re(g, ['kRSKangXi'], r'[1-9][0-9]{0,2}\.-?[0-9]{1,2}', ' ', status=Provisional, scope=Radical_Stroke_Counts, min=v('2.0.0'))
    prop.make_re(g, ['kRSKanWa'], r'[1-9][0-9]{0,2}\.[0-9]{1,2}', ' ', status=Provisional, scope=Radical_Stroke_Counts, min=v('2.0.0'))
    prop.make_re(g, ['kRSKorean'], r'[1-9][0-9]{0,2}\.[0-9]{1,2}', ' ', status=Provisional, scope=Radical_Stroke_Counts, min=v('2.0.0'))
    prop.make_re(g, ['cjkRSUnicode', 'kRSUnicode', 'Unicode_Radical_Stroke', 'URS'], r'[1-9][0-9]{0,2}\'?\.-?[0-9]{1,2}', ' ', status=Informative, scope=IRG_Sources, min=v('2.0.0'))
    prop.make_re(g, ['kSBGY'], r'[0-9]{3}\.[0-7][0-9]', ' ', status=Provisional, scope=Dictionary_Indices, min=v('3.2.0'))
    prop.make_re(g, ['kSemanticVariant'], r'U\+2?[0-9A-F]{4}(<k[A-Za-z0-9]+(:[TBZFJ]+)?(,k[A-Za-z0-9]+(:[TBZFJ]+)?)*)?', ' ', status=Provisional, scope=Variants, min=v('2.0.0'))
    prop.make_set(g, ['kSimplifiedVariant'], prop.U_Codepoint, status=Provisional, scope=Variants, min=v('2.0.0'))
    prop.make_re(g, ['kSpecializedSemanticVariant'], r'U\+2?[0-9A-F]{4}(<k[A-Za-z0-9]+(:[TBZFJ]+)?(,k[A-Za-z0-9]+(:[TBZFJ]+)?)*)?', ' ', status=Provisional, scope=Variants, min=v('2.0.0'))
    prop.make_re(g, ['kTaiwanTelegraph'], r'[0-9]{4}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kTang'], r'\*?[A-Za-z()\u00E6\u0251\u0259\u025B\u0300\u030C]+', ' ', status=Provisional, scope=Readings, min=v('2.0.0'))
    prop.make_re(g, ['kTotalStrokes'], r'[1-9][0-9]{0,2}', ' ', status=Informative, scope=Dictionary_like_Data, min=v('3.1.0'))
    prop.make_set(g, ['kTraditionalVariant'], prop.U_Codepoint, status=Provisional, scope=Variants, min=v('2.0.0'))
    prop.make_re(g, ['kVietnamese'], r'[A-Za-z\u0110\u0111\u0300-\u0303\u0306\u0309\u031B\u0323]+', ' ', status=Provisional, scope=Readings, min=v('3.1.1'))
    prop.make_re(g, ['kXerox'], r'[0-9]{3}:[0-9]{3}', ' ', status=Provisional, scope=Other_Mappings, min=v('2.0.0'))
    prop.make_re(g, ['kXHC1983'], r'[0-9]{4}\.[0-9]{3}\*?(,[0-9]{4}\.[0-9]{3}\*?)*:[a-z\u0300\u0301\u0304\u0308\u030C]+', ' ', status=Provisional, scope=Readings, min=v('5.1.0'))
    prop.make_re(g, ['kZVariant'], r'U\+2?[0-9A-F]{4}(<k[A-Za-z0-9]+(:[TBZ]+)?(,k[A-Za-z0-9]+(:[TBZ]+)?)*)?', ' ', status=Provisional, scope=Variants, min=v('2.0.0'))
    # Tangut Properties
    # (there is no documentation for these!)
    prop.make_re(g, ['kTGT_MergedSrc'], r'|'.join([
        r'H2004-A-[0-9]{4}',
        r'H2004-B-[0-9]{4}',
        r'L1986-[0-9]{4}',
        r'L1997-[0-9]{4}',
        r'L2006-[0-9]{4}',
        r'L2008(-[0-9]{4}){1,2}',
        r'L2008-[0-9]{4}[AB]',
        r'N1966-[0-9]{3}-[0-9]{2}([0-9BDGK]|GG)',
        r'S1968-[0-9]{4}',
    ]), None, status=Normative, scope=Dictionary_Indices, min=v('9.0.0'))
    prop.make_re(g, ['kRSTUnicode'], r'[0-9]{1,3}.[0-9]{1,2}', None, status=Informative, scope=Dictionary_like_Data, min=v('9.0.0'))


_init_classes()
