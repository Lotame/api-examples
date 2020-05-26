'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: get_child_nodes.py
    Author: Brett Coker
    Python Version: 3.6.1

    Given a hierarchy ID, returns the IDs of all children, grandchildren, etc.
'''
import better_lotameapi


def main():
    lotame = better_lotameapi.Lotame()

    hierarchy_id = input('Hierarchy ID: ')
    endpoint = f'hierarchies/{hierarchy_id}/nodes?depth=2'
    response = lotame.get(endpoint)

    if response.status_code != 200:
        print('Error: Could not find hierarchy.')
        lotame.cleanup()
        return

    nodes = response.json()['nodes']
    node_ids = []
    ''' Get the ID of the top nodes and then check for children.'''
    for node in nodes:
        node_ids.append(node['id'])
        get_child_nodes(node, node_ids)

    for node_id in node_ids:
        print(node_id)

    
def get_child_nodes(node, node_ids):
    """Recursively checks all child nodes for more children."""
    if node['childNodes']:
        for child in node['childNodes']:
            node_ids.append(child['id'])
            get_child_nodes(child, node_ids)


if __name__ == '__main__':
    main()
