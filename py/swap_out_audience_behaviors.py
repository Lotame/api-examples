'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: swap_out_audience_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.4

    Swaps out one audience behavior with another.

    You should understand that this is very likely to cause a
    fluctuation in uniques.

    Takes a .csv as an argument, with the following format:
        - Header row (names don't matter)
        - Audience IDs in column A
        - Old behavior IDs in column B
        - Net behavior IDs in column C
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
    response = lotame.put(f'audiences/{audience_id}', info)

    status = response.status_code
    if status != 204:
        return False

    return True


def is_valid_behavior_id(lotame, behavior_id):
    response = lotame.get(f'behaviors/{behavior_id}')

    status = response.status_code
    if status != 200:
        return False

    return True


def replace_behavior(component, old_behavior_id, new_behavior_id, complete=False):
    for item in component:
        if complete:
            return True
        if item['component']:
            complete = replace_behavior(item['component'], old_behavior_id, new_behavior_id, complete)
            if complete:
                return True
        else:
            current_behavior = item['complexAudienceBehavior']['behavior']['id']
            if current_behavior == old_behavior_id:
                item['complexAudienceBehavior']['behavior']['id'] = new_behavior_id
                del item['complexAudienceBehavior']['behavior']['name']
                return True

    return False


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audiences.csv')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        # Skip header row
        next(reader, None)

        for row in reader:
            skip_row = False

            audience_id = row[0]
            old_behavior_id = row[1]
            new_beahvior_id = row[2]

            audience_info = get_audience_info(lotame, audience_id)

            for behavior_id in [old_behavior_id, new_beahvior_id]:
                if not is_valid_behavior_id(lotame, behavior_id):
                    print(f'Error: {behavior_id} is not a valid behavior ID')
                    skip_row = True

            if skip_row:
                continue

            component = audience_info['definition']['component']
            success = replace_behavior(component, old_behavior_id, new_beahvior_id)

            if not success:
                print(f'Error: Couldn\'t find {old_behavior_id} in audience {audience_id}')
                continue

            audience_info['definition']['component'] = component

            if set_audience_info(lotame, audience_id, audience_info):
                print(f'Updated audience {audience_id} with behavior {new_beahvior_id}')
            else:
                print(f'Error: Couldn\'t update audience {audience_id} with {new_beahvior_id}')

    
if __name__ == '__main__':
    main()
