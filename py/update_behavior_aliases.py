'''
    Filename: update_behavior_aliases.py
    Author: Brett Coker
    Python Version: 3.6.2

    Adds or replaces behavior aliases. Takes an xls/xlsx as an argument.

    The spreadsheet should be formatted as follows:
        - Header row required
        - First column is behavior IDs
        - Second column is aliases.

    Dependent on openpyxl, available through pip.
'''
import sys
from getpass import getpass
import requests
import openpyxl

api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def get_behavior_alias_info(tgt, behavior_id):
    """Gets a behavior's JSON file of aliases."""
    endpoint = f'{api_url}behaviors/{behavior_id}/aliases'
    payload = {'service': endpoint}
    service_ticket = requests.post(tgt, data=payload).text
    full_endpoint = f'{endpoint}?ticket={service_ticket}'
    response = requests.get(full_endpoint)

    # Return None if the behavior ID could not be found
    status = response.status_code
    if status != 200:
        return None

    return response.json()


def update_behavior_alias(tgt, behavior_id, new_alias, replace):
    """Updates a behavior's alias, either through replacing or appending."""
    alias_info = get_behavior_alias_info(tgt, behavior_id)

    # Return False if unable to grab existing alias info
    if not alias_info:
        return False

    # Replace any aliases by inserting the new one as a list
    if replace:
        alias_info['alias'] = [new_alias]
    # Append the new alias to the existing list
    else:
        alias_info['alias'].append(new_alias)

    endpoint = f'{api_url}behaviors/{behavior_id}/aliases'
    payload = {'service': endpoint}
    service_ticket = requests.post(tgt, data=payload).text
    full_endpoint = f'{endpoint}?ticket={service_ticket}'
    response = requests.put(full_endpoint, json=alias_info)

    # Return False if adding the alias failed
    status = response.status_code
    if status != 204:
        return False

    return True

def main():
    """Reads from an Excel spreadsheet and replaces/appends aliases."""
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} aliases.csv')
        sys.exit()

    username = input('Username: ')
    password = getpass()
    payload = {'username': username, 'password': password}

    # Exit if we cannot get the ticket-granting ticket (i.e. if the username
    # and/or password are incorrect)
    try:
        tgt = requests.post(auth_url, data=payload).headers['location']
    except KeyError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    print('Select option:')
    print('1. Replace aliases')
    print('2. Append aliases')
    option = 0
    # Loop until a valid choice is given by the user
    while option not in ['1', '2']:
        option = input('Option: ')

    replace = bool(option == 1)

    # Prepare to read from the Excel spreadsheet
    filename = sys.argv[1]
    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    # Go through the Excel spreadsheet, skipping the first row (header)
    for row in range(2, sheet.max_row + 1):
        behavior_id = str(sheet[f'A{row}'].value)
        new_alias = str(sheet[f'B{row}'].value)

        updated = update_behavior_alias(tgt, behavior_id, new_alias, replace)

        if updated:
            print(f'Updated alias for behavior {behavior_id}')
        else:
            print(f'Error updating alias for behavior {behavior_id}')

    requests.delete(tgt)


if __name__ == '__main__':
    main()
