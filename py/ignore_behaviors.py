'''
    Filename: ignore_behaviors.py
    Author: Elbert Fliek
    Python Version: 2.7.12

    Takes a .txt file containing behavior IDs (one per line) as an argument.
    Ignores those behaviors
'''
import argparse
import lotame_utils
import requests
from ConfigParser import SafeConfigParser


# Set up our Parser and get the values
parser = SafeConfigParser()
parser.read('config.cfg')
username = parser.get('api_examples', 'username')
password = parser.get('api_examples', 'password')
base_api_url = parser.get('api_examples', 'api_url')

argparser = argparse.ArgumentParser(description='Ignore a list of behaviors.')
argparser.add_argument(
    'idsfile',
    help='the name of the file containing a list of behaviors to ignore')
args = argparser.parse_args()


def putRequest(grandingTicket, service, body):
    service_call = base_api_url + 'behaviors/ignored'
    payload = {'service': service_call}
    service_ticket = requests.post(grandingTicket, data=payload).text
    headers = {'Accept': 'application/json'}
    return requests.put(
        ('%s?ticket=%s') % (service_call, service_ticket),
        json=body,
        headers=headers)


def main():
    grandingTicket = lotame_utils.getTicketGrandingTicket(username, password)

    ignore = []
    with open(args.idsfile) as behavior_ids:
        for behavior_id in behavior_ids:
            ignore.append({'id': behavior_id})

    body = {'behaviors': {
        'behavior': ignore,
        'totalRows': len(ignore)
    }}

    resp = putRequest(grandingTicket, 'behaviors/ignored', body)

    print 'Ignore behaviors response status code: %s' % resp.status_code

    # Once we are done with the Ticket Granting Ticket we should clean it up'
    resp = requests.delete(grandingTicket)
    print 'Remove Granding Ticket response status code: %s' % resp.status_code


if __name__ == '__main__':
    main()
