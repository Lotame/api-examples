'''
    Filename: get_behavior_names.py
    Author: Brett Coker
    Python Version: 3.6.2

    Takes a .txt file containing behavior IDs (one per line) as an argument.

    Goes through a list of behavior IDs and outputs the name of each behavior.
'''
import sys
import better_lotameapi


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behavior_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

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
    
if __name__ == '__main__':
    main()
