'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: add_recency.txt
    Author: Brett Coker
    Python Version: 3.6.1

    Takes a .txt file of audience IDs (one per line) as an argument.

    Adds (or changes) a recency value to each behavior in the given
    audience's definitions.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def add_recency(component, recency):
    """Recursively adds recency values to all behaviors."""
    for item in component:
        if item['component']:
            add_recency(item['component'], recency)
        else:
            item['complexAudienceBehavior']['recency'] = recency


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    recency = input('Recency (in days): ')
    recency = str(int(recency) * 24 * 60)  # Convert secs to days

    filename = sys.argv[1]
    with open(filename) as audience_ids:
        for audience_id in audience_ids:
            audience_id = audience_id.strip()

            info = lotame.get(f'audiences/{audience_id}').json()
            component = info['definition']['component']
            add_recency(component, recency)
            info['definition']['component'] = component
            response = lotame.put(f'audiences/{audience_id}', info)
            status = response.status_code

            print(f'Audience {audience_id} | HTTP {status}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
