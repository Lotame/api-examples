"""
Python Lotame API wrapper.
==========================
Filename: lotame.py
Author: Paulo Kuong
Email: pkuong80@gmail.com
Python Version: 3.6.1

Please refer to https://api.lotame.com/docs/#/ to get all Endpoints.
Please refer to README (https://github.com/paulokuong/lotame) for examples.
"""
from lotame.lotame import Lotame


if __name__ == '__main__':
    l = Lotame(username='xxxx', password='yyyy')

    # Search audiences
    audiences = l.get('audiences/search',
                      searchTerm='Age - ').json()['Audience']

    # Get behavior 3333
    behavior = l.get('behaviors/{}'.format(3333)).json()

    # Create audience segment with 3 behaviors.
    audience_definition = l.get_create_audience_json(
        'Lotame api test 5',
        2215, [[6322283, 6322292], [6322283, 6322292]],
        'Testing out Lotame API 5')
    post_response_json = l.post('audiences', audience_definition).json()
    print(post_response_json)

    # Create audience segment with 3 behaviors for (My Profile)
    audience_definition = l.get_create_audience_json(
        'Lotame api test 5',
        2215, [[6322283, 6322292, 1111760, 6322303],
               [6322283, 6322292, 1111760, 6322303]],
        'Testing out Lotame API 5', overlap=True)

    # Create audience segment with 3 behaviors for (All Profile)
    audience_definition = l.get_create_audience_json(
        'Lotame api test 5',
        2215, [[6322283, 6322292, 1111760, 6322303],
               [6322283, 6322292, 1111760, 6322303]],
        'Testing out Lotame API 5', overlap=False)

    # Getting Reach Estimate (Note that description param is removed
    # since it is not valid param)
    audience_definition = l.get_create_audience_json(
        'Lotame api test 8',
        2215, [[6322283, 6322292, 1111760, 6322303],
               [6322283, 6322292, 1111760, 6322303]])
    reach_estimates = l.post(
        'audiences/reachEstimates', audience_definition).json()
    reach_estimates_res = l.get(
        'audiences/reachEstimates/{}'.format(reach_estimates.get('id')))
    print(reach_estimates_res.json())

    # Getting behaviors under hierarchy tree at depth 2 child nodes.
    [{'name': j['name'], 'behavior_id':j['behaviorId']}
     for j in l.get('hierarchies/525000', depth=2).json().get(
     'nodes')[1].get('childNodes')]
