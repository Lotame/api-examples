'''
    Filename: get_behavior_names.py
    Author: Brett Coker
    Python Version: 3.6.1

    Takes a .txt file containing behavior IDs (one per line) as an argument.

    Goes through a list of behavior IDs and outputs the name of each behavior.
'''
import requests
import sys
from getpass import getpass

# Two URLs that must be defined for working with the Lotame API
api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def main():
    # Exit if there's no argument passed in
    if len(sys.argv) != 2:
        print('Usage: python ' + sys.argv[0] + ' behavior_ids.txt')
        sys.exit()

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

    # Open the user-provided list of behavior IDs and go through each line
    filename = sys.argv[1]
    with open(filename) as behavior_ids:
        for behavior_id in behavior_ids:
            # Get rid of the newline character at the end of each line, since
            # this will confuse the API
            behavior_id = behavior_id.strip()

            endpoint = 'behaviors/' + behavior_id
            service_call = api_url + endpoint
            payload = {'service': service_call}

            # This call gets the service ticket from the API. This ticket is
            # only valid for ten seconds, will only work once, and will only
            # work for the endpoint provided in the payload (service_call)
            service_ticket = requests.post(tgt, data=payload).text
            # Perform the request that we want and get the Response object
            response = requests.get(service_call + '?ticket=' + service_ticket)

            # Pull the resulting JSON from the Response object and get the
            # value from the 'name' key
            behavior_info = response.json()
            behavior_name = behavior_info['name']

            print(behavior_id + '\t' + behavior_name)

    # Delete the ticket-granting ticket, now that the script is done with it
    requests.delete(tgt)


if __name__ == '__main__':
    main()
