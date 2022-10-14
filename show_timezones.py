# TODO: Add unit tests
# TODO: Remove print statements

# usage: show_timezones.py [-h] [--match MATCH] [--offset OFFSET], or, run python show_timezones.py -h for help.

import argparse
import logging
import re
from datetime import datetime

import requests
from pytz import timezone
from requests.adapters import HTTPAdapter


# setting logging type as DEBUG, can be changed to INFO, WARNING, if required.
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class TimeZoneProcess:

    TZ_URL = "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
    CURRENT_TD_MESSAGE = "Current time and date for this zone is: {}"

    def __init__(self):
        self.parser = argparse.ArgumentParser("show_timezones.py")
        self.offset = None
        self.match = None
        self._set_script_parameters()

    def _set_script_parameters(self):
        self.parser.add_argument("--match",
                                 help='If specified, this script will display information only about time zones whose '
                                 'values match the string supplied to this argument.'
                                 ' Works in OR condition with --offset param.')
        self.parser.add_argument("--offset", type=int,
                                 help='If specified, this script will only display time zones matching'
                                      'this offset. Works in OR condition with --match param.')
        args = self.parser.parse_args()
        self.match = args.match
        self.offset = args.offset
        logging.debug("Params passed to the script are: match={} and offset={}".format(self.match, self.offset))

    def get_json_data(self):
        """
        Method to retrieve json data from timezone url
        :return: list containing info about timezones
        """
        http_obj = HttpRequests()
        response, err = http_obj.get(self.TZ_URL)
        if err:
            raise Exception(err)
        timezone_data = response.json()
        return timezone_data

    def filter_and_display_timezones(self, tz_data):
        """
        Method to filter and display timezones
        :param tz_data: timezone data(list)
        """

        match_filtered_regions = list()
        offset_filtered_regions = list()

        for region in tz_data:
            to_match = self.match if self.match else ''
            if re.search(to_match, region['value'], flags=re.IGNORECASE):
                match_filtered_regions.append(region)

            if self.offset:
                try:
                    _offset = int(self.offset)
                except ValueError:
                    raise Exception("Invalid value found for 'offset' param: '{}'".format(self.offset))
                if abs(_offset) == abs(region['offset']):
                    offset_filtered_regions.append(region)

        print("filtered_regions is: ", match_filtered_regions)
        print("filtered_regions len: ", len(match_filtered_regions))
        filtered_list = match_filtered_regions + offset_filtered_regions
        print("\noffset_filtered_regions is: ", offset_filtered_regions)
        print("offset_filtered_regions is: ", len(offset_filtered_regions))
        for region in filtered_list:
            print(''.join(['Region is: ', region['value'], '(', region['abbr'], ')', ': ', region['text']]))
            zone = region['utc'][0]
            tz = timezone(zone)
            dt = datetime.now(tz)
            print(self.CURRENT_TD_MESSAGE.format(dt.strftime('%d-%b-%Y, %H:%M:%S %p')), "\n")

        return filtered_list  # just in case required for any further processing, or validating via unit-test cases.


class HttpRequests:

    @staticmethod
    def get(url, headers=None):
        session = requests.Session()
        session.mount(url, HTTPAdapter(max_retries=4))
        logging.debug("Connecting to URL: {}".format(url))
        resp = session.get(url, headers=headers)
        logging.debug("Response code: {}".format(resp.status_code))
        err = None
        if resp.status_code != 200:
            err = 'Unable to get data from the url: {}, status code: {}'.format(url, resp.status_code)
            return [], err
        return resp, err

    # def post()...

    # def patch()...


if __name__ == "__main__":
    obj_tz = TimeZoneProcess()
    tz_data = obj_tz.get_json_data()
    obj_tz.filter_and_display_timezones(tz_data)
