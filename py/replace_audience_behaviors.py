'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: replace_audience_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.4

    Given a .csv of audience and behavior IDs, replaces all behaviors in the
    given audience with the behaviors provided in the spreadsheet. They will be
    either AND or OR'd together.

    It's usually better to just create new audiences, but if an in-place
    replacement is desired, it can be done with this script.

    CSV file formatting:
        - Header row (values don't matter)
        - Audience IDs in first column
        - Behavior IDs in every column after the first, one per column
'''
import sys
import csv
import better_lotameapi


def choice(prompt, valid_options):
    answer = ''
    while answer not in valid_options:
        answer = input(prompt)

    return answer


def get_audience_info(lotame, audience_id):
    """Grabs audience info from the API."""
    response = lotame.get(f'audiences/{audience_id}')

    status = response.status_code
    if status != 200:
        return None

    return response.json()


def put_audience_info(lotame, audience_id, audience_info):
    """Updates an audience."""
    status = lotame.put(f'audiences/{audience_id}', audience_info).status_code

    if status != 204:
        return False

    return True


def create_behavior_definition(behavior_id, relationship):
    """Creates behavior definition from ID and relationship."""
    definition = {
        'operator': relationship,
        'complexAudienceBehavior': {
            'behavior': {
                'id': behavior_id,
            }
        }
    }
    return definition


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audiences.xlsx')
        return

    lotame = better_lotameapi.Lotame()

    print('Relationship?')
    print('1. AND')
    print('2. OR')
    relationship = choice('Choose: ', ['1', '2'])

    if relationship == '1':
        relationship = 'AND'
    else:
        relationship = 'OR'

    filename = sys.argv[1]
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        # Skip header row
        next(reader, None)

        for row in reader:
            audience_id = row.pop(0)

            audience_info = get_audience_info(lotame, audience_id)
            if not audience_info:
                print(f'Error: Could not find audience {audience_id}')
                continue

            behaviors = []
            for behavior_id in row:
                if behavior_id == '':
                    break
                if not behaviors:
                    behavior = create_behavior_definition(behavior_id, None)
                else:
                    behavior = create_behavior_definition(behavior_id, relationship)
                behaviors.append(behavior)

            audience_info['definition']['component'] = behaviors
            if put_audience_info(lotame, audience_id, audience_info):
                print(f'Updated audience {audience_id}')
            else:
                print(f'Error: Could not update audience {audience_id}')

    
if __name__ == '__main__':
    main()
