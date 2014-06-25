# -*- coding: utf-8 -*-

import string
import re
import datetime


########
# Constants
########

DIGITS_SET  = set(string.digits)

# Package name separators - strings which sep package name
# from the version, e.g. linux[-]2.6.5. 
# This should not include '.' since it usually separates 
# the version numbers. This case is handled specially.
NAME_SEPS = ['-V', '-v', '-R', '-r', '_V', '_v', '_R', '_r', ' V', ' v', ' R', ' r', '/R', '/r', '/V', '/v', ' ', '-', '_', '/']
PNS_SET = set(NAME_SEPS)


########
# Helper functions
########

def pluralize(word, n):
    assert(type(word) is str)
    return word + 's' if n == 0 or n > 1 else word

def first_int(s):
    """Return the first integer in a string, or None"""
    # TODO these should be benchmarked against just using re
    ret = ''
    for c in s:
        if c in string.digits:
            ret += c
        else:
            break
    if len(ret) > 0:
        return int(ret)
    else:
        return None

def last_int(s):
    """Return the last integer in a string, or None"""
    ret = ''
    for c in reversed(s):
        if c in string.digits:
            ret += c
        else:
            break
    if len(ret) > 0:
        return int(ret[::-1])
    else:
        return None

def any_digits_in_str(s):
    return len(set(s) & DIGITS_SET) > 0

def str_is_all_digits(s):
    return len(s) > 0 and len(set(s) - DIGITS_SET) == 0

def next_digit_offset(s, start_offset=0):
    """Given an optional start offset, find the offset of the 
       next digit character in string s, or -1"""
    s_len = len(s)
    for i in xrange(start_offset, s_len):
        if s[i] in string.digits:
            return i
    return -1

def find_any_in_seq(search_vals, seq):
    """Find any value in search_vals in the sequence seq"""
    for v in search_vals:
        if v in seq:
            return True
    return False

