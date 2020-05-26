'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: enable_apr.py
    Author: Brett Coker
    Python Version: 3.6.0

    Takes a txt file that is a list of audience IDs (one per line) and enables
    APR for those audiences.
'''
import sys
import better_lotameapi


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as file:
        for audience_id in file:
            audience_id = audience_id.strip()

            info = lotame.get(f'audiences/{audience_id}').json()
            if info['generate_apr']:
                print(f'APR already active for audience {audience_id}')
            else:
                info['generate_apr'] = True
                response = lotame.put(f'audiences/{audience_id}', info)
                status = response.status_code
                print(f'Audience {audience_id} | HTTP {status}')

    
if __name__ == '__main__':
    main()
