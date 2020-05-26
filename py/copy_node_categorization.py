'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: copy_node_categorization.txt
    Author: Brett Coker
    Python Version: 3.6.2

    Copies behavior categorizations from one node to another.

    Takes an .xlsx file as an argument. It should include a header row and two
    columns:
        - Column A: Original node IDs
        - Column B: Node IDs to copy to
'''
import sys
import openpyxl
import better_lotameapi


def get_categorized(lotame, node_id, client_id):
    endpoint = f'hierarchies/nodes/{node_id}/categorizedBehaviors' \
               f'?client_id={client_id}'
    response = lotame.get(endpoint)

    status = response.status_code
    if status != 200:
        return None

    return response.json()


def categorize(lotame, node_id, info):
    endpoint = f'hierarchies/nodes/{node_id}/categorizedBehaviors'
    response = lotame.put(endpoint, info)

    status = response.status_code
    if status != 204:
        return False

    return True


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} nodes.xlsx')
        return

    lotame = better_lotameapi.Lotame()

    client_id = input('Hierarchy owner ID: ')

    filename = sys.argv[1]
    workbook = openpyxl.load_workbook(filename)
    sheet_names = workbook.get_sheet_names()
    sheet = workbook.get_sheet_by_name(sheet_names[0])

    for row in range(2, sheet.max_row + 1):
        original_id = str(sheet[f'A{row}'].value)
        duplicate_id = str(sheet[f'B{row}'].value)

        categorized = get_categorized(lotame, original_id, client_id)
        if not categorized['behavior']:
            print(f'Nothing to categorize from {original_id} to {duplicate_id}')
            continue

        del categorized['totalRows']

        for behavior in categorized['behavior']:
            del behavior['created']
            del behavior['modified']
            del behavior['categories']

        success = categorize(lotame, duplicate_id, categorized)
        if success:
            print(f'Copied from {original_id} to {duplicate_id}')
        else:
            print(f'Error copying from {original_id} to {duplicate_id}')

    
if __name__ == '__main__':
    main()
