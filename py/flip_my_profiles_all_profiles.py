'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: flip_my_profiles_all_profiles.py
    Author: Brett Coker
    Python Version: 3.6.0

    Takes a .txt file of audience IDs as an audience (one per line).

    Changes all audiences to either My Profiles or All Profile, as chosen when
    running this script.
'''
import sys
import better_lotameapi


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    print('Change all audiences to...')
    print('1. My Profiles')
    print('2. All Profiles')
    audience_type = 0
    while audience_type not in [1, 2]:
        audience_type = int(input('Choose: '))

    filename = sys.argv[1]
    with open(filename) as file:
        for audience_id in file:
            audience_id = audience_id.strip()

            info = lotame.get(f'audiences/{audience_id}').json()

            # Set appropriate option, or skip to next audience if already set
            if audience_type == 1:
                if info['overlapOnly']:
                    print('Audience {audience_id} already correct.')
                    continue
                info['overlapOnly'] = True  # My Profiles
            else:
                if not info['overlapOnly']:
                    print('Audience {audience_id} already correct.')
                    continue
                info['overlapOnly'] = False  # All Profiles

            status = lotame.put(f'audiences/{audience_id}', info).status_code
            print(f'Audience {audience_id} | HTTP {status}')

    
if __name__ == '__main__':
    main()
