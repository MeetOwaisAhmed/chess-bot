from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import dateparser
import re


def get_clock_emoji(time: datetime) -> str:
    clock_emoji = "🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦"
    """Generates embed with current time UTC"""
    return clock_emoji[
        round(2 * (time.hour % 12 + time.minute / 60)) % len(clock_emoji)
    ]


def __fix_tz(text: str) -> str:
    """Overrides certain timezones with more relevant ones"""
    replacements = {
        "BST": "+0100",  # British Summer Time
        "IST": "+0530",  # Indian Standard Time
    }
    for timezone, offset in replacements.items():
        text = re.sub(fr"\b{timezone}\b", offset, text, flags=re.IGNORECASE)
    return text


def parse_date(
    date_str: Optional[str] = None,
    from_tz: Optional[str] = None,
    to_tz: Optional[str] = None,
    future: Optional[bool] = None,
    base: datetime = datetime.now(),
) -> Optional[datetime]:
    """Returns datetime object for given date string
    Arguments:
    :param date_str: :class:`Optional[str]` date string to parse
    :param from_tz: :class:`Optional[str]` string representing the timezone to interpret the date as (eg. "Asia/Jerusalem")
    :param to_tz: :class:`Optional[str]` string representing the timezone to return the date in (eg. "Asia/Jerusalem")
    :param future: :class:`Optional[bool]` set to true to prefer dates from the future when parsing
    :param base: :class:`datetime` datetime representing where dates should be parsed relative to
    """
    if date_str is None:
        return None
    # set dateparser settings
    settings: Dict[str, Any] = {
        "RELATIVE_BASE": base.replace(tzinfo=None),
        **({"TIMEZONE": __fix_tz(from_tz)} if from_tz else {}),
        **({"TO_TIMEZONE": __fix_tz(to_tz)} if to_tz else {}),
        **({"PREFER_DATES_FROM": "future"} if future else {}),
    }
    # parse the date with dateparser
    date = dateparser.parse(__fix_tz(date_str), settings=settings)
    # return the datetime object
    return date


def format_date(
    date: datetime, base: datetime = datetime.now(), all_day: bool = False
) -> str:
    """Convert dates to a specified format
    Arguments:
    :param date: :class:`datetime` The date to format
    :param base: :class:`datetime` When the date or time matches the info from base, it will be skipped.
        This helps avoid repeated info when formatting time ranges.
    :param all_day: :class:`bool` If set to true, the time of the day will not be included
    """
    # %a = Weekday (eg. "Mon"), %d = Day (eg. "01"), %b = Month (eg. "Sep")
    date_format = "%a %d %b"
    # include the year if the date is in a different year
    if date.year != base.year:
        # %Y = Year (eg. "2021")
        date_format += " %Y"
    # include the time if it is not an all day event and not the same as the base
    if not all_day and date != base:
        # %H = Hours (24-hour clock), %M = Minutes
        date_format += " %H:%M"
    # format the date and remove leading zeros and trailing spaces
    return date.strftime(date_format).replace(" 0", " ", 1).strip()