def find_date(s):
    """If possible, find the first string in the line s representing a date,
       and return a 3-tuple: (start, end, datetime.date), or None"""
    # TODO i18n and whatnot
    months_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                     'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    months_long  = ['january', 'february', 'march', 'april', 'june',
                    'july', 'august', 'september', 'october', 'november', 
                    'december']
    s = s.lower()
    # Match strings on custom boundary
    tmp_pat = r'{}(?:[-,. _0-9])'
    months_short_pat = [tmp_pat.format(x) for x in months_short]
    months_long_pat  = [tmp_pat.format(x) for x in months_long]
    found_b = re.search('|'.join(months_short_pat), s)
    found_B = re.search('|'.join(months_long_pat), s)
    if found_b and found_B:
        return None
    if not found_b and not found_B:
        patlist = [
            # Some patterns have empty group for the separator so the
            # indices stay consistent
            r'((?:2\d\d\d|19\d\d))([-._ ])(\d\d)\2(\d\d)',
            r'((?:2\d\d\d|19\d\d))()(\d\d)(\d\d)',
            r'(\d\d)([-._ ])(\d\d)\2((?:2\d\d\d|19\d\d))',
            r'(\d\d)()(\d\d)((?:2\d\d\d|19\d\d))',
        ]
        m = None
        for pat in patlist:
            m = re.search(pat, s)
            if m:
                break
        if m:
            groups = m.groups()
            groups_len = len(groups)
            if groups_len == 4:
                x, _, y, z = groups
            else:
                raise Exception("find_date() got bogus number of matched groups (groups={}, groups_len={})".format(groups, groups_len)) 
            tmp = '{} {} {}'.format(x, y, z)
            if len(x) == 2:
                if int(y) > 12:
                    if int(x) <= 12 and int(y) <= 31 and int(z) >= 1970 \
                            and int(z) <= 2999:
                        return (m.start(), 
                            m.end(),   
                            datetime.datetime.strptime(tmp, "%m %d %Y").date())
                else:
                    if int(y) <= 12 and int(x) <= 31 and int(z) >= 1970 \
                            and int(z) <= 2999:
                        return (m.start(), 
                            m.end(),   
                            datetime.datetime.strptime(tmp, "%d %m %Y").date())
            if len(x) == 4:
                if int(y) > 12:
                    if int(x) >= 1970 and int(x) <= 2999 and \
                            int(y) <= 31 and int(z) <= 12:
                        return (m.start(),     
                            m.end(),       
                            datetime.datetime.strptime(tmp, "%Y %d %m").date())
                else:
                    if int(x) >= 1970 and int(x) <= 2999 and \
                            int(y) <= 12 and int(z) <= 31:
                        return (m.start(),     
                            m.end(),       
                            datetime.datetime.strptime(tmp, "%Y %m %d").date())
    # If that failed, try textual months
    patlist = [
        r'((?:2\d\d\d|19\d\d))([-._ ])([a-zA-Z]{3,})\2(\d\d?)',
        r'((?:2\d\d\d|19\d\d))()([a-zA-Z]{3,})(\d\d?)',
        r'(\d\d?)([-._ ])([a-zA-Z]{3,})[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
        r'([a-zA-Z]{3,})([-._ ])(\d\d?)[,]?\2((?:2\d\d\d|19\d\d|\d\d))',
        r'(\d\d?)()([a-zA-Z]{3,})((?:2\d\d\d|19\d\d|\d\d))',
    ]
    m = None
    for pat in patlist:
        m = re.search(pat, s)
        if m:
            break
    if m:
        groups = m.groups()
        groups_len = len(groups)
        x, _, y, z = groups
        if x[0] not in string.digits:
            # Month first, so swap day and month
            foo = x
            x = y
            y = foo
        if len(x) == 4:
            # Year first, so swap day and year
            foo = x
            x = z
            z = foo
        # Make sure it's a month
        y_tmp = y.lower()
        if y_tmp not in months_short and y_tmp not in months_long:
            return None
        # Now x is day, y is month, z is year
        fmt = '%d'
        x = '0' + x
        x = x[-2:]
        if len(z) == 2:
            if int(z) > 69:
                z = '19' + z
            else:
                z = '20' + z
            z = z[-4:]
        if len(y) == 3:
            fmt += ' %b'
        else:
            fmt += ' %B'
        fmt += ' %Y'
        tmp = '{} {} {}'.format(x, y, z)
        return (m.start(), 
                m.end(),   
                datetime.datetime.strptime(tmp, fmt).date())
    return None

def find_pns(s, start_offset, have_pns):
    """Find a package name separator in a string, or ''"""
    s_len   = len(s)
    sep_len = 1
    # Find first digit
    i = start_offset
    i -= 1
    # Move back one more if v_ersion or r_elease
    if s[i].lower() in ['v', 'r']:
        i -= 1
        sep_len += 1
    # Return string
    sep = s[i:i+sep_len]
    if sep not in NAME_SEPS:
        if have_pns:
            ndo_start = i+sep_len+1
            if ndo_start >= s_len:
                return ''
            ndo = next_digit_offset(s, ndo_start)
            if ndo == -1 or ndo >= s_len:
                return ''
            else:
                return find_pns(s, ndo, have_pns)
        elif sep == '.':
            # Handle case "sendmail.8.14.x". We don't want '.' in NAME_SEPS
            # though - that makes the have_pns check worthless, since '.'
            # is usually version_sep
            return sep
        else:
            # Handle edge case where form is "ProFTPD1.3.3" or so
            return '' 
    else:
        return sep


def human_to_timedelta(s):
    days = 0
    months = 0
    years = 0
    s = s.lower().rstrip().lstrip()
    if str_is_all_digits(s):
        # If only digits, assume number of days
        return datetime.timedelta(int(s))
    pattern = r'\s*(\d+\s*[a-z]+\,?\s*)\s*(\d+\s*[a-z]+\,?\s*)?\s*(\d+\s*[a-z]+\,?\s*)?'
    m = re.match(pattern, s)
    if m:
        for g in m.groups():
            if g == None:
                break 
            clean = g.replace(' ', '')
            n = first_int(clean)
            char_offset = len(str(n))
            duration = clean[char_offset]
            if duration not in 'ymd':
                raise HumanDurationParseError(
                        "Couldn't interpret time spec '{}'".format(g))
            if duration == 'y':
                days += (n * 365)
            if duration == 'm':
                days += (n * 30)
            if duration == 'd':
                days += n
    else:
        raise HumanDurationParseError("invalid duration spec {}".format(s))
    return datetime.timedelta(days) 

def timedelta_to_human(delta):
    days = 0
    months = 0
    years = 0
    delta_days = delta.days     # readonly
    if type(delta) is not datetime.timedelta:
        raise TypeError("timedelta_to_human() arg must be datetime.timedelta")
    while delta_days >= 365:
        years += 1
        delta_days -= 365
    while delta_days >= 30:
        months += 1
        delta_days -= 30
    days = delta_days
    assert(days < 30)
    assert(days >= 0)
    s = ''
    if years:
        s += '{} {}'.format(years, pluralize('year', years))
    if months:
        if len(s):
            s += ', '
        s += '{} {}'.format(months, pluralize('month', months))
    if len(s) == 0 or days > 0:
        if len(s):
            s += ', '
        s += '{} {}'.format(days, pluralize('day', days))
    return s


########
# Exception classes
########

class VersionError(Exception):
    pass

class VersionNotComparableError(VersionError):
    """The two versions are not comparable."""

class VersionParseError(VersionError):
    """Failed to parse the version string."""

class VersionInitError(VersionError):
    """Failed to initialize the version instance."""

class HumanDurationParseError(VersionError):
    """Failed to parse the duration string."""


########
# Version class itself
########

