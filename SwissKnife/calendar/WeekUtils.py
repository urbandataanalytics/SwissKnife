from datetime import datetime


def get_week_format_from_timestamp(timestamp_millis: int) -> str:
    """Get week format from timestamp in milliseconds.

    :param timestamp_millis: Timestamp en milliseconds.
    :type timestamp_millis: int
    :return: Return in week format {year}W{week}.
    :rtype: str
    """

    # This algorithm avoids results like 2019W01 for a 2019-12-31 date
    # and 2021W53 for a 2021-01-01 date

    date_object = datetime.utcfromtimestamp(int(timestamp_millis) / 1000)
    calendar = date_object.isocalendar()
    year = calendar[0]
    target_week = calendar[1]

    return "{}W{:0>2}".format(year, target_week)