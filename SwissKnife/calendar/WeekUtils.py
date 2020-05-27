from datetime import datetime


def get_week_format_from_timestamp(timestamp_millis: int) -> str:
    """Get week format from timestamp in milliseconds. The week number
    returned will follow ISO-8601 standard

    :param timestamp_millis: Timestamp in milliseconds.
    :type timestamp_millis: int
    :return: Return in week format {year}W{week}. Note that the week will be pad to two digits, e.g: 2020W01
    :rtype: str
    """

    date_object = datetime.utcfromtimestamp(int(timestamp_millis) / 1000)
    calendar = date_object.isocalendar()
    year = calendar[0]
    target_week = calendar[1]

    return "{}W{:0>2}".format(year, target_week)