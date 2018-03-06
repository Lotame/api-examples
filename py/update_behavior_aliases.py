'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: update_behavior_aliases.py
    Author: Brett Coker
    Python Version: 3.6.3
    Updated: 12/19/17

    Adds new aliases to behaviors. Takes an xlsx as an argument.

    The spreadsheet should be formatted as follows:
        - Header row required
        - First column is behavior IDs
        - Second column is aliases.
'''
import sys
from getpass import getpass
import openpyxl
import better_lotameapi as lotame


def main():
    if len(sys.argv) == 1:
        print(f'Usage: python {sys.argv[0]} aliases.xlsx')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username or password.')
        sys.exit()

    option = 0
    while option not in ['1', '2']:
        print('Select option:')
        print('1. Replace variants')
        print('2. Append variants')
        option = input('Option: ')

    filename = sys.argv[1]
    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    for row in range(2, sheet.max_row + 1):
        behavior_id = str(sheet[f'A{row}'].value)
        new_alias = str(sheet[f'B{row}'].value)

        endpoint = f'behaviors/{behavior_id}/aliases'
        info = lotame.get(endpoint).json()

        if option == '1':  # Replace
            info['alias'] = [new_alias]
        else:  # Append
            info['alias'].append(new_alias)

        status = lotame.put(endpoint, info).status_code

        print(f'Behavior {behavior_id} | HTTP {status}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
