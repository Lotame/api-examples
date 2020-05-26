'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: get_monthly_behavior_uniques.py
    Author: Brett Coker
    Python Version: 3.6.4

    Takes a .txt file of behavior IDs as an argument.

    For the given list of behaviors, pulls uniques from the user-provided
    month. Those are then written to a .csv file.
'''
import sys
import csv
import better_lotameapi


def get_choice(prompt, options=None):
    choice = input(prompt)

    if options:
        while choice not in options:
            choice = input(prompt).lower()

    return choice


def get_behavior_client_id(lotame, behavior_id):
    response = lotame.get(f'behaviors/{behavior_id}')

    status = response.status_code
    if status != 200:
        return None

    return response.json()['clientId']


def get_monthly_uniques(lotame, behavior_id, network, date):
    client_id = get_behavior_client_id(lotame, behavior_id)

    if not client_id:
        return None

    network = bool(network == 'y')

    endpoint = f'statistics/behaviors/{behavior_id}/aggregated' \
               f'?client_as_group={network}&ref_date={date}' \
               f'&stat_interval=FULL_MONTH&client_id={client_id}' \
                '&universe_id=1'
    response = lotame.get(endpoint)

    status = response.status_code
    if status != 200:
        return None

    return response.json()['uniques']


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} behavior_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as behavior_file:
        behavior_ids = [behavior_id.strip() for behavior_id in behavior_file]

    valid_months = [str(month) for month in range(1, 13)]
    prompt = 'Enter a month (numeric): '
    month = get_choice(prompt, valid_months)
    if len(month) == 1:
        month = f'0{month}'

    year = get_choice('Enter a year: ')
    date = f'{year}{month}01'

    prompt = 'Are these network clients? (y/n) '
    network = get_choice(prompt, ['y', 'n'])

    behavior_stats = []
    print('Grabbing stats...')
    for behavior_id in behavior_ids:
        uniques = get_monthly_uniques(lotame, behavior_id, network, date)

        if not uniques:
            print(f'Error: Couldn\'t get uniques for {behavior_id}')
            continue

        behavior_stat = {
            'behavior_id': behavior_id,
            'uniques': uniques
        }

        behavior_stats.append(behavior_stat)

        if not behavior_stats:
            print('Couldn\'t get any stats')
            return

    filename = f'monthly_stats_{date}.csv'
    with open(filename, 'w') as statfile:
        writer = csv.writer(statfile, delimiter='\t')
        writer.writerow(['Behavior ID', 'Monthly Uniques'])

        for behavior_stat in behavior_stats:
            behavior_id = behavior_stat['behavior_id']
            uniques = behavior_stat['uniques']

            writer.writerow([behavior_id, uniques])

    print(f'Stats written to {filename}')


if __name__ == '__main__':
    main()
