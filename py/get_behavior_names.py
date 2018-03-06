'''
    Filename: get_behavior_names.py
    Author: Brett Coker
    Python Version: 3.6.2

    Takes a .txt file containing behavior IDs (one per line) as an argument.

    Goes through a list of behavior IDs and outputs the name of each behavior.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    # Exit if there's no argument passed in
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behavior_ids.txt')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    # Authenticate with the Lotame API
    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    # Open the user-provided list of behavior IDs and go through each line
    filename = sys.argv[1]
    with open(filename) as behavior_ids:
        for behavior_id in behavior_ids:
            # Get rid of the newline character at the end of each line, since
            # this will confuse the API
            behavior_id = behavior_id.strip()

            # Get the behavior info from the Lotame API
            response = lotame.get(f'behaviors/{behavior_id}')

            # Pull the resulting JSON from the Response object and get the
            # value from the 'name' key
            behavior_info = response.json()
            behavior_name = behavior_info['name']

            print(behavior_id + '\t' + behavior_name)

    # Delete the ticket-granting ticket, now that the script is done with it
    lotame.cleanup()


if __name__ == '__main__':
    main()
