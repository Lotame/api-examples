'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: ignore_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.2

    Ignores a list of behaviors. Takes a .txt file of behavior IDs as an
    argument.
'''
import sys
import better_lotameapi


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behavior_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as behavior_file:
        behavior_ids = [behavior_id.strip() for behavior_id in behavior_file]

    info = {
        'behaviors': {
            'behavior': []
        }
    }

    for behavior_id in behavior_ids:
        behavior = {'id': behavior_id}
        info['behaviors']['behavior'].append(behavior)

    status = lotame.put('behaviors/ignored', info).status_code
    if status == 204:
        print('Successfully ignored behaviors.')
    else:
        print('Error: Could not ignore behaviors.')

    
if __name__ == '__main__':
    main()
