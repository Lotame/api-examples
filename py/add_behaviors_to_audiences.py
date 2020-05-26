'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: add_behaviors_to_audiences.py
    Author: Brett Coker
    Python Version: 3.6.4

    Adds behaviors to a given list of audiences (one behavior per audience).

    Takes a .csv as an argument:
        - Header row required (contents don't matter)
        - Column A should be audience IDs
        - Column B should be behavior IDs

    Behaviors will be either ANDed or ORed, as chosen by the user when running
    the script. They will be appended to the end of the definition, which
    means they will be in their own group (i.e. not nested).
'''
import sys
import csv
import better_lotameapi


def get_audience_info(lotame, audience_id):
    response = lotame.get(f'audiences/{audience_id}')

    status = response.status_code
    if status != 200:
        return None

    return response.json()


def set_audience_info(lotame, audience_id, info):
    status = lotame.put(f'audiences/{audience_id}', info).status_code
    return bool(status == 204)


def is_valid_behavior(lotame, behavior_id):
    status = lotame.get(f'behaviors/{behavior_id}').status_code
    return bool(status == 200)


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audiences.csv')
        return

    lotame = better_lotameapi.Lotame()

    print('Append options:')
    print('1. AND')
    print('2. OR')
    choice = ''
    while choice not in ['1', '2']:
        choice = input('Choice: ')

    if choice == '1':
        operator = 'AND'
    else:
        operator = 'OR'

    filename = sys.argv[1]
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        # Skip header row
        next(reader)

        for row in reader:
            audience_id = row[0]
            behavior_id = row[1]

            audience_info = get_audience_info(lotame, audience_id)
            if not audience_info:
                print(f'Error: Audience {audience_id} not found')
                continue

            if not is_valid_behavior(lotame, behavior_id):
                print(f'Error: Behavior {behavior_id} not found')
                continue

            behavior = {
                'operator': operator,
                'complexAudienceBehavior': {
                    'behavior': {
                        'id': behavior_id
                    }
                }
            }

            audience_info['definition']['component'].append(behavior)
            if set_audience_info(lotame, audience_id, audience_info):
                print(f'Updated audience {audience_id}')
            else:
                print(f'Error: Could not update audience {audience_id}')

    
if __name__ == '__main__':
    main()
