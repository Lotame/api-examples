'''
    Filename: flip_enrich_extend.py
    Author: Brett Coker
    Python Version: 3.6.2

    Takes a .txt file of audience IDs as an audience (one per line).

    Changes all audiences to either enrich or extend, as chosen when running
    this script.
'''
import sys
from getpass import getpass
import requests

api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def get_audience_info(tgt, audience_id):
    """Given the ticket-granting ticket and an audience ID, returns the JSON
    of the corresponding audience.
    """
    endpoint = f'{api_url}audiences/{audience_id}'
    payload = {'service': endpoint}
    service_ticket = requests.post(tgt, data=payload).text
    full_endpoint = f'{endpoint}?ticket={service_ticket}'
    response = requests.get(full_endpoint)

    # Return None if a bad response is received
    status = response.status_code
    if status != 200:
        return None

    # Otherwise, return the audience's JSON file
    return response.json()


def update_audience(tgt, audience_id, info):
    """Given the ticket-granting ticket, an audience ID, and an audience JSON,
    performs a PUT request to update the given audience. Returns True if the
    update was successful, or False if it was not.
    """
    endpoint = f'{api_url}audiences/{audience_id}'
    payload = {'service': endpoint}
    service_ticket = requests.post(tgt, data=payload).text
    full_endpoint = f'{endpoint}?ticket={service_ticket}'
    response = requests.put(full_endpoint, json=info)

    # Return False if a bad response is received
    status = response.status_code
    if status != 204:
        return False

    return True


def main():
    """Given a .txt file of audience IDs, changes each of the audiences to
    either Enrich or Extend.
    """
    if len(sys.argv) == 1:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        sys.exit()

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

    print('Change all audiences to...')
    print('1. Enrich')
    print('2. Extend')
    choice = ''
    # Loop until a valid choice is given by the user
    while choice not in ['1', '2']:
        choice = input('Choose: ')

    # Pull all of the audience IDs out of the .txt file
    filename = sys.argv[1]
    with open(filename) as infile:
        audience_ids = [audience_id.strip() for audience_id in infile]

    for audience_id in audience_ids:
        info = get_audience_info(tgt, audience_id)

        # Skip to the next audience if this one could not be found
        if not info:
            print(f'Error retrieving audience {audience_id}')
            continue

        # Set appropriate option, or skip to next audience if already set
        # Set audience to Enrich
        if choice == '1':
            if info['overlapOnly']:
                print(f'Audience {audience_id} already on Enrich.')
                continue
            info['overlapOnly'] = True  # Enrich
        # Set audience to Extend
        else:
            if not info['overlapOnly']:
                print(f'Audience {audience_id} already on Extend.')
                continue
            info['overlapOnly'] = False  # Extend

        # Attempt to update the audience and print whether it was successful
        audience_updated = update_audience(tgt, audience_id, info)
        if audience_updated:
            print(f'Updated audience {audience_id}')
        else:
            print(f'Error updating audience {audience_id}')

    # Delete the ticket-granting ticket, now that we're done with it
    requests.delete(tgt)


if __name__ == '__main__':
    main()
