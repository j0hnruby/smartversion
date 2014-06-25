# -*- coding: utf-8 -*-

import datetime
from datetime import date, timedelta
import random

from nose.tools import assert_raises

from .smartversion import (
        Version, 
        first_int, last_int, any_digits_in_str, str_is_all_digits, 
          find_any_in_seq, next_digit_offset, find_pns,
          find_date,
        human_to_timedelta, timedelta_to_human,
        VersionParseError, VersionNotComparableError,
)

today = date.today()

def test_helper():
    x = first_int('123')
    assert(type(x) is int)
    assert(x == 123)

    assert(first_int('123foo') == 123)
    assert(first_int('123456789a9') == 123456789)
    assert(first_int('123foobar456') == 123)
    assert(first_int('1a2') == 1)
    assert(first_int('0a2') == 0)
    assert(first_int('0 1') == 0)
    assert(first_int('9 8') == 9)

    x = last_int('123')
    assert(type(x) is int)
    assert(x == 123)

    assert(last_int('456foo123') == 123)
    assert(last_int('9a123456789') == 123456789)
    assert(last_int('1a2') == 2)
    assert(last_int('0a2') == 2)
    assert(last_int('0 1') == 1)
    assert(last_int('9 8') == 8)

    assert(any_digits_in_str('foo') is False)
    assert(any_digits_in_str('FOO') is False)
    assert(any_digits_in_str('1') is True)
    assert(any_digits_in_str('foo2') is True)
    assert(any_digits_in_str('SODI:HF:OIFD0') is True)
    assert(any_digits_in_str('765') is True)
    assert(any_digits_in_str('') is False)

    assert(str_is_all_digits('foo') is False)
    assert(str_is_all_digits('foo1') is False)
    assert(str_is_all_digits('1foo') is False)
    assert(str_is_all_digits('') is False)
    assert(str_is_all_digits('1') is True)
    assert(str_is_all_digits('123') is True)
    assert(str_is_all_digits('123.456') is False)

    assert(next_digit_offset('') == -1)
    assert(next_digit_offset('foo') == -1)
    assert(next_digit_offset('1') == 0)
    assert(next_digit_offset('foo1') == 3)
    assert(next_digit_offset('foo1', 4) == -1)
    assert(next_digit_offset('foo1bar2', 4) == 7)
    assert(next_digit_offset('foo1bar2', 7) == 7)
    assert(next_digit_offset('foo1bar2', 8) == -1)

    # TODO find_pns

    assert(find_date('20090110') == (0, 8, date(2009, 1, 10)))
    assert(find_date('19690110') is None)
    assert(find_date('30000110') is None)
    assert(find_date('20091330') is None)
    assert(find_date('20091232') is None)
    assert(find_date('19990110') == (0, 8, date(1999, 1, 10)))
    assert(find_date('19700101') == (0, 8, date(1970, 1, 1)))
    assert(find_date('29991231') == (0, 8, date(2999, 12, 31)))
    assert(find_date('20093112') == (0, 8, date(2009, 12, 31)))
    assert(find_date('20094512') is None)
    assert(find_date('20093113') is None)
    assert(find_date('01101999') == (0, 8, date(1999, 10, 1)))
    assert(find_date('01231999') == (0, 8, date(1999, 1, 23)))
    assert(find_date('2009-01-10') == (0, 10, date(2009, 1, 10)))
    assert(find_date('01-10-2009') == (0, 10, date(2009, 10, 1)))
    assert(find_date('01 Jan 2009') == (0, 11, date(2009, 1, 1)))
    assert(find_date('1 jan 2009')  == (0, 10, date(2009, 1, 1)))
    assert(find_date('jan 1, 2009')  == (0, 11, date(2009, 1, 1)))
    assert(find_date('01-Jan-2009') == (0, 11, date(2009, 1, 1)))
    assert(find_date('Jan 01, 2009') == (0, 12, date(2009, 1, 1)))
    assert(find_date('January 01, 2009') == (0, 16, date(2009, 1, 1)))
    assert(find_date('January 01 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('01 January 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('1 January 2009') == (0, 14, date(2009, 1, 1)))
    assert(find_date('January 1 2009') == (0, 14, date(2009, 1, 1)))
    assert(find_date('January 1, 2009') == (0, 15, date(2009, 1, 1)))
    assert(find_date('2009-Jan-01') == (0, 11, date(2009, 1, 1)))
    assert(find_date('1998-Aug-28') == (0, 11, date(1998, 8, 28)))
    assert(find_date('1970-January-31') == (0, 15, date(1970, 1, 31)))
    assert(find_date('2525 Dec 20') == (0, 11, date(2525, 12, 20)))
    assert(find_date('2999 May 8') == (0, 10, date(2999, 5, 8)))
    assert(find_date('9 Aug 09') == (0, 8, date(2009, 8, 9)))
    assert(find_date('18_Mar_81') == (0, 9, date(1981, 3, 18)))
    assert(find_date('29may2003') == (0, 9, date(2003, 5, 29)))
    assert(find_date('2003may29') == (0, 9, date(2003, 5, 29)))
    assert(find_date('libapreq 2012-06-13') == (9, 19, date(2012, 6, 13)))
    assert(find_date('3.0.77') is None)
    assert(find_date('2.6.10.77') is None)
    assert(find_date('mini_httpd/1.19 19dec2003') == (16, 25, date(2003, 12, 19)))
    assert(find_date('26may2002') == (0, 9, date(2002, 5, 26)))


    assert(human_to_timedelta('0') == timedelta(0))
    assert(human_to_timedelta('1') == timedelta(1))
    assert(human_to_timedelta('12345') == timedelta(12345))
    assert(human_to_timedelta('0d') == timedelta(0))
    assert(human_to_timedelta('1d') == timedelta(1))
    assert(human_to_timedelta('1 d') == timedelta(1))
    assert(human_to_timedelta('1 D') == timedelta(1))
    assert(human_to_timedelta('1 day') == timedelta(1))
    assert(human_to_timedelta('1y') == timedelta(365))
    assert(human_to_timedelta('1year') == timedelta(365))
    assert(human_to_timedelta('1 year') == timedelta(365))
    assert(human_to_timedelta('1Y') == timedelta(365))
    assert(human_to_timedelta('1 YEAR') == timedelta(365))
    assert(human_to_timedelta('1 YEAR') == timedelta(365))
    assert(human_to_timedelta('1y1d') == timedelta(366))
    assert(human_to_timedelta('1y,1d') == timedelta(366))
    assert(human_to_timedelta('1y10d') == timedelta(375))
    assert(human_to_timedelta('1y, 10d') == timedelta(375))
    assert(human_to_timedelta('1 year, 10 days') == timedelta(375))
    assert(human_to_timedelta('10 years') == timedelta(3650))
    assert(human_to_timedelta('10years') == timedelta(3650))
    assert(human_to_timedelta('10y') == timedelta(3650))
    assert(human_to_timedelta('1 y, 0m, 2 d') == timedelta(367))
    assert(human_to_timedelta('0d, 0m, 1y') == timedelta(365))
    assert(human_to_timedelta('0m, 1 years, 0d') == timedelta(365))
    assert(human_to_timedelta('1m') == timedelta(30))
    assert(human_to_timedelta('2m') == timedelta(60))
    assert(human_to_timedelta('6m') == timedelta(180))
    assert(human_to_timedelta('12m') == timedelta(360))
    assert(human_to_timedelta('24m') == timedelta(720))
    assert(human_to_timedelta('24m') == human_to_timedelta('1y11m25d'))
    assert(human_to_timedelta('1y12m') == human_to_timedelta('725d'))
    assert(human_to_timedelta('1d 1m 1y') == timedelta(396))
    assert(human_to_timedelta('1d 12m 1y') == timedelta(726))
    assert(human_to_timedelta('1d 12m 1y') == human_to_timedelta('726d'))
   
    assert(timedelta_to_human(timedelta(0)) == '0 days')
    assert(timedelta_to_human(timedelta(1)) == '1 day')
    assert(timedelta_to_human(timedelta(2)) == '2 days')
    assert(timedelta_to_human(timedelta(30)) == '1 month')
    assert(timedelta_to_human(timedelta(31)) == '1 month, 1 day')
    assert(timedelta_to_human(timedelta(59)) == '1 month, 29 days')
    assert(timedelta_to_human(timedelta(60)) == '2 months')
    assert(timedelta_to_human(timedelta(180)) == '6 months')
    assert(timedelta_to_human(timedelta(360)) == '12 months')
    assert(timedelta_to_human(timedelta(364)) == '12 months, 4 days')
    assert(timedelta_to_human(timedelta(365)) == '1 year')
    assert(timedelta_to_human(timedelta(366)) == '1 year, 1 day')
    assert(timedelta_to_human(timedelta(729)) == '1 year, 12 months, 4 days')
    assert(timedelta_to_human(timedelta(730)) == '2 years')
    assert(timedelta_to_human(timedelta(760)) == '2 years, 1 month')
    assert(timedelta_to_human(timedelta(789)) == '2 years, 1 month, 29 days')
    assert(timedelta_to_human(timedelta(3650)) == '10 years')

    h2td = human_to_timedelta
    td2h = timedelta_to_human
    assert(td2h( h2td('1y') ) == '1 year')
    assert(td2h( h2td('1y1m1d') ) == '1 year, 1 month, 1 day')
    assert(td2h( h2td('1y, 0 months, 20DAYS') ) == '1 year, 20 days')

    assert(h2td( td2h(timedelta(0)) ) == timedelta(0))
    assert(h2td( td2h(timedelta(1)) ) == timedelta(1))
    assert(h2td( td2h(timedelta(2)) ) == timedelta(2))
    assert(h2td( td2h(timedelta(30)) ) == timedelta(30))
    assert(h2td( td2h(timedelta(59)) ) == timedelta(59))
    assert(h2td( td2h(timedelta(180)) ) == timedelta(180))
    assert(h2td( td2h(timedelta(360)) ) == timedelta(360))
    assert(h2td( td2h(timedelta(365)) ) == timedelta(365))
    assert(h2td( td2h(timedelta(366)) ) == timedelta(366))
    assert(h2td( td2h(timedelta(719)) ) == timedelta(719))
    assert(h2td( td2h(timedelta(720)) ) == timedelta(720))
    assert(h2td( td2h(timedelta(724)) ) == timedelta(724))
    assert(h2td( td2h(timedelta(725)) ) == timedelta(725))
    assert(h2td( td2h(timedelta(730)) ) == timedelta(730))

def test_version_parse():
    # TODO specific semver tests, including build (+...)

    assert_raises(VersionParseError, Version.parse, 'OpenSSH')
    assert_raises(VersionParseError, Version.parse, 'OpenSSH-_ ')
    assert_raises(VersionParseError, Version.parse, 'foo x')

    s = 'OpenSSH 4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'OpenSSH')
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH_4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == '_')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH-4'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  is None)
    assert(str(v) == s) 

    s = 'OpenSSH 4.x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is str)
    assert(v.minor    == 'x')
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.X'
    v = Version.parse(s) 
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is str)
    assert(v.minor    == 'X')
    assert(v.patch    is None)
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.x.x'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is str)
    assert(v.minor    == 'x')
    assert(type(v.patch) is str)
    assert(v.patch    == 'x')
    assert(v.patch1   is None)
    assert(v.patch2   is None)
    assert(v.patch_str == 'x')
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 4.X.X'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is str)
    assert(v.minor    == 'X')
    assert(type(v.patch) is str)
    assert(v.patch    == 'X')
    assert(v.patch1   is None)
    assert(v.patch2   is None)
    assert(v.patch_str == 'X')
    assert(v.name_sep == ' ')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'sendmail.8.14.7'
    v = Version.parse(s)
    assert(v.name_clean == 'sendmail')
    assert(v.name     == 'sendmail')
    assert(v.major    == 8)
    assert(v.minor    == 14)
    assert(v.patch    == '7')
    assert(v.patch1   == 7)
    assert(type(v.patch1) is int)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s)

    s = 'Mercury POP3 server 1.48'
    v = Version.parse(s)
    assert(v.name_clean == 'mercurypop3server')
    assert(v.name     == 'Mercury POP3 server')
    assert(v.major    == 1)
    assert(v.minor    == 48)
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'Squid http proxy 3.0.STABLE20'
    v = Version.parse(s)
    assert(v.name_clean == 'squidhttpproxy')
    assert(v.name     == 'Squid http proxy')
    assert(v.major    == 3)
    assert(v.minor    == 0)
    assert(v.patch    == 'STABLE20')
    assert(v.patch1   is None)
    assert(v.patch_str == 'STABLE')
    assert(v.patch2   == 20)
    assert(str(v) == s)

    s = 'OpenSSH_4.3'
    v = Version.parse(s)
    assert(type(v.name_clean) is str)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 4)
    assert(type(v.minor) is int)
    assert(v.minor    == 3)
    assert(v.patch    is None)
    assert(v.patch_str is None)
    assert(v.name_sep == '_')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH_4.3'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(type(v.name_clean) is str)
    assert(v.major    == 4)
    assert(type(v.major) is int)
    assert(v.minor    == 3)
    assert(type(v.minor) is int)
    assert(v.patch    == None)
    assert(v.patch_str == None)
    assert(v.name_sep == '_')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH-4.3'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    == 3)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'Cisco-1.25'
    v = Version.parse(s)
    assert(v.name_clean == 'cisco')
    assert(v.name     == 'Cisco')
    assert(v.major    == 1)
    assert(v.minor    == 25)
    assert(type(v.minor) is int)
    assert(v.patch    is None)
    assert(v.name_sep == '-')
    assert(v.version_sep  == '.')
    assert(str(v) == s) 

    s = 'OpenSSH_6.2'
    v = Version.parse(s)
    assert(type(v.name_clean) is str)
    assert(v.name_clean == 'openssh')
    assert(type(v.major) is int)
    assert(v.major    == 6)
    assert(type(v.minor) is int)
    assert(v.minor    == 2)
    assert(str(v) == s) 

    s = 'OpenSSH_6.2p5'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 6)
    assert(v.minor    == 2)
    assert(type(v.patch) is str)
    assert(v.patch    == 'p5')
    assert(v.patch1   is None)
    assert(type(v.patch2) is int)
    assert(v.patch2   == 5)
    assert(v.patch_str == 'p')
    assert(str(v) == s) 

    s = 'OpenSSH_5.5p1 Debian-6+squeeze2'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 5)
    assert(v.minor    == 5)
    assert(v.patch    == 'p1')
    print str(v)
    assert(str(v) == s) 

    s = 'OpenSSH_4.3-HipServ'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.major    == 4)
    assert(v.minor    == 3)
    assert(v.patch    == '-HipServ')
    assert(str(v) == s) 

    s = 'ARRIS_0.44_01'
    v = Version.parse(s)
    assert(v.name_clean == 'arris')
    assert(v.major    == 0)
    assert(v.minor    == 44)
    assert(v.patch    == '_01')
    assert(v.patch1   is None)
    assert(v.patch_str == '_')
    assert(v.patch2   == 1)
    assert(str(v) == s) 

    s = 'ProFTPD1.3.3'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(v.patch    == '3')
    assert(v.patch1   == 3)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'linux-3.0.77'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.name     == 'linux')
    assert(v.major    == 3)
    assert(v.minor    == 0)
    assert(type(v.patch) is str)
    assert(v.patch    == '77')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 77)
    assert(str(v) == s) 

    s = 'linux-2.6.27.10'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(v.patch    == '27.10')
    assert(v.patch1   == 27)
    assert(v.patch2   == 10)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'OpenSSH 5.5p1 Debian 6+squeeze4 (protocol 2.0)'
    v = Version.parse(s)
    assert(v.name_clean == 'openssh')
    assert(v.name     == 'OpenSSH')
    assert(v.major    == 5)
    assert(v.minor    == 5)
    assert(v.patch    == 'p1')
    assert(v.patch1   is None)
    assert(v.patch2   == 1)
    assert(v.patch_str == 'p')
    print str(v)
    assert(str(v) == s) 

    s = 'lighttpd 1.4.23'
    v = Version.parse(s)
    assert(v.name_clean == 'lighttpd')
    assert(v.major    == 1)
    assert(v.minor    == 4)
    assert(v.patch    == '23')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 23)
    assert(v.patch2   is None)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'ProFTPD 1.3.3a'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(v.patch    == '3a')
    assert(v.patch1   == 3)
    assert(type(v.patch1) is int)
    assert(v.patch_str == 'a')
    assert(str(v) == s) 

    s = 'BetaFTPD 0.0.8pre17'
    v = Version.parse(s)
    assert(v.name_clean == 'betaftpd')
    assert(v.major    == 0)
    assert(v.minor    == 0)
    assert(v.patch    == '8pre17')
    assert(v.patch1   == 8)
    assert(v.patch2   == 17)
    assert(v.patch_str == 'pre')
    assert(str(v) == s) 

    s = 'linux-2.6.0-rc1'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(v.patch    == '0-rc1')
    assert(v.patch1   == 0)
    assert(v.patch2   == 1)
    assert(v.patch_str == '-rc')
    assert(str(v) == s) 

    s = 'linux-2.6.0-test4'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 6)
    assert(v.patch    == '0-test4')
    assert(v.patch1   == 0)
    assert(v.patch2   == 4)
    assert(v.patch_str == '-test')
    assert(str(v) == s) 

    s = 'Gene6 FTP Server v3.10.0'
    v = Version.parse(s)
    assert(v.name_clean == 'gene6ftpserver')
    assert(v.name     == 'Gene6 FTP Server')
    assert(v.major    == 3)
    assert(v.minor    == 10)
    assert(v.patch    == '0')
    assert(v.patch1   == 0)
    assert(v.patch2 is None)
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'IdeaWebServer httpd v0.70'
    v = Version.parse(s)
    assert(v.name_clean == 'ideawebserverhttpd')
    assert(v.name     == 'IdeaWebServer httpd')
    assert(v.major    == 0)
    assert(v.minor    == 70)
    assert(v.patch is None)
    assert(str(v) == s) 

    s = 'Multicraft 1.8.2 FTP server'
    v = Version.parse(s)
    assert(v.name_clean == 'multicraft')
    assert(v.major    == 1)
    assert(v.minor    == 8)
    assert(v.patch    == '2')
    assert(v.patch1   == 2)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'ProFTPD 1.3.3g Server'
    v = Version.parse(s)
    assert(v.name_clean == 'proftpd')
    assert(v.name     == 'ProFTPD')
    assert(v.major    == 1)
    assert(v.minor    == 3)
    assert(v.patch    == '3g')
    assert(v.patch1   == 3)
    assert(v.patch_str == 'g')
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Loxone FTP 5.66.4.23'
    v = Version.parse(s)
    assert(v.name_clean == 'loxoneftp')
    assert(v.name     == 'Loxone FTP')
    assert(v.major    == 5)
    assert(v.minor    == 66)
    assert(v.patch    == '4.23')
    assert(v.patch1   == 4)
    assert(v.patch2   == 23)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Exim smtpd 4.X'
    v = Version.parse(s)
    assert(v.name_clean == 'eximsmtpd')
    assert(v.name     == 'Exim smtpd')
    assert(v.major    == 4)
    assert(v.minor    == 'X')
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'MikroTik router ftpd 5.7'
    v = Version.parse(s)
    assert(v.name_clean == 'mikrotikrouterftpd')
    assert(v.name     == 'MikroTik router ftpd')
    assert(v.major    == 5)
    assert(v.minor    == 7)
    assert(v.patch    is None)
    assert(str(v) == s)

    s = 'Dropbear sshd 0.51'
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'RapidLogic httpd 1.1'
    v = Version.parse(s)
    assert(str(v) == s)

    s = 'MySQL 5.0.91-log'
    v = Version.parse(s)
    assert(v.name_clean == 'mysql')
    assert(v.major    == 5)
    assert(v.minor    == 0)
    assert(v.patch    == '91-log')
    assert(v.patch1   == 91)
    assert(v.patch_str == '-log')
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Foowizard 12.1.99900.0'
    v = Version.parse(s)
    assert(v.name_clean == 'foowizard')
    assert(v.major    == 12)
    assert(v.minor    == 1)
    assert(v.patch    == '99900.0')
    assert(v.patch1   == 99900)
    assert(v.patch2   == 0)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Task Manager Pro 2.0245'
    v = Version.parse(s)
    assert(v.name_clean == 'taskmanagerpro')
    assert(v.name     == 'Task Manager Pro')
    assert(v.major    == 2)
    assert(v.minor    == 245)
    assert(v.patch    is None)
    assert(v.zero_pfx_minor == True)
    assert(str(v) == s) 

    s = 'Internet Download Helper 8.22.0.1234'
    v = Version.parse(s)
    assert(v.name_clean == 'internetdownloadhelper')
    assert(v.major    == 8)
    assert(v.minor    == 22)
    assert(v.patch    == '0.1234')
    assert(v.patch1   == 0)
    assert(v.patch2   == 1234)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'Apache/2'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.major    == 2)
    assert(v.minor    is None)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Linux/2.x'
    v = Version.parse(s)
    assert(v.name_clean == 'linux')
    assert(v.major    == 2)
    assert(v.minor    == 'x')
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'PHP/5.2.9-1'
    v = Version.parse(s)
    assert(v.name_clean == 'php')
    assert(v.major    == 5)
    assert(v.minor    == 2)
    assert(v.patch    == '9-1')
    assert(v.patch1   == 9)
    assert(v.patch2   == 1)
    assert(v.patch_str == '-')
    assert(str(v) == s) 

    s = 'lighttpd/1.4.28-devel-4979'
    v = Version.parse(s)
    assert(v.name_clean == 'lighttpd')
    assert(v.major    == 1)
    assert(v.minor    == 4)
    assert(v.patch    == '28-devel-4979')
    assert(v.patch1   == 28)
    assert(v.patch2   == 4979)
    assert(v.patch_str == '-devel-')
    assert(str(v) == s) 

    s = 'Apache/2.2.18'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.name     == 'Apache')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == '18')
    assert(v.patch1   == 18)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(str(v) == s) 

    s = 'Apache/2_2_18'
    v = Version.parse(s)
    assert(v.name_clean == 'apache')
    assert(v.name     == 'Apache')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == '18')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 18)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'Microsoft-IIS/6.0'
    v = Version.parse(s)
    assert(v.name_clean == 'microsoft-iis')
    assert(v.name     == 'Microsoft-IIS')
    assert(v.major    == 6)
    assert(v.minor    == 0)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Virata-EmWeb/R6_0_1'
    v = Version.parse(s)
    assert(v.name_clean == 'virata-emweb')
    assert(v.major    == 6)
    assert(v.minor    == 0)
    assert(v.patch    == '1')
    assert(type(v.patch1) is int)
    assert(v.patch1   == 1)
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'IdeaWebServer/v0.80'
    v = Version.parse(s)
    assert(v.name_clean == 'ideawebserver')
    assert(v.name     == 'IdeaWebServer')
    assert(v.major    == 0)
    assert(v.minor    == 80)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'mod_ssl/2.2.18'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_ssl')
    assert(v.major    == 2)
    assert(v.minor    == 2)
    assert(v.patch    == '18')
    assert(v.patch_str is None)
    assert(str(v) == s) 

    s = 'Gemtek/0.899'
    v = Version.parse(s)
    assert(v.name_clean == 'gemtek')
    assert(v.major    == 0)
    assert(v.minor    == 899)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'OpenSSL/1.0.0-fips'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 1)
    assert(v.minor    == 0)
    assert(v.patch    == '0-fips')
    assert(v.patch1   == 0)
    assert(v.patch_str == '-fips')
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'KM-MFP-http/V0.0.1'
    v = Version.parse(s)
    assert(v.name_clean == 'km-mfp-http')
    assert(v.name     == 'KM-MFP-http')
    assert(v.major    == 0)
    assert(v.minor    == 0)
    assert(v.patch    == '1')
    assert(str(v) == s) 

    s = 'PHP/4.4.4-8+etch6'
    v = Version.parse(s)
    assert(v.name_clean == 'php')
    assert(v.major    == 4)
    assert(v.minor    == 4)
    assert(v.patch    == '4-8')
    assert(v.patch1   == 4)
    assert(v.patch2   == 8)
    assert(v.patch_str == '-')
    assert(v.build_meta == 'etch6')
    assert(str(v) == s) 

    s = 'IP_SHARER WEB 1.0'
    v = Version.parse(s)
    assert(v.name_clean == 'ip_sharerweb')
    assert(v.name     == 'IP_SHARER WEB')
    assert(v.major    == 1)
    assert(v.minor    == 0)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'mod_auth_passthrough/2.1'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_auth_passthrough')
    assert(v.name     == 'mod_auth_passthrough')
    assert(v.major    == 2)
    assert(v.minor    == 1)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'FrontPage/5.0.2.2635'
    v = Version.parse(s)
    assert(v.name_clean == 'frontpage')
    assert(v.major    == 5)
    assert(v.minor    == 0)
    assert(v.patch    == '2.2635')
    assert(v.patch1   == 2)
    assert(v.patch2   == 2635)
    assert(v.patch_str == '.')
    assert(str(v) == s) 

    s = 'OpenSSL/0.9.8r'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 0)
    assert(v.minor    == 9)
    assert(v.patch    == '8r')
    assert(v.patch1   == 8)
    assert(v.patch_str == 'r')
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'mod_apreq2-20090110/2.7.1'
    v = Version.parse(s)
    assert(v.name_clean == 'mod_apreq2')
    assert(v.name     == 'mod_apreq2')
    assert(v.major    == 2)
    assert(v.minor    == 7)
    assert(v.patch    == '1')
    assert(v.patch1   == 1)
    assert(v.patch_str is None)
    assert(v.patch2 is None)
    assert(v.release_date == date(2009, 01, 10))
    assert(str(v) == s) 

    s = 'mini_httpd/1.19 19dec2003'
    v = Version.parse(s)
    assert(v.name_clean == 'mini_httpd')
    assert(v.major    == 1)
    assert(v.minor    == 19)
    assert(v.patch    is None)
    assert(v.release_date == date(2003, 12, 19))
    assert(str(v) == s) 

    s = 'Allegro-Software-RomPager/4.34'
    v = Version.parse(s)
    assert(v.name_clean == 'allegro-software-rompager')
    assert(v.major    == 4)
    assert(v.minor    == 34)
    assert(v.patch    is None)
    assert(str(v) == s) 

    s = 'Foobar 8.00.162'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.name     == 'Foobar')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_pfx_minor)
    assert(v.patch    == '162')
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'Foobar 8.00.0162'
    v = Version.parse(s)
    assert(v.name_clean == 'foobar')
    assert(v.name     == 'Foobar')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_pfx_minor)
    assert(v.patch    == '0162')
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 

    s = 'LANCOM 1611+ 8.0.162'
    v = Version.parse(s)
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.patch    == '162')
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    #assert(str(v) == s)    # TODO ???

    s = 'LANCOM 1611+ 8.00.162'
    v = Version.parse(s)
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_pfx_minor)
    assert(v.patch    == '162')
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    #assert(str(v) == s)        # TODO

    s = 'LANCOM 1611+ 8.00.0162 / 16.06.2010'
    v = Version.parse(s)
    assert(v.release_date == date(2010, 06, 16))
    assert(v.name_clean == 'lancom1611+')
    assert(v.name     == 'LANCOM 1611+')
    assert(v.major    == 8)
    assert(v.minor    == 0)
    assert(v.zero_pfx_minor)
    assert(v.patch    == '0162')
    assert(v.patch1   == 162)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(v.release_date == date(2010, 6, 16))
    #assert(str(v) == s)        # TODO

    s = 'OpenSSL/0.9.8e-fips-rhel5'
    v = Version.parse(s)
    assert(v.name_clean == 'openssl')
    assert(v.major    == 0)
    assert(v.minor    == 9)
    assert(v.patch    == '8e-fips-rhel5')
    assert(v.patch1   == 8)
    assert(v.patch_str == 'e-fips-rhel')
    assert(v.patch2   == 5)     # Even though that's not ideal
    assert(str(v) == s) 

    s = 'Sun-ONE-ASP/4.0.3'
    v = Version.parse(s)
    assert(v.name_clean == 'sun-one-asp')
    assert(v.major    == 4)
    assert(v.minor    == 0)
    assert(v.patch    == '3')
    assert(v.patch1   == 3)
    assert(v.patch_str is None)
    assert(v.patch2   is None)
    assert(str(v) == s) 

    s = 'thttpd/2.23beta1 26may2002'
    v = Version.parse(s)
    assert(v.name_clean == 'thttpd')
    assert(v.major    == 2)
    assert(v.minor    == 23)
    assert(v.patch    == 'beta1')
    assert(v.patch1   is None)
    assert(v.patch2   == 1)
    assert(v.patch_str == 'beta')
    assert(v.release_date == date(2002, 5, 26))
    assert(str(v) == s) 

    s = 'Foobar 3 (FB3-DX) 1.90.26'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'ProTools Basic Edition 5.0 Build 11'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Fiddlesticks 2.0 Beta 2'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'IDA 5.19.1.1387.2314'
    #v = Version.parse(s)
    #assert(str(v) == s) 
    s = 'IDA 5.19.1.1387.2314.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 
    s = 'IDA 5.19.1.1387.2314.0.1352135'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'example Cyrus POP3 v2.2.13-Debian-2.2.13-14+lenny3 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'example.org POP MDaemon 9.0.4'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'POP3 Bigfoot v1.0 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'IMail 8.05 4000-1'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'IdeaPop3Server v0.80'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'example.example Cyrus POP3 v2.3.7-Invoca-RPM-2.3.7-12.el5_7.2 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Qpopper (version 4.0.5)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'example.org POP3 MDaemon 13.0.5'
    ##v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'example Cyrus POP3 v2.2.12 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'CommuniGate Pro POP3 Server 5.4.10'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = ' example.org IceWarp 10.2.2 POP3'
    ##v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'POP3 on WinWebMail [3.8.1.3]'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Microsoft Exchange Server 2003 POP3 <A6><F8><AA>A<BE><B9><AA><A9><A5><BB> 6.5.7638.1 (example.local)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Microsoft Windows POP3 Service Version 1.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Microsoft Exchange 2000 POP3 server version 6.0.6249.0 (example.example.org)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Cyrus POP3 v2.2.13-Debian-2.2.13-19 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'X1 NT-POP3 Server mail.example.org (IMail 8.03 304911-2)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Kerio Connect 8.0.1 POP3 server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Welcome to RaidenMAILD POP3 service v2205'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Lotus Notes POP3 server version Release 8.5.3'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'X1 NT-POP3 Server example.org (IMail 9.23 64609-2757)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'IceWarp 10.3.5 RHEL5 POP3'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'XMail 1.27 POP3 Server'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Intoto Http Server v1.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Apache/2.2.15 (CentOS)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'mod_gzip/1.3.26.1a'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'mod_perl/1.29'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'DIR-600 Ver 2.11'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'mini_httpd/1.19 19dec2003'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Embedthis-Appweb/3.3.1'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Boa/0.94.14rc21'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'MailEnable-HTTP/5.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    # Fuck you Zope
    s = 'Zope/(Zope 2.11.4-final, python 2.5.4, linux2) ZServer/1.1'

    s = 'Mathopd/1.5p6'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'PHP/5.2.6-1+lenny15 with Suhosin-Patch'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'squid/2.7.STABLE9'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'lighttpd/1.4.26-devel-6243M'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Winstone Servlet Engine v0.9.10'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'PHP/5.3.10-1ubuntu3.11'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'F6D4630-4-v2/1.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'thttpd/2.25b 29dec2003'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Jetty(8.y.z-SNAPSHOT)'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    s = 'Microsoft-HTTPAPI/2.0'
    #v = Version.parse(s)
    #assert(str(v) == s) 

    #s = 'GlassFish Server Open Source Edition  4.0'
    #v = Version.parse(s)
    #assert(v.name_clean == 'glassfishserveropensourceedition') # ergh
    #assert(v.name    == 'GlassFish Server Open Source Edition')
    #assert(v.major   == 4)
    #assert(v.minor   == 0)
    #assert(v.patch   is None)
    #assert(str(v) == s) 

    #s = 'David-WebBox/11.00a (0717)'
    #v = Version.parse(s)
    #assert(v.name_clean == 'david-webbox')
    #assert(v.name     == 'David-WebBox')
    #assert(v.major    == 11)
    #assert(v.minor    == 0)
    #assert(v.patch    == 'a')
    #assert(v.patch1   is None)
    #assert(v.patch2   is None)
    #assert(v.patch_str == 'a')
    #assert(v.extra_str == ' (0717)')
    #assert(str(v) == s) 

    s = 'VOD server/4.9.0.01 (Unix)'
    v = Version.parse(s)
    # TODO extra str
    #assert(str(v) == s) 

    s = 'Boa/0.94.13-20100727-114000'
    v = Version.parse(s)
    assert(v.name_clean == 'boa')
    assert(v.name     == 'Boa')
    assert(v.major    == 0)
    assert(v.minor    == 94)
    assert(v.patch    == '13-114000')
    assert(v.patch1   == 13)
    assert(v.patch2   == 114000)
    assert(v.patch_str == '-')
    assert(str(v) == s) 

    s = 'distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))'  # TODO
    #v = Version.parse(s)
    #assert(v.name_clean == 'distccd v1')
    #assert(v.name    == 'distccdv1')
    #assert(v.major   == 4)
    #assert(v.minor   == 2)
    #assert(v.patch   == '4')
    #assert(v.patch1  == 4)
    #assert(v.patch_str is None)
    #assert(v.patch2    is None)
    #assert(str(v) == s) 

    s = 'ISC BIND 9.4.2'
    v = Version.parse(s)
    assert(v.name_clean == 'iscbind')
    assert(v.name     == 'ISC BIND')
    assert(v.major    == 9)
    assert(v.minor    == 4)
    assert(v.patch    == '2')
    assert(v.patch1   == 2)
    assert(v.patch_str is None)
    assert(v.patch2    is None)
    assert(str(v) == s) 
    
    s = 'Apache Tomcat/Coyote JSP engine 1.1'   # TODO
    #v = Version.parse(s)
    #assert(str(v) == s) 


