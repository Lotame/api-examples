'''
    Filename: audience_creation_example.py
    Author: Brett Coker
    Python Version: 3.6.2

    An example of how to use the Lotame API to create a basic audience,
    consisting of two behaviors ANDed together. This script assumes that the
    audience should be created on Enrich, with the APR disabled.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    username = input('Username: ')
    password = getpass()

    # Exit if we cannot get the ticket-granting ticket (i.e. if the username
    # and/or password are incorrect)
    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    client_id = input('Client ID: ')
    audience_name = input('New Audience Name: ')

    # Put the two behavior IDs in a list for future iteration
    behavior_ids = []
    behavior_ids.append(input('First Behavior ID: '))
    behavior_ids.append(input('Second Behavior ID: '))

    behaviors = []
    first_behavior = True
    for behavior_id in behavior_ids:
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
        behavior = create_behavior_definition(behavior_id, relationship)
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
    new_audience = lotame.post('audiences', audience).json()

    # Print out the ID of the new audience
    new_audience_id = new_audience['id']
    print('New audience created with ID ' + new_audience_id)

    # Delete the ticket-granting ticket, now that we're done with it
    lotame.cleanup()


def create_behavior_definition(behavior_id, relationship):
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
