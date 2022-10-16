import unittest
from unittest import mock
from show_timezones import TimeZoneProcess
from collections import namedtuple


class TestTimeZoneProcess(unittest.TestCase):

    def setUp(self):
        self.test_json_data = [{
            "value": "UTC-11",
            "abbr": "U",
            "offset": -11,
            "isdst": False,
            "text": "(UTC-11:00) Coordinated Universal Time-11",
            "utc": [
              "Etc/GMT+11",
              "Pacific/Midway",
              "Pacific/Niue",
              "Pacific/Pago_Pago"
            ]
          },
          {
            "value": "Hawaiian Standard Time",
            "abbr": "HST",
            "offset": -10,
            "isdst": False,
            "text": "(UTC-10:00) Hawaii",
            "utc": [
              "Etc/GMT+10",
              "Pacific/Honolulu",
              "Pacific/Johnston",
              "Pacific/Rarotonga",
              "Pacific/Tahiti"
            ]
          },
          {
            "value": "Alaskan Standard Time",
            "abbr": "AKDT",
            "offset": 10,
            "isdst": False,
            "text": "(UTC-09:00) Alaska",
            "utc": [
              "America/Anchorage",
              "America/Juneau",
              "America/Nome",
              "America/Sitka",
              "America/Yakutat"
            ]
          },
        ]
        self.tz_obj = TimeZoneProcess()

    def tearDown(self):
        pass

    def mocked_http_response(self):
        Response = namedtuple('Response', ['json', 'status_code', 'text'])
        resp = Response(lambda: {"value": "any_random_value"}, "200", "any_random_data")
        return resp, []

    def test_filter_and_display_timezones_default_run_positive(self):
        ret_data = self.tz_obj.filter_and_display_timezones(self.test_json_data)
        self.assertEqual(len(self.test_json_data), len(ret_data), "The returned data is not correct.")

    def test_filter_and_display_timezones_empty_data(self):
        ret_data = self.tz_obj.filter_and_display_timezones([])
        self.assertEqual(0, len(ret_data), "Returned data should have been empty")

    def test_setting_value_of_match_param(self):
        """
        Test to filter timezones by setting `match` parameter.
        """
        self.tz_obj.match = "Alaska"
        ret_data = self.tz_obj.filter_and_display_timezones(self.test_json_data)
        self.assertEqual(len(ret_data), 1, msg="There should have been exactly 1 record (Alaskan region)")

    def test_setting_value_of_offset_param(self):
        """
        Test to filter timezones by setting `offset` parameter.
        """
        self.tz_obj.offset = 10
        ret_data = self.tz_obj.filter_and_display_timezones(self.test_json_data)
        self.assertEqual(len(ret_data), 2, msg="There should have been exactly 2 records(for +10 and -10 offset)")

    def test_setting_value_of_offset_and_match_params_both(self):
        """
        Test to filter timezones by setting `offset` and `match` parameters.
        """
        self.tz_obj.offset = 10
        self.tz_obj.match = "Hawaiian"
        ret_data = self.tz_obj.filter_and_display_timezones(self.test_json_data)
        self.assertEqual(len(ret_data), 2, msg="There should have been exactly 2 records")

    def test_setting_value_of_offset_and_match_params_both_but_none_matches(self):
        """
        Test to filter timezones by setting `offset` and `match` parameters. Should return Zero records.
        """
        self.tz_obj.offset = 50
        self.tz_obj.match = "HawaiianHawaaiin"
        ret_data = self.tz_obj.filter_and_display_timezones(self.test_json_data)
        self.assertEqual(len(ret_data), 0, msg="There should have been exactly 0 records")

    @mock.patch('show_timezones.HttpRequests.get', side_effect=mocked_http_response)
    def test_http_get(self, mock_get):
        resp = self.tz_obj.get_json_data()
        print(resp)
        self.assertEqual(1, len(resp), msg="Length of the response data should have been 1.")


