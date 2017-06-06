'''
    Filename: get_audience_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.1

    Given a user-inputted audience ID, prints out a list of behaviors used to
    create that audience.
'''
import requests
import sys
from getpass import getpass

# Two URLs that must be defined for working with the Lotame API
api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def main():
    username = input('Username: ')
    password = getpass()
    payload = {'username': username, 'password': password}

    # Get the ticket-granting ticket from the Lotame API. If we get a KeyError,
    # we know that the credentials are invalid, so we handle this by exiting
    try:
        tgt = requests.post(auth_url, data=payload).headers['location']
    except KeyError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    audience_id = input('Audience ID: ')

    endpoint = 'audiences/' + audience_id
    service_call = api_url + endpoint
    payload = {'service': service_call}

    # This call gets the service ticket from the API. This ticket is
    # only valid for ten seconds, will only work once, and will only
    # work for the endpoint provided in the payload (service_call)
    service_ticket = requests.post(tgt, data=payload).text
    # Perform the request that we want and get the Response object
    response = requests.get(service_call + '?ticket=' + service_ticket)

    # Pull the resulting JSON from the Response object and get the desired
    # values from it
    audience_info = response.json()
    audience_name = audience_info['name']
    definition = audience_info['definition']['component']

    # Delete the ticket-granting ticket, now that the script is done with it
    requests.delete(tgt)

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
