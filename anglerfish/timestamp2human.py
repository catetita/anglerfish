#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Calculate time, with precision from seconds to days.

ISO-8601 standard:Its permitted to omit 'T' character by mutual agreement."""


import time

from collections import deque, namedtuple
from datetime import datetime
from types import MappingProxyType

try:
    from ujson import dumps
except ImportError:
    from json import dumps


def timestamp2human(timestamp_on_seconds: int, iso_sep: str=" ") -> namedtuple:
    """Calculate date & time, with precision from seconds to millenniums."""
    # Calculate all time units from timestamp_on_seconds positive integer.
    minutes, seconds = divmod(int(abs(timestamp_on_seconds)), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)
    years, months = divmod(months, 12)
    decades, years = divmod(years, 10)
    centuries, decades = divmod(decades, 10)
    millenniums, centuries = divmod(centuries, 10)

    # Build a namedtuple with all named time units and all its integer values.
    time_units = namedtuple(
        "AllHumanFriendlyFrequentTimeUnits",
        ("seconds minutes hours days weeks months "
         "years decades centuries millenniums")
    )(
        seconds, minutes, hours, days, weeks, months,
        years, decades, centuries, millenniums
    )

    # Build a human friendly time string with frequent time units.
    time_parts, human_time_auto = deque(), None  # []
    if millenniums:
        this_time = f"{millenniums} Millennium{'s' if millenniums > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time
        time_parts.append(this_time)
    if centuries:
        this_time_unit = f"{centuries} Centur{'ies' if centuries > 1 else 'y'}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if decades:
        this_time_unit = f"{decades} Decade{'s' if decades > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if years:
        this_time_unit = f"{years} Year{'s' if years > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if months:
        this_time_unit = f"{months} Month{'s' if months > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if weeks:
        this_time_unit = f"{weeks} Week{'s' if weeks > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if days:
        this_time_unit = f"{days} Day{'s' if days > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if hours:
        this_time_unit = f"{hours} Hour{'s' if hours > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if minutes:
        this_time_unit = f"{minutes} minute{'s' if minutes > 1 else ''}"
        if not human_time_auto:
            human_time_auto = this_time_unit
        time_parts.append(this_time_unit)
    if not human_time_auto:
        human_time_auto = f"{seconds} Second{'s' if seconds > 1 else ''}"
    time_parts.append(f"{seconds} Second{'s' if seconds > 1 else ''}")

    # Get a Human string ISO-8601 representation of datetime.datetime with UTC.
    iso_datetime = datetime.fromtimestamp(timestamp_on_seconds).replace(
        microsecond=0).astimezone().isoformat(iso_sep)

    time_dict = {
        "seconds": seconds, "minutes": minutes, "hours": hours, "days": days,
        "weeks": weeks, "months": months, "years": years, "decades": decades,
        "centuries": centuries, "millenniums": millenniums,
    }

    return namedtuple(
        "HumanTimes",
        "human units auto iso dict json inmmutable ")(
        " ".join(time_parts), time_units, human_time_auto, iso_datetime,
        time_dict, dumps(time_dict), MappingProxyType(time_dict))


def timedelta2human(time_delta) -> namedtuple:  # Just a shortcut :)
    """Convert a timedelta object to human string representation."""
    return timestamp2human(time_delta.total_seconds())


def datetime2human(date_time) -> namedtuple:  # Just a shortcut :)
    """Convert a datetime object to human string representation."""
    return timestamp2human(time.mktime(date_time.timetuple()))


def now2human(utc=False) -> namedtuple:  # Just a shortcut :)
    """Now expressed as human friendly time units string, optional UTC."""
    date_time = datetime.utcnow() if utc else datetime.now()
    return timestamp2human(time.mktime(date_time.timetuple()))
