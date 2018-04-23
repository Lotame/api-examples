'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: flip_enrich_extend.py
    Author: Brett Coker
    Python Version: 3.6.0

    Takes a .txt file of audience IDs as an audience (one per line).

    Changes all audiences to either enrich or extend, as chosen when running
    this script.
'''
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Username and/or password invalid.')
        sys.exit()

    print('Change all audiences to...')
    print('1. Enrich')
    print('2. Extend')
    audience_type = 0
    while audience_type not in [1, 2]:
        audience_type = int(input('Choose: '))

    filename = sys.argv[1]
    with open(filename) as file:
        for audience_id in file:
            audience_id = audience_id.strip()

            info = lotame.get('audiences/{audience_id}').json()

            # Set appropriate option, or skip to next audience if already set
            if audience_type == 1:
                if info['overlapOnly']:
                    print('Audience {audience_id} already correct.')
                    continue
                info['overlapOnly'] = True  # Enrich
            else:
                if not info['overlapOnly']:
                    print('Audience {audience_id} already correct.')
                    continue
                info['overlapOnly'] = False  # Extend

            status = lotame.put('audiences/{audience_id}', info).status_code
            print('Audience {audience_id} | HTTP {status}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
