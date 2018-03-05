

from __future__ import division
from datetime import date, datetime, time, timedelta, tzinfo
from calendar import timegm
import re

from pytz import timezone, utc
import six

# try:
#     from inspect import signature
# except ImportError:  # pragma: nocover
#     from funcsigs import signature

try:
    from threading import TIMEOUT_MAX
except ImportError:
    TIMEOUT_MAX = 4294967  # Maximum value accepted by Event.wait() on Windows

# __all__ = ('asint', 'asbool', 'astimezone', 'convert_to_datetime', 'datetime_to_utc_timestamp',
#            'utc_timestamp_to_datetime', 'timedelta_seconds', 'datetime_ceil', 'get_callable_name',
#            'obj_to_ref', 'ref_to_obj', 'maybe_ref', 'repr_escape', 'check_callable_args')


class _Undefined(object):
    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '<undefined>'


undefined = _Undefined()  #: a unique object that only signifies that no value is defined

class JobLookupError(KeyError):
    def __init__(self, job_id):
        super(JobLookupError, self).__init__(u'No job by the id of %s was found' % job_id)


class ConflictingIdError(KeyError):
    def __init__(self, job_id):
        super(ConflictingIdError, self).__init__(
            u'Job identifier (%s) conflicts with an existing job' % job_id)
        

def asint(text):
    """
    Safely converts a string to an integer, returning ``None`` if the string is ``None``.

    :type text: str
    :rtype: int

    """
    if text is not None:
        return int(text)


def asbool(obj):
    """
    Interprets an object as a boolean value.

    :rtype: bool

    """
    if isinstance(obj, str):
        obj = obj.strip().lower()
        if obj in ('true', 'yes', 'on', 'y', 't', '1'):
            return True
        if obj in ('false', 'no', 'off', 'n', 'f', '0'):
            return False
        raise ValueError('Unable to interpret value "%s" as boolean' % obj)
    return bool(obj)


def astimezone(obj):
    """
    Interprets an object as a timezone.

    :rtype: tzinfo

    """
    if isinstance(obj, six.string_types):
        return timezone(obj)
    if isinstance(obj, tzinfo):
        if not hasattr(obj, 'localize') or not hasattr(obj, 'normalize'):
            raise TypeError('Only timezones from the pytz library are supported')
        if obj.zone == 'local':
            raise ValueError(
                'Unable to determine the name of the local timezone -- you must explicitly '
                'specify the name of the local timezone. Please refrain from using timezones like '
                'EST to prevent problems with daylight saving time. Instead, use a locale based '
                'timezone name (such as Europe/Helsinki).')
        return obj
    if obj is not None:
        raise TypeError('Expected tzinfo, got %s instead' % obj.__class__.__name__)


_DATE_REGEX = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
    r'(?: (?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})'
    r'(?:\.(?P<microsecond>\d{1,6}))?)?')


def convert_to_datetime(input, tz, arg_name):
    """
    Converts the given object to a timezone aware datetime object.

    If a timezone aware datetime object is passed, it is returned unmodified.
    If a native datetime object is passed, it is given the specified timezone.
    If the input is a string, it is parsed as a datetime with the given timezone.

    Date strings are accepted in three different forms: date only (Y-m-d), date with time
    (Y-m-d H:M:S) or with date+time with microseconds (Y-m-d H:M:S.micro).

    :param str|datetime input: the datetime or string to convert to a timezone aware datetime
    :param datetime.tzinfo tz: timezone to interpret ``input`` in
    :param str arg_name: the name of the argument (used in an error message)
    :rtype: datetime

    """
    if input is None:
        return
    elif isinstance(input, datetime):
        datetime_ = input
    elif isinstance(input, date):
        datetime_ = datetime.combine(input, time())
    elif isinstance(input, six.string_types):
        m = _DATE_REGEX.match(input)
        if not m:
            raise ValueError('Invalid date string')
        values = [(k, int(v or 0)) for k, v in m.groupdict().items()]
        values = dict(values)
        datetime_ = datetime(**values)
    else:
        raise TypeError('Unsupported type for %s: %s' % (arg_name, input.__class__.__name__))

    if datetime_.tzinfo is not None:
        return datetime_
    if tz is None:
        raise ValueError(
            'The "tz" argument must be specified if %s has no timezone information' % arg_name)
    if isinstance(tz, six.string_types):
        tz = timezone(tz)

    try:
        return tz.localize(datetime_, is_dst=None)
    except AttributeError:
        raise TypeError(
            'Only pytz timezones are supported (need the localize() and normalize() methods)')


def datetime_to_utc_timestamp(timeval):
    """
    Converts a datetime instance to a timestamp.

    :type timeval: datetime
    :rtype: float

    """
    if timeval is not None:
        print timeval.utctimetuple()
        print timeval.microsecond
        return timegm(timeval.utctimetuple()) + timeval.microsecond / 1000000


def utc_timestamp_to_datetime(timestamp):
    """
    Converts the given timestamp to a datetime instance.

    :type timestamp: float
    :rtype: datetime

    """
    if timestamp is not None:
        return datetime.fromtimestamp(timestamp,utc)


def timedelta_seconds(delta):
    """
    Converts the given timedelta to seconds.

    :type delta: timedelta
    :rtype: float

    """
    return delta.days * 24 * 60 * 60 + delta.seconds + \
        delta.microseconds / 1000000.0


def datetime_ceil(dateval):
    """
    Rounds the given datetime object upwards.

    :type dateval: datetime

    """
    if dateval.microsecond > 0:
        return dateval + timedelta(seconds=1, microseconds=-dateval.microsecond)
    return dateval


def datetime_repr(dateval):
    return dateval.strftime('%Y-%m-%d %H:%M:%S %Z') if dateval else 'None'



 
 
if six.PY2:
    def repr_escape(string):
        if isinstance(string, six.text_type):
            return string.encode('ascii', 'backslashreplace')
        return string
else:
    def repr_escape(string):
        return string
 
 

