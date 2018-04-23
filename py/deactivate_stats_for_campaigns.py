'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: deactivate_stats_for_campaigns.py
    Author: Brett Coker
    Python Version: 3.6.2

    Sets the activateStats key for each given campaign to False.

    Takes a .txt file of campaign IDs as an argument.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} campaign_ids.txt')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    filename = sys.argv[1]
    with open(filename) as campaign_file:
        campaign_ids = [campaign_id.strip() for campaign_id in campaign_file]

    for campaign_id in campaign_ids:
        response = lotame.get(f'campaigns/{campaign_id}')

        status = response.status_code
        if status != 200:
            print(f'Could not retrieve campaign {campaign_id}')
            continue

        campaign_info = response.json()
        campaign_info['activateStats'] = False

        response = lotame.put(f'campaigns/{campaign_id}', campaign_info)

        status = response.status_code
        if status == 200:
            print(f'Deactivated stats for campaign {campaign_id}')
        else:
            print(f'Could not deactivate stats for campaign {campaign_id}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
