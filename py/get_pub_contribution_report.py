'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: get_pub_contribution_report.py
    Author: Brett Coker
    Python Version: 3.6.1

    Outputs a publisher contribution report CSV for a given audience ID.
'''
import csv
import sys
from getpass import getpass
import better_lotameapi as lotame


def main():
    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username and/or password.')

    audience_id = input('Audience ID: ')

    response = lotame.get(f'reports/audiences/{audience_id}/publisher')
    status = response.status_code

    if status != 200:
        print('Error retrieving contribution report.')
        sys.exit()

    report = response.json()

    columns = report['reportColumns']
    with open('pub_contribution_report.csv', 'w', newline='') as csvfile:
        report_writer = csv.writer(csvfile, delimiter=',')
        report_writer.writerow(columns)

        for publisher in report['stats']:
            publisher_stats = []
            for column in columns:
                publisher_stats.append(publisher[column])
            report_writer.writerow(publisher_stats)


if __name__ == '__main__':
    main()
