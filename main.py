#!/usr/bin/env python3
import datetime
import time

from twilio.rest import Client

import creds
import number_list

debug = True

if not debug:
    client = Client(creds.creds['account_sid'], creds.creds['auth_token'])


# This is the actual call method used.
def make_call(n, client, t_number, s_number, url):
    client.calls.create(
        to=s_number,
        from_=t_number,
        url=url,
        record=True
    )

    print(
        f"Call: {n} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Placed a call using twilio's {t_number}"
        f" to scammer number {s_number} with {url}")


def test_call(n, t_number, s_number, url):
    print(
        f"Call: {n} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Placed a call using twilio's {t_number}"
        f" to scammer number {s_number} with {url}")


# This is the method which loops through your active Twilio phone numbers and makes calls as often as set in seconds,
# and loops as many times specified.

def flood_scammer(loops, seconds, url):
    print(f'The following number(s):')
    for i in number_list.scammer_phone_number:
        print(f'{i},')
    print(f'Will be called by the following number(s):')
    for x in number_list.twilio_active_phone_numbers:
        print(f'{x},')
    print('\n')
    n = 1
    # You can change 'range(x)' number to loop as many times as you want.
    for i in range(loops):
        for tnumber in number_list.twilio_active_phone_numbers:
            for snumber in number_list.scammer_phone_number:
                if debug:
                    test_call(n, tnumber, snumber, url)
                    n += 1
                else:
                    make_call(n, client, tnumber, snumber, url)
                    n += 1
                time.sleep(seconds)  # Change how long to wait to call again in seconds


if __name__ == '__main__':
    flood_scammer(loops=1,  # loops * total Twilio nums * Scammer nums
                  seconds=0.5,  # Time before next call.
                  # A url with a valid xml playback message
                  # EX: https://www.twilio.com/console/runtime/twiml-bins
                  url="http://example.twilio.com/voice.xml")
