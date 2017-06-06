'''
    Filename: uncategorized_behavior_report.py
    Author: Brett Coker
    Python Version: 3.6.1

    Generates an uncategorized beahvior report and saves it as a CSV file
    named uncategorized_behaviors.csv. The file is saved to the directory
    where this script is run from.
'''
import requests
import sys
import csv
from getpass import getpass

# Two URLs that must be defined for working with the Lotame API
api_url = 'https://api.lotame.com/2/'
auth_url = 'https://crowdcontrol.lotame.com/auth/v1/tickets'


def main():
    username = input('Username: ')
    password = getpass()
    payload = {'username': username, 'password': password}

    # Get the ticket-granting ticket from the Lotame API. If we get a KeyError,
    # we know that the credentials are invalid, so we handle this by exiting
    try:
        tgt = requests.post(auth_url, data=payload).headers['location']
    except KeyError:
        print('Error: Invalid username and/or password.')
        sys.exit()

    # Get the client ID to create the report for
    client_id = input('Client ID: ')

    # This call will grab the first 5000 results from the report. If there are
    # greater than 5000 behaviors, consider either increasing the page_count
    # or creating a loop that utilizes the page_num paramenter of the API call
    endpoint = 'reports/behaviors/uncategorized?client_id=' + \
        client_id + '&page_count=5000'
    service_call = api_url + endpoint
    payload = {'service': service_call}

    # This call gets the service ticket from the API. This ticket is
    # only valid for ten seconds, will only work once, and will only
    # work for the endpoint provided in the payload (service_call)
    service_ticket = requests.post(tgt, data=payload).text
    # Perform the request that we want and get the Response object
    response = requests.get(service_call + '&ticket=' + service_ticket)

    # Delete the ticket-granting ticket, now that the script is done with it
    requests.delete(tgt)

    # We need to pull the list called 'stats' out of the Response's JSON file.
    # The rest of the data from the JSON file can be ignored for the purpose of
    # this script
    report = response.json()
    stats = report['stats']

    with open('uncategorized_behaviors.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Behavior Name', 'Behavior ID', 'Uniques'])
        for behavior in stats:
            behavior_name = behavior['behaviorName']
            behavior_id = behavior['behaviorId']
            uniques = behavior['uniques']

            writer.writerow([behavior_id, behavior_name, uniques])


if __name__ == '__main__':
    main()
