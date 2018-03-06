'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: get_apr_genders.py
    Author: Brett Coker
    Python Version: 3.6.3

    For a given .txt file of audience IDs, exports a .csv with the male and
    female percentages from each audience's APR.
'''
import sys
import csv
from getpass import getpass
from datetime import datetime
import better_lotameapi as lotame


def get_apr_gender_percents(audience_id):
    response = lotame.get(f'reports/audiences/{audience_id}/profile/type/6')

    status = response.status_code
    if status != 200:
        return None

    apr_info = response.json()

    gender_percents = {}
    gender_percents['audience_name'] = apr_info['audienceName']
    for affinity in apr_info['audienceAffinities']:
        gender = affinity['behaviorName']
        percent = str(round(float(affinity['compositional30']), 2))

        gender_percents[gender] = percent

    return gender_percents


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} audience_ids.txt')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    filename = sys.argv[1]
    with open(filename) as audience_file:
        audience_ids = [audience_id.strip() for audience_id in audience_file]

    today = datetime.today().strftime('%Y%m%d')
    outfile_name = f'audience_apr_genders_{today}.csv'

    with open(outfile_name, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(['Audience ID', 'Audience Name', 'Male', 'Female'])

        for audience_id in audience_ids:
            gender_percents = get_apr_gender_percents(audience_id)

            if not gender_percents:
                print(f'Error: Could not get APR for audience {audience_id}')
                continue

            audience_name = gender_percents['audience_name']
            male_percent = gender_percents['Male'] + '%'
            female_percent = gender_percents['Female'] + '%'

            row = [audience_id, audience_name, male_percent, female_percent]
            writer.writerow(row)

    print(f'Results exported to {outfile_name}')
    lotame.cleanup()


if __name__ == '__main__':
    main()
