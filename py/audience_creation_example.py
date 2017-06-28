'''
    Filename: audience_creation_example.py
    Author: Brett Coker
    Python Version: 3.6.1

    An example of how to use the Lotame API to create a basic audience,
    consisting of two behaviors ANDed together. This script assumes that the
    audience should be created on Enrich, with the APR disabled.
'''
import requests
import sys
from getpass import getpass

api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def main():
    username = input('Username: ')
    password = getpass()
    payload = {'username': username, 'password': password}

    # Exit if we cannot get the ticket-granting ticket (i.e. if the username
    # and/or password are incorrect)
    try:
        tgt = requests.post(auth_url, data=payload).headers['location']
    except KeyError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    client_id = input('Client ID: ')
    audience_name = input('New Audience Name: ')

    # Put the two behavior IDs in a list for future iteration
    behaviors_ids = []
    behaviors_ids.append(input('First Behavior ID: '))
    behaviors_ids.append(input('Second Behavior ID: '))

    behaviors = []
    first_behavior = True
    for behavior_id in behaviors_ids:
        # We can't give the first behavior a relationship, because there's
        # nothing behind it that it can relate to
        if first_behavior:
            relationship = None
            first_behavior = False
        # But we can define how the second behavior relates to the first. Note
        # that AND or OR *must* be in all caps, or you'll get a 500 error
        else:
            relationship = 'AND'

        # Puts the behavior IDs into a JSON skeleton, preparing them to be
        # passed into the audience JSON
        behavior = create_behavior_definition(tgt, behavior_id, relationship)
        behaviors.append(behavior)

    audience = {
        'clientId': client_id,
        'name': audience_name,
        'overlapOnly': True,  # True for Enrich, False for Extend
        'generate_apr': False,  # Be sure to set whether APR should be enabled
        'Client': {
            'id': client_id
        },
        'definition': {
            'component': behaviors
        }
    }

    # Use the above audience JSON to create the new audience
    endpoint = 'audiences'
    service_call = api_url + endpoint
    payload = {'service': service_call}
    service_ticket = requests.post(tgt, data=payload).text
    new_audience = requests.post(service_call + '?ticket=' + service_ticket, json=audience).json()

    # Print out the ID of the new audience
    new_audience_id = new_audience['id']
    print('New audience created with ID ' + new_audience_id)

    # Delete the ticket-granting ticket, now that we're done with it
    requests.delete(tgt)


def create_behavior_definition(tgt, behavior_id, relationship):
    """Creates behavior definition from ID and relationship."""
    definition = {
        'operator': relationship,
        'complexAudienceBehavior': {
            'behavior': {
                'id': behavior_id
            }
        }
    }
    return definition


if __name__ == '__main__':
    main()
