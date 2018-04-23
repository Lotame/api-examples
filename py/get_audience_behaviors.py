'''
    Filename: get_audience_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.2

    Given a user-inputted audience ID, prints out a list of behaviors used to
    create that audience.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    username = input('Username: ')
    password = getpass()

    # Authenticate with the Lotame API
    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    audience_id = input('Audience ID: ')

    # Get the audience info from the Lotame API
    response = lotame.get(f'audiences/{audience_id}')

    # Pull the resulting JSON from the Response object and get the desired
    # values from it
    audience_info = response.json()
    audience_name = audience_info['name']
    definition = audience_info['definition']['component']

    # Delete the ticket-granting ticket, now that the script is done with it
    lotame.cleanup()

    # If there are any nested groups of behaviors in the audience definition,
    # the best way to pull them out is with a recursive function, which is why
    # we define find_behaviors(definition, behaviors)
    behaviors = {}
    find_behaviors(definition, behaviors)

    print('Behaviors in ' + audience_name)
    for behavior_id in behaviors:
        print(behavior_id + '\t' + behaviors[behavior_id])


def find_behaviors(definition, behaviors):
    """
    Adds all behavior IDs from an audience's component list into
    a list called behavior_list
    """
    for item in definition:
        if item['component']:
            find_behaviors(item['component'], behaviors)
        else:
            behavior_id = item['complexAudienceBehavior']['behavior']['id']
            behavior_name = item['complexAudienceBehavior']['behavior']['name']
            behaviors[behavior_id] = behavior_name


if __name__ == '__main__':
    main()
