import unittest

from SwissKnife.calendar.WeekUtils import get_week_format_from_timestamp


class TestWeekUtils(unittest.TestCase):

    def test_get_52_week(self):
        timestamp_millis = 1514678400000  # 2017-12-31 (Sunday)
        result = get_week_format_from_timestamp(timestamp_millis)
        self.assertEqual(result, "2017W52")

    def test_get_first_week_with_a_previous_year_day(self):
        timestamp_millis = 1577709695547  # 2019-12-30 (Sunday)
        result = get_week_format_from_timestamp(timestamp_millis)
        self.assertEqual(result, "2020W01")

    def test_get_last_week_with_a_next_year_day(self):
        timestamp_millis = 1609459200000  # 2021-01-01 (Friday)
        result = get_week_format_from_timestamp(timestamp_millis)
        self.assertEqual(result, "2020W53")


if __name__ == '__main__':
    unittest.main()