class Version(object):

    # For mocking
    date_class = datetime.date

    # Used to represent "release_date not set", and still allow sorting
    timedelta_epoch = None      # set on __init__
    

    @classmethod
    def parse_patch(cls, patch):
        # Return a 3-tuple of these
        patch1 = None
        patch2 = None
        patch_str = None
        # MMMMM
        if patch is None:
            return (None, None, None)
        if type(patch) is int:
            return patch, None, None
        if type(patch) is not str and type(patch) is not unicode:
            raise TypeError("'patch' arg to _parse_patch() must be int or str/unicode")
        if patch == 'X' or patch == 'x':
            return (None, None, patch)
        # Patch parsing
        if patch[0] in string.digits:
            patch1 = first_int(patch)
            start_idx = len(str(patch1))
        else:
            start_idx = 0
        end_range = len(patch)
        # If all digits, whole patch is now in patch1
        # Next parse any trailing digits (e.g. "rc2")
        if not str_is_all_digits(patch): 
            # Either all non-digit trailing or there's a last_int
            if patch[-1] in string.digits:
                patch2 = last_int(patch) 
                end_range = len(patch) - len(str(patch2))
                # Handle 0 prefix
                if patch[end_range-1] == '0':
                    end_range -= 1
            patch_str = patch[ start_idx:end_range ]
        return (patch1, patch2, patch_str)

    # XXX Use ply if this becomes unmaintainable (it's close)
    @classmethod
    def parse(cls, s):
        """Parse a string into a Version object"""
        # Normalize whitespace - may break round-trip 
        # stringify, but probably ok, and eases parsing
        s = s.rstrip().lstrip()
        s = re.sub(r'\s+', ' ', s)  

        if not any_digits_in_str(s):
            raise VersionParseError("Version string '{}' contains no digits - this cannot be a version".format(s))

        # Figure out name separator 
        have_pns = find_any_in_seq(NAME_SEPS, s)
        first_digit_offset = next_digit_offset(s)
        name_sep = find_pns(s, first_digit_offset, have_pns)

        # Split into parts. At end of this, name and version must
        # be set, or we must have raised an exception.
        name = None
        version  = None
        parts    = [] 
        extra_str = None 
        # Handle edge case where form is "ProFTPD1.3.3" or so
        if name_sep == '': 
            parts.append( s[:first_digit_offset] )
            parts.append( s[first_digit_offset:] )
        else:
            parts = s.split(name_sep)

        # If > 2 parts and name_sep isn't space, we probably have
        # name_sep in the version string - rejoin it
        parts_len = len(parts)

        if parts_len > 2 and name_sep != ' ':
            parts[1] += name_sep + name_sep.join(parts[2:])
            del parts[2:]

        # This handles all the fucking weird cases
        if parts_len > 2 and name_sep == ' ':
            if not any_digits_in_str(parts[1]):
                parts[0] += ' ' + ' '.join(parts[1:parts_len-1])
                parts[1] = parts[-1]
            else:
                # Handle modem model names like LANCOM 1611+
                if '.' not in parts[1] and '_' not in parts[1] \
                    and '+' in parts[1]:
                    tmp = parts.pop(1)
                    parts_len -= 1
                    parts[0] = parts[0] + ' ' + tmp
                # Now assume part with most digits is the version,
                # anything before is part of name and anything
                # after goes in extra_str
                max_digits = 0
                max_digits_idx = -1
                for i in xrange(1, parts_len):
                    num_digits = len( set(parts[i]) & DIGITS_SET )
                    if num_digits > max_digits:
                        max_digits = num_digits
                        max_digits_idx = i
                assert(max_digits_idx != -1)
                assert(max_digits_idx > 0)
                add_parts_first = parts[1:max_digits_idx]
                add_parts_last  = parts[max_digits_idx+1:]
                if len(add_parts_first) > 0:
                    parts[0] += ' ' + ' '.join(add_parts_first)
                parts[1] = parts[max_digits_idx]
                if len(add_parts_last) > 0:
                    extra_str = ' '.join(add_parts_last)
            del parts[2:]

        # Get rid of spaces in pkg name, but save it first
        full_name = parts[0]

        # This is a good heuristic - remove everything
        # after first space, if present. Only name_sep != ' '
        # because split would remove that
        i = parts[1].find(' ')
        if i != -1: 
            extra_str = parts[1][i:]    # keep for round-trip str()
            parts[1] = parts[1][:i]

        # name, version string
        assert(len(parts) == 2)

        clean_name = parts[0].lower().replace(' ', '')
        version  = parts[1]
        version_len = len(version)
        offset = 0
        major = None
        minor = None
        patch = None
        version_sep  = None
        zero_pfx_major = False
        zero_pfx_minor = False
        release_date = None
        build_meta = None
        ver_date_start = None
        ver_date_end = None
        ver_date_str = None

        # Handle 'vX.Y', 'rX.Y'
        if version[0].lower() == 'v' or version[0].lower() == 'r':
            version = version[1:]

        # If there's a date string in the version string, move it to extra_str
        # so we can parse. 
        d = find_date(version)
        if d:
            ver_date_start, ver_date_end, release_date = d
            if version[ver_date_end] in '/-_.':
                ver_date_end += 1
            ver_date_str = version[ver_date_start:ver_date_end]
            version = version[:ver_date_start] + version[ver_date_end:]

        major = first_int(version)
        if major is None:
            raise VersionParseError("Couldn't get major version number")
        offset = len(str(major)) + 1
        if offset > version_len - 1:
            minor = None
        else:
            # If we have a minor version number, store the version sep.
            # Store here since 2nd sep can be a special case value
            version_sep = version[offset-1]
            # Then store minor
            if version[offset:offset+2].lower() == 'x'+version_sep \
                    or version[offset:].lower() == 'x':
                minor = version[offset]
            else:
                minor = first_int(version[offset:])
                if version[offset:offset+2] == '00':
                    zero_pfx_minor = True
                    offset += 1
                if version[offset:offset+1] == '0' and minor != 0:
                    zero_pfx_minor = True
            offset += len(str(minor)) + 1
        if offset > version_len - 1:
            patch = None
        else:
            patch = version[offset:version_len]
            # Handle extra shit instead of version sep
            if offset > 0 and version[offset-1] not in [version_sep, 'p']:
                patch = version[offset-1] + patch
            # Handle the special case OpenSSH X.YpZ - put the 'p' in patch 
            # level, since it's useful information (p=portable), and 
            # p and non-p OpenSSH versions can be meaningfully compared
            if offset > 0 and version[offset-1] == 'p':
                patch = 'p' + patch

        if extra_str:
            date_tuple = find_date(extra_str)
            if date_tuple:
                _, _, release_date = date_tuple

        assert(    clean_name is not None \
               and full_name is not None \
               and major    is not None \
               and name_sep is not None)

        if patch:
            plus_idx = patch.find('+')
            if plus_idx != -1:
                build_meta = patch[plus_idx+1:]
                patch = patch[:plus_idx]

        patch1, patch2, patch_str = Version.parse_patch(patch)
   
        obj = cls(full_name, major, minor,  
                release_date=release_date, 
                zero_pfx_major=zero_pfx_major, zero_pfx_minor=zero_pfx_minor,
                name_sep=name_sep, version_sep=version_sep,
                extra_str=extra_str, build_meta=build_meta)
        obj.name_clean = clean_name
        obj.patch1 = patch1
        obj.patch2 = patch2
        obj.patch_str = patch_str
        obj.patch  = patch
        obj.ver_date_start = ver_date_start
        obj.ver_date_end   = ver_date_end
        obj.ver_date_str   = ver_date_str
        return obj


    # TODO override assign to .patch to call _parse_patch() and save fields
    def __init__(self, name, major, 
                 minor=None, patch=None, release_date=None, eol_date=None,
                 build_meta=None,
                 zero_pfx_major=False, zero_pfx_minor=False,
                 name_sep=' ', version_sep='.',
                 extra_str=None):
        self.name      = name
        self.patch     = None
        self.patch1    = None
        self.patch2    = None
        self.patch_str = None
        self.extra_str = extra_str 
        self.release_date   = release_date
        self.build_meta     = build_meta
        self.eol_date       = eol_date
        self.name_sep       = name_sep
        self.version_sep    = version_sep 
        self.zero_pfx_major = zero_pfx_major 
        self.zero_pfx_minor = zero_pfx_minor
        self.name_clean     = None
        self.ver_date_start = None
        self.ver_date_end   = None
        self.ver_date_str   = None

        self.timedelta_epoch = self.date_class.today() \
                             - datetime.date(1970, 1, 1) \
                             + datetime.timedelta(1)

        if self.name_sep is None:
            self.name_sep = ''

        if type(major) is str or type(major) is unicode:
            major = int(major)
        if type(major) is not int:
            raise VersionInitError("Argument 'major' must be str or int")
        if major < 0:
                raise VersionInitError("Can't have negative number in version (major={})".format(major))
        self.major = major

        if minor is not None and self.version_sep is None:
            raise VersionInitError("Passed minor=(not None) and version_sep=None, that's a bit silly")
        if minor is not None and minor != 'x' and minor != 'X':
            if type(minor) is str:
                minor = int(minor)
            if type(minor) is not int:
                raise VersionInitError("Argument 'minor' must be str or int (or None)")
            if minor < 0:
                raise VersionInitError("Can't have negative number in version (minor={})".format(minor))
        self.minor = minor

        if patch is not None:
            self.patch1, self.patch2, self.patch_str = \
              Version.parse_patch(patch)
            # Ensure patch is always a str, even if just a single digit
            self.patch = str(patch)

    def __eq__(self, other):
        if self.name == other.name and \
           self.major == other.major and \
           self.minor == other.minor and \
           self.patch == other.patch:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.name != other.name:
            raise VersionNotComparableError(
                "Tried to compare versions for different packages, " \
              + "that doesn't make sense ({}/{})".format(
                  self.name, other.name)
            )
        if self.__eq__(other):
            return False
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        if self.minor > other.minor:
            return False

        # Patch 
        if self.patch1 == None and other.patch1 != None:
            return True
        if self.patch1 != None and other.patch1 == None:
            return False
        if self.patch1 != None and other.patch1 != None:
            if self.patch1 < other.patch1:
                return True
            if self.patch1 > other.patch1:
                return False

        # 2.6.10-rc1 < 2.6.10   (but careful about 3.0.65.1)
        if self.patch_str != self.version_sep and \
           other.patch_str != other.version_sep:
            if self.patch_str != None and other.patch_str == None:
                return True
            if self.patch_str == None and other.patch_str != None:
                return False
        
        # 3.0.65 < 3.0.65.1
        if self.patch2 == None and other.patch2 != None:
            return True
        if self.patch2 != None and other.patch2 == None:
            return False
        if self.patch2 != None and other.patch2 != None:
            if self.patch2 < other.patch2:
                return True
            if self.patch2 > other.patch2:
                return False
        raise Exception("can't happen")     # TODO debug only
        return False

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    
    def get_version_str(self):
        s = ''
        s += "{}{}".format(
                '0' if self.zero_pfx_major else '',
                self.major)
        if self.minor is not None:
            s += "{}{}{}".format(
                self.version_sep, 
                '0' if self.zero_pfx_minor else '',
                self.minor)
        if self.patch is not None:
            assert(type(self.patch) is str)
            vs = self.version_sep
            if self.patch[0] == 'p' or self.patch[0] in '-_':
                vs = ''
            if self.patch_str and self.patch_str.lower() in ['alpha', 'beta']:
                vs = ''
            s += "{}{}".format(vs, self.patch)
        if self.ver_date_str is not None:
            s = s[:self.ver_date_start] + \
                self.ver_date_str + \
                s[self.ver_date_start:]
        return s

    def __str__(self):
        s = "{}{}".format(
                self.name, 
                self.name_sep)
        s += self.get_version_str()
        if self.build_meta is not None:
            s += '+{}'.format(self.build_meta)
        if self.extra_str is not None:
            if self.extra_str[0] != ' ':
                s += ' '
            s += self.extra_str
        return s

    def __unicode__(self):
        return self.__str__()

    def __hash__(self):
        pass # TODO

    def __repr__(self):
        return self.__str__()   # TODO?


    def age(self):
        """Return a timedelta representing the age. If release_date is None,
           age will be more than number of days since the epoch (1970-1-1)."""
        if self.release_date is None:
            return self.timedelta_epoch 
        if type(self.release_date) is not datetime.date:
            raise TypeError(".age() called but release_date is not a datetime.date")
        return self.date_class.today() - self.release_date

    def age_human(self):
        if self.release_date is None:
            return 'none'
        return timedelta_to_human(self.age())

    # TODO let compare_to be a timedelta
    def is_older_than(self, compare_to):
        if self.release_date is None:
            raise RuntimeError("called is_older_than() when self.release_date is not set")
        if type(compare_to) is Version:
            if compare_to.release_date is None:
                raise RuntimeError("called is_older_than() when compare_to.release_date is not set")
            return self.release_date < compare_to.release_date
        if type(compare_to) is datetime.date:
            return self.release_date < compare_to
        if type(compare_to) is str or type(compare_to) is unicode:
            return self.age() > human_to_timedelta(compare_to)
        raise TypeError("bad type for compare_to() arg")

    def is_newer_than(self, compare_to):
        if self.release_date is None:
            raise RuntimeError("called is_newer_than() when self.release_date is not set")
        if type(compare_to) is Version:
            if compare_to.release_date is None:
                raise RuntimeError("called is_newer_than() when compare_to.release_date is not set")
            return self.release_date > compare_to.release_date
        if type(compare_to) is datetime.date:
            return self.release_date > compare_to
        if type(compare_to) is str or type(compare_to) is unicode:
            return self.age() < human_to_timedelta(compare_to)
        raise TypeError("bad type for compare_to() arg")

# TODO Semver subclass?
