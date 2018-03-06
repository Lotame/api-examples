'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: create_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.4

    Opens an xlsx and creates behaviors based off of the information in it.
    The spreadsheet should be formatted as follows:
        - Must have a header row
        - Column A is the behavior name
        - Column B is the behavior description
        - Column C is the client ID
        - Column D is the behavior type ID
    Run this with the .xlsx file as an argument.
'''
import sys
from getpass import getpass
import openpyxl
import better_lotameapi as lotame


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behaviors.xlsx')
        sys.exit()

    username = input('Username: ')
    password = getpass()

    lotame.authenticate(username, password)

    filename = sys.argv[1]
    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    for row in range(2, sheet.max_row + 1):
        name = str(sheet[f'A{row}'].value)
        description = str(sheet[f'B{row}'].value)
        client_id = str(sheet[f'C{row}'].value)
        type_id = str(sheet[f'D{row}'].value)

        options = {
            'name': name,
            'description': description,
            'clientId': client_id,
            'behaviorTypeId': type_id
        }

        response = lotame.post('behaviors?use_aliases=true', options)
        print(f'{name} | {response.status_code}')

    lotame.cleanup()


if __name__ == '__main__':
    main()
