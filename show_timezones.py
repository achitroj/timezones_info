# usage: show_timezones.py [-h] [--match MATCH] [--offset OFFSET], or, run 'python show_timezones.py -h' for help.

import argparse
import copy
import logging
import re
from datetime import datetime, timedelta
from datetime import timezone as dt_timezone

import requests
from pytz import timezone
from requests.adapters import HTTPAdapter

# setting logging type as DEBUG, can be changed to INFO, WARNING, as required.
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)


class TimeZoneProcess:

    TZ_URL = "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
    CURRENT_TD_MESSAGE = "Current datetime: {}"

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
        self.parser.add_argument("--offset", type=float,
                                 help='If specified, this script will only display time zones matching'
                                      'this offset. Works in OR condition with --match param.')
        args = self.parser.parse_args()
        self.match = args.match
        self.offset = args.offset
        logging.debug("Params passed to the script are: match={} and offset={}".format(self.match, self.offset))
        return args

    def get_json_data(self, url=None):
        """
        Method to retrieve json data from timezone url
        :return: list containing info about timezones
        """
        _url = url if url else self.TZ_URL
        http_obj = HttpRequests()
        response, err = http_obj.get(_url)
        if err:
            raise Exception(err)
        timezone_data = response.json()
        return timezone_data

    def filter_and_display_timezones(self, tz_data):
        """
        Method to filter and display timezones
        :param tz_data: timezone data(list of dicts)
        """
        final_list = list()
        if not tz_data:
            return final_list

        match_filtered_regions = list()
        offset_filtered_regions = list()

        to_match = self.match if self.match else ''
        _offset = float(self.offset) if self.offset else self.offset

        for region in tz_data:
            if re.search(to_match, region['value'], flags=re.IGNORECASE):
                match_filtered_regions.append(region)

            if self.offset:
                if not to_match:
                    match_filtered_regions.clear()

                if not region['isdst']:  # if daylight saving is False, then we will compare with offset field
                    if abs(_offset) == abs(region['offset']):
                        offset_filtered_regions.append(region)

                if region['isdst']:  # if daylight saving is True, we will compare with UTC
                    try:
                        _utc = [float(x) for x in re.findall(r'\d+', region['text'])][0]
                    except IndexError:  # that means, there is no int value in region['text'] and hence UTC is Zero
                        _utc = 0
                    if abs(_offset) == abs(_utc):
                        offset_filtered_regions.append(region)

        final_list = copy.deepcopy(match_filtered_regions)
        [final_list.append(x) for x in offset_filtered_regions if x not in final_list]
        logging.debug("filtered list is {}".format(final_list))

        for region in final_list:
            print(''.join(['\nTimezone is: ', region['value'], '(', region['abbr'], ')', ': ', region['text']]))
            try:
                zone = region['utc'][0]
                tz = timezone(zone)
                dt = datetime.now(tz)
            except IndexError:  # in case the 'utc' field is empty, like in case of Mid-Atlantic Standard Time
                logging.debug("No region found for {0}, so extracting UTC field from 'text' field...".
                              format(region['value']))
                utc_val = float('.'.join(re.findall(r'\d+', region['text'])))
                if "-" in region['text']:
                    dt = datetime.now(dt_timezone.utc) - timedelta(hours=utc_val)
                else:
                    dt = datetime.now(dt_timezone.utc) + timedelta(hours=utc_val)

            print(self.CURRENT_TD_MESSAGE.format(dt.strftime('%d-%b-%Y, %H:%M:%S %p')), "\n")

        print("Total {0} records found".format(len(final_list)))
        return final_list


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
