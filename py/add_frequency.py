'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: add_frequency.txt
    Author: Brett Coker
    Python Version: 3.6.1

    Takes a .txt file of audience IDs (one per line) as an argument.

    Adds (or changes) a frequency value to each behavior in the given
    audience's definitions.
'''
import sys
import better_lotameapi


def add_frequency(component, frequency):
    """Recursively adds frequency values to all behaviors."""
    for item in component:
        if item['component']:
            add_frequency(item['component'], frequency)
        else:
            item['complexAudienceBehavior']['frequency'] = frequency


def get_audience(lotame, audience_id):
    response = lotame.get(f'audiences/{audience_id}')
    return response.json()


def update_audience(lotame, audience_id, audience):
    response = lotame.put(f'audiences/{audience_id}', audience)
    return response.status_code == 204


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    frequency = input('Frequency: ')

    filename = sys.argv[1]
    with open(filename) as audience_ids:
        for audience_id in audience_ids:
            audience_id = audience_id.strip()

            audience = get_audience(lotame, audience_id)
            component = audience['definition']['component']
            add_frequency(component, frequency)
            audience['definition']['component'] = component
            
            if update_audience(lotame, audience_id, audience):
                print(f'Updated audience {audience_id}')
            else:
                print(f'Error: Unable to update audience {audience_id}')

    
if __name__ == '__main__':
    main()
