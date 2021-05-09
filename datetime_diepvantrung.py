import math as _math
from datetime import timedelta

class timedelta_custom(timedelta):
    """Represent the difference between two datetime objects.
    Supported operators:
    - add, subtract timedelta
    - unary plus, minus, abs
    - compare to timedelta
    - multiply, divide by int
    In addition, datetime supports subtraction of two datetime objects
    returning a timedelta, and addition or subtraction of a datetime
    and a timedelta giving a datetime.
    Representation: (days, seconds, microseconds).  Why?  Because I
    felt like it.
    """
    __slots__ = '_days','_hours','_minutes', '_seconds', 

    def __new__(cls, days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0):
        # Doing this efficiently and accurately in C is going to be difficult
        # and error-prone, due to ubiquitous overflow possibilities, and that
        # C double doesn't have enough bits of precision to represent
        # microseconds over 10K years faithfully.  The code here tries to make
        # explicit where go-fast assumptions can be relied on, in order to
        # guide the C implementation; it's way more convoluted than speed-
        # ignoring auto-overflow-to-long idiomatic Python could be.

        # XXX Check that all inputs are ints or floats.

        # Final values, all integer.
        # s and us fit in 32-bit signed ints; d isn't bounded.
        d = h = m = us = s = 0

        # Normalize everything to days, seconds, microseconds.
        days += weeks*7
        microseconds += milliseconds*1000

        # Get rid of all fractions, and normalize s and us.
        # Take a deep breath <wink>.
        if isinstance(days, float):
            dayfrac, days = _math.modf(days)
            dayhoursfrac, daysecondswhole = _math.modf(dayfrac * (24.))
            assert daysecondswhole == int(daysecondswhole)  # can't overflow
            h = int(daysecondswhole)
            assert days == int(days)
            d = int(days)
        else:
            dayhoursfrac = 0.0
            d = days
        assert isinstance(dayhoursfrac, float)
        assert abs(dayhoursfrac) <= 1.0
        assert isinstance(d, int)
        assert abs(s) <= 24 * 3600
        # days isn't referenced again before redefinition

        if isinstance(hours, float):
            hoursfrac, hours = _math.modf(hours)
            hoursminutefrac, hoursminutewhole = _math.modf(hoursfrac * (60.))
            assert seconds == int(seconds)
            hours = int(hours)
            m = int(hoursminutewhole)
            hoursfrac += dayhoursfrac
            assert abs(hoursfrac) <= 2.0
        else:
            hoursminutefrac = dayhoursfrac
        days, hours = divmod(hours, 24)
        d += days
        h += int(hours)


        if isinstance(minutes, float):
            minutesfrac, minutes = _math.modf(minutes)
            minutesecondsfrac, minutesecondswhole = _math.modf(minutesfrac * (60.))
            assert seconds == int(seconds)
            minutes = int(minutes)
            m = int(minutesecondswhole)
            minutesfrac += dayminutesfrac
            assert abs(minutesfrac) <= 2.0
        else:
            minutesecondsfrac = hoursminutefrac
        hours, minutes = divmod(minutes, 60)
        h += hours
        m += int(minutes)

        if isinstance(seconds, float):
            secondsfrac, seconds = _math.modf(seconds)
            assert seconds == int(seconds)
            seconds = int(seconds)
            secondsfrac += minutesecondsfrac
            assert abs(secondsfrac) <= 2.0
        else:
            secondsfrac = minutesecondsfrac
        assert isinstance(secondsfrac, float)
        assert abs(secondsfrac) <= 2.0

        assert isinstance(seconds, int)
        hours, seconds = divmod(seconds, 3600)
        h += hours
        s += int(seconds)    # can't overflow
        assert isinstance(s, int)
        assert abs(s) <= 2 * 24 * 3600

        usdouble = secondsfrac * 1e6
        assert abs(usdouble) < 2.1e6    # exact value not critical

        if isinstance(microseconds, float):
            microseconds = round(microseconds + usdouble)
            seconds, microseconds = divmod(microseconds, 1000000)
            hours, seconds = divmod(seconds, 3600)
            h += hours
            s += seconds
        else:
            microseconds = int(microseconds)
            seconds, microseconds = divmod(microseconds, 1000000)
            hours, seconds = divmod(seconds, 3600)
            h += hours
            s += seconds
            microseconds = round(microseconds + usdouble)
        assert isinstance(s, int)
        assert isinstance(microseconds, int)
        assert abs(s) <= 3 * 24 * 3600
        assert abs(microseconds) < 3.1e6

        seconds, _ = divmod(microseconds, 1000000)
        s += seconds
        minutes, s = divmod(seconds, 60)
        m += minutes
        hours, m = divmod(m, 3600)
        h += hours
        days, h = divmod(h, 24)
        d += days

        assert isinstance(d, int)
        assert isinstance(s, int) and 0 <= s < 24*3600
        assert isinstance(us, int) and 0 <= us < 1000000

        if abs(d) > 999999999:
            raise OverflowError("timedelta # of days is too large: %d" % d)

        self = super().__new__(cls)
        self._days = d
        self._minutes = m
        self._hours = h
        self._seconds = s
        return self

    def __repr__(self):
        args = []
        if self._days:
            args.append("days=%d" % self._days)
        if self._hours:
            args.append("hours=%d" % self._hours)
        if self._minutes:
            args.append("minutes=%d" % self._minutes)
        if self._seconds:
            args.append("seconds=%d" % self._seconds)
        if not args:
            args.append('0')
        return "%s.%s(%s)" % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              ', '.join(args))


    @property
    def hours(self):
        """hours"""
        return self._hours

    @property
    def minutes(self):
        """minutes"""
        return self._minutes

    def total_seconds(self):
        """Total seconds in the duration."""
        return ((self.days * 86400 + self.seconds + self.hours * 3600) * 10**6 +
                self.microseconds) / 10**6
        
# i = timedelta_custom(hours=2.5)
# print(isinstance(i, timedelta))
# print(i.__repr__())