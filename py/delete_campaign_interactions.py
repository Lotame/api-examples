'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: delete_campaign_interactions.py
    Author: Brett Coker
    Python Version: 3.6.4

    Deletes given interactions from a given campaign.

    Takes a .csv as an argument, formatted as follows:
        - Header row (values don't matter)
        - Campaign ID in column A
        - Interaction ID in column B
'''
import sys
from getpass import getpass
import csv
import better_lotameapi as lotame


def delete_interaction(campaign_id, interaction_id):
    endpoint = f'campaigns/{campaign_id}/interactions/{interaction_id}' \
               '?deep_clean=true'

    status = lotame.delete(endpoint).status_code

    if status == 204:
        return True

    return False


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} campaigns.csv')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password')
        sys.exit()

    filename = sys.argv[1]
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        #Skip header
        next(reader, None)

        for row in reader:
            campaign_id = row[0]
            interaction_id = row[1]

            if delete_interaction(campaign_id, interaction_id):
                message = f'Deleted interaction {interaction_id} from ' \
                          f'campaign {campaign_id}'
            else:
                message = f'Could not delete interaction {interaction_id} ' \
                          f'from campaign {campaign_id}'
            print(message)

    lotame.cleanup()


if __name__ == '__main__':
    main()