def test_compare():
    compare = lambda l: l[0] == l[1]

    # Equalities
    v1 = Version('foo', 1)
    v2 = Version('foo', 1)
    assert(v1 == v2)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 1)
    assert(v1 == v2)

    v1 = Version('foo', 1, 1, '1')
    v2 = Version('foo', 1, 1, '1')
    assert(v1 == v2)

    v1 = Version('foo', 1, 1, '1rc')
    v2 = Version('foo', 1, 1, '1rc')
    assert(v1 == v2)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 1, '1rc1')
    assert(v1 == v2)

    v1 = Version('foo', 1, 1, 'rc1')
    v2 = Version('foo', 1, 1, 'rc1')
    assert(v1 == v2)

    v1 = Version('foo', 1, 1, 'rc')
    v2 = Version('foo', 1, 1, 'rc')
    assert(v1 == v2)

    v1.extra_str = 'asd'
    v2.extra_str = 'lkj'
    assert(v1 == v2)

    v1.release_date = date(2000, 1, 1)
    v2.release_date = date(2000, 1, 2)
    assert(v1 == v2)

    v1.build_meta = 'lkasdjf'
    v2.build_meta = ';KFJDAa'
    assert(v1 == v2)

    # Inequalities
    v1 = Version('foo', 1)
    v2 = Version('foo', 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 1)
    v2 = Version('foo', 1, 1, 2)
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, '1test')
    v2 = Version('foo', 1, 1, '1frob')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, '1test5')
    v2 = Version('foo', 1, 1, '1test6')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 'test5')
    v2 = Version('foo', 1, 1, 'test6')
    assert(v1 != v2)
    assert(v2 != v1)

    v1 = Version('foo', 1, 1, 'test')
    v2 = Version('foo', 1, 1, 'frob')
    assert(v1 != v2)
    assert(v2 != v1)

    # Ordering
    v1 = Version('foo', 1)
    v2 = Version('foo', 2)
    assert(v1 < v2)

    v1 = Version('foo', 1, None)
    v2 = Version('foo', 1, 1)
    assert(v1 < v2)

    v1 = Version('foo', 1, 1)
    v2 = Version('foo', 1, 2)
    assert(v1 < v2)

    v1 = Version('foo', 1, 2)
    v2 = Version('foo', 2, 1)
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, 1)
    v2 = Version('foo', 1, 1, 2)
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, 2)
    v2 = Version('foo', 1, 2, 1)
    assert(v1 < v2)

    v1 = Version('foo', 1, 2, 1)
    v2 = Version('foo', 2, 1, 1)
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, 'rc0')
    v2 = Version('foo', 1, 1, 'rc1')
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, '1-rc1')
    v2 = Version('foo', 1, 1, 1)
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, 'rc0')
    v2 = Version('foo', 1, 1, '1rc0')
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, '1rc0')
    v2 = Version('foo', 1, 1, '1rc1')
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 1, '2rc0')
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, '1rc1')
    v2 = Version('foo', 1, 2, '1rc1')
    assert(v1 < v2)

    v1 = Version('foo', 1, 2, '1rc1')
    v2 = Version('foo', 2, 1, '1rc1')
    assert(v1 < v2)

    v1 = Version('foo', 1, 1, 'rc1')
    v2 = Version('foo', 1, 1)
    assert(v1 < v2)

    # Normal usage
    v1 = Version.parse('linux-2.4.6')
    v2 = Version.parse('linux-2.4.8')
    v3 = Version.parse('linux-2.4.10-rc1')      # rc < version proper
    v4 = Version.parse('linux-2.4.10')
    v5 = Version.parse('linux-2.6.27.10')
    v6 = Version.parse('linux-2.6.27.11')
    v7 = Version.parse('linux-3.0')
    v8 = Version.parse('linux-3.0.1')
    v9 = Version.parse('linux-3.0.65')
    v10 = Version.parse('linux-3.0.65.1')
    v11 = Version.parse('linux-4.x')
    v12 = Version.parse('linux-5.X')

    assert(v1 < v2)
    assert(v2 > v1)
    assert(v1 != v2)
    assert(v2 != v1)

    # Make sure rc compare ABOVE lower version without patch_str
    assert(v2 < v3)
    assert(v3 > v2)
    assert(v2 != v3)
    assert(v3 != v2)

    assert(v3 < v4)
    assert(v4 > v3)
    assert(v3 != v4)
    assert(v4 != v3)

    assert(v4 < v5)
    assert(v5 > v4)
    assert(v4 != v5)
    assert(v5 != v4)

    assert(v5 < v6)
    assert(v6 > v5)
    assert(v5 != v6)
    assert(v6 != v5)

    assert(v6 < v7)
    assert(v7 > v6)
    assert(v6 != v7)
    assert(v7 != v6)

    assert(v7 < v8)
    assert(v8 > v7)
    assert(v7 != v8)
    assert(v8 != v7)

    assert(v8 < v9)
    assert(v9 > v8)
    assert(v8 != v9)
    assert(v9 != v8)

    assert(v9 < v10)
    assert(v10 > v9)
    assert(v9 != v10)
    assert(v10 != v9)
    
    assert(v10 < v11)
    assert(v11 > v10)
    assert(v10 != v11)
    assert(v11 != v10)

    assert(v11 < v12)
    assert(v12 > v11)
    assert(v11 != v12)
    assert(v12 != v11)

    l = sorted([v12, v11, v10, v9, v8, v7, v6, v5, v4, v3, v2, v1])
    for i in xrange(10):
        assert(l[0] == v1)
        assert(l[1] == v2)
        assert(l[2] == v3)
        assert(l[3] == v4)
        assert(l[4] == v5)
        assert(l[5] == v6)
        assert(l[6] == v7)
        assert(l[7] == v8)
        assert(l[8] == v9)
        assert(l[9] == v10)
        assert(l[10] == v11)
        assert(l[11] == v12)
        random.shuffle(l)
        l.sort()

