'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: uncategorize_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.2

    Uncategorizes a list of behaviors, given an xls such that:
    - Column A contains node IDs
    - Column B contains behavior IDs
'''
import sys
import getpass
import openpyxl
import better_lotameapi as lotame


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behaviors.xlsx')
        sys.exit()

    username = input('Username: ')
    password = getpass.getpass()

    try:
        lotame.authenticate(username, password)
    except lotame.AuthenticationError:
        print('Error: Invalid username or password.')
        sys.exit()

    # Prep to open given Excel file
    filename = sys.argv[1]
    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    for row in range(2, sheet.max_row + 1):
        # Get node and behavior for the row
        node_id = str(sheet[f'A{row}'].value)
        behavior_id = str(sheet[f'B{row}'].value)

        endpoint = 'hierarchies/nodes/' + \
            node_id + '/categorizedBehaviors?behavior_id=' + \
            behavior_id + '&unscoped=false&include_global=false'

        status = lotame.delete(endpoint).status_code

        if status == 204:
            print(f'Decategorized behavior {behavior_id} from {node_id}')
        else:
            print(f'Error decategorizing behavior {behavior_id} from {node_id}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
