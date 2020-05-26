'''
    Filename: get_audience_behaviors.py
    Author: Brett Coker
    Python Version: 3.6.2

    Given a user-inputted audience ID, prints out a list of behaviors used to
    create that audience.
'''
import better_lotameapi


def find_behaviors(definition, behaviors):
    """
    Adds all behavior IDs from an audience's component list into
    a list called behavior_list
    """
    for item in definition:
        if item['component']:
            find_behaviors(item['component'], behaviors)
        else:
            behavior_id = item['complexAudienceBehavior']['behavior']['id']
            behavior_name = item['complexAudienceBehavior']['behavior']['name']
            behaviors[behavior_id] = behavior_name


def main():
    lotame = better_lotameapi.Lotame()

    audience_id = input('Audience ID: ')

    # Get the audience info from the Lotame API
    response = lotame.get(f'audiences/{audience_id}')

    # Pull the resulting JSON from the Response object and get the desired
    # values from it
    audience_info = response.json()
    audience_name = audience_info['name']
    definition = audience_info['definition']['component']

    # If there are any nested groups of behaviors in the audience definition,
    # the best way to pull them out is with a recursive function, which is why
    # we define find_behaviors(definition, behaviors)
    behaviors = {}
    find_behaviors(definition, behaviors)

    print('Behaviors in ' + audience_name)
    for behavior_id in behaviors:
        print(behavior_id + '\t' + behaviors[behavior_id])


if __name__ == '__main__':
    main()