def test_methods():
    class MyDate(date):
        @staticmethod
        def today():
            return date(2000, 2, 1)
    Version.date_class = MyDate

    #### .age()
    v1 = Version('foo', 1, 0, release_date=date(2000, 1, 1))
    assert(v1.age() == timedelta(31))
    assert(v1.age_human() == '1 month, 1 day')

    v2 = Version('foo', 1, 0, release_date=date(2000, 2, 1))
    assert(v2.age() == timedelta(0))
    assert(v2.age_human() == '0 days')

    v3 = Version('foo', 1, 0)
    assert(v3.age() > timedelta(10988))
    assert(v3.age_human() == 'none')

    v4 = Version('foo', 1, 0, release_date=date(1970, 1, 1)) 
    assert(v4.age() == timedelta(10988)) 
    assert(v4.age_human() == '30 years, 1 month, 8 days')

    #dup
    v5 = Version('foo', 1, 0, release_date=date(2000, 1, 1))
    assert(v5.age_human() == '1 month, 1 day')

    l = sorted([v2, v1, v5, v4, v3], key=lambda x: x.age())
    assert(l[0] == v2)
    assert(l[1] == v1)
    assert(l[2] == v5)
    assert(l[3] == v4)
    assert(l[4] == v3)

    v1 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    assert(v1.is_older_than('1m'))
    assert(v1.is_older_than('12m4d'))
    assert(v1.is_older_than('1y') is False)
    assert(v1.is_newer_than('2y'))
    assert(v1.is_newer_than('1y1d'))
    assert(v1.is_newer_than('1y') is False)
    assert(v1.is_newer_than('12m4d') is False)

    v1 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    v2 = Version('foo', 1, 1, release_date=date(1999, 3, 1))
    assert(v2.is_newer_than(v1))
    assert(v1.is_older_than(v2))

    assert(v1.is_older_than(date(1999, 2, 2)))
    assert(v1.is_older_than(date(1999, 2, 1)) is False)
    assert(v1.is_newer_than(date(1998, 2, 2)))
    assert(v1.is_newer_than(date(1999, 2, 1)) is False)

    v1 = Version('foo', 1, 1, release_date=date(2000, 2, 1))
    assert(v1.is_older_than('0d') is False)

    v1.release_date = date(2000, 1, 31)
    assert(v1.is_older_than('0d'))
    assert(v1.is_newer_than('1d') is False)
    assert(v1.is_older_than('1d') is False)
    assert(v1.is_newer_than('1d') is False)

    v1.release_date = date(2000, 1, 1)
    assert(v1.is_older_than('1m'))
    assert(v1.is_older_than('30d'))
    assert(v1.is_older_than('31d') is False)
    assert(v1.is_newer_than('32d'))
    assert(v1.is_newer_than('31d') is False)

    v1.release_date = date(1999, 2, 1)
    v2 = Version('foo', 1, 1, release_date=date(1999, 2, 1))
    assert(v1.is_older_than(v2) is False)
    assert(v1.is_newer_than(v2) is False)
    assert(v2.is_older_than(v1) is False)
    assert(v2.is_newer_than(v1) is False)

    v2.release_date = date(1999, 2, 2)
    assert(v1.is_older_than(v2))
    assert(v2.is_older_than(v1) is False)
    assert(v2.is_newer_than(v1))
    assert(v1.is_newer_than(v2) is False)

    v1 = Version('foo', 1, 1, release_date=date(1990, 2, 1))
    assert(v1.is_older_than('10y2d') is False)
    assert(v1.is_newer_than('10y2d') is False)
    assert(v1.is_newer_than('10y3d'))
    assert(v1.is_older_than('10y1d'))
