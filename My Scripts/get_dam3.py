import sys
sys.path.append('../')

import os
import json
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'behavecon.settings')
django.setup()
from group.models import Session, Player


# enter session name below
session_name = 'priming9301'

# get all players that are part of the session
players = Player.objects.filter(session=session_name)
# get the group numbers
groups = list(set([player.group for player in players]))

count_dict = dict.fromkeys(groups, 0)
for player in players:
    # for each player 
    # increment the group value in count_dict by 1 if that player chose "Dam 3"
    group = player.group
    answers = json.loads(player.answers)
    # do a key check in case
    if "damChoiceGroup" in answers.keys():
        if answers["damChoiceGroup"] == "Dam 3":
            count_dict[group] += 1
    else:
        print "Warning: damChoiceGroup missing"
        
# get the number of groups that have 2 or more votes for "Dam 3"
total_gte_2 = sum([1 for value in count_dict.itervalues() if value >= 2])

print "Results: ", str(total_gte_2)