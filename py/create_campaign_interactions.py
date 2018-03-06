'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: create_campaign_interactions.py
    Author: Brett Coker
    Python Version: 3.6.4

    Creates interactions for campaigns.

    Takes a .csv as an argument, formatted as follows:
        - Header row (contents don't matter)
        - Campaign IDs in column A
        - Behavior IDs in column B
        - Interaction type IDs in column C
'''
import sys
import csv
from getpass import getpass
import better_lotameapi as lotame


def campaign_exists(campaign_id):
    status = lotame.get(f'campaigns/{campaign_id}').status_code
    return bool(status == 200)


def add_interaction(campaign_id, behavior_id, interaction_type_id):
    interaction = {
        'campaignId': campaign_id,
        'behaviorId': behavior_id,
        'interactionTypeId': interaction_type_id
    }

    response = lotame.post(f'campaigns/{campaign_id}/interactions', interaction)

    status = response.status_code
    return bool(status == 200)


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} interactions.csv')
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

        # Skip header row
        next(reader, None)

        for row in reader:
            campaign_id = row[0]
            behavior_id = row[1]
            interaction_type_id = row[2]

            if not campaign_exists(campaign_id):
                print(f'Error: Cannot find campaign {campaign_id}')
                continue

            created = add_interaction(campaign_id, behavior_id, interaction_type_id)

            if created:
                print(f'Added {behavior_id} to campaign {campaign_id}')
            else:
                print(f'Error: Could not add {behavior_id} to campaign {campaign_id}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
