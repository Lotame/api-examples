'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.
    
    Filename: categorize_behaviors.py
    Author: Brett Coker
    Python Version: 3.8.1

    Categorizes behaviors into given nodes.

    Takes a .csv as an argument:
        - Column A: Node IDs
        - Column B: Behavior IDs
'''
import sys
import csv
import better_lotameapi


def categorize_behavior(lotame, node_id, behavior_id):
    endpoint = f'hierarchies/nodes/{node_id}/categorizedBehaviors'

    options = {
        'behavior': [
            {'id': behavior_id}
        ]
    }

    response = lotame.put(endpoint, options)
    return response.status_code == 204


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behaviors.csv')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            node_id = row[0]
            behavior_id = row[1]

            if categorize_behavior(lotame, node_id, behavior_id):
                print(f'Categorized {behavior_id} into {node_id}')
            else:
                print(f'Error: Could not categorize {behavior_id} into {node_id}')


if __name__ == '__main__':
    main()
