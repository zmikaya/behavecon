from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint
from group.models import Session, Player
from djangoChat.models import Message
from django.db import IntegrityError
import json
import ast
import os
import django
import datetime
from dateutil import parser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'behavecon.settings')
django.setup()

# Create your views here.
from django.http import HttpResponse

@ensure_csrf_cookie
def index(request):
    return render(request, 'group/index.html')

@ensure_csrf_cookie
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print 'here'
                login(request, user)
                return HttpResponseRedirect('/profile/')
        else:
            failure = {'reason': "Invalid login attempt."}
            return render(request, "group/controls/login.html", failure)

    return render(request, 'group/controls/login.html')

@login_required
def profile(request):
    live_sessions = Session.objects.filter(live=1)
    live_session_list = []
    for session in live_sessions:
        live_session_list.append([session.name, session.date, getSessionType(session.stype), session.players])
    dead_sessions = Session.objects.filter(live=0)
    dead_session_list = []
    for session in dead_sessions:
        dead_session_list.append([session.name, session.date, getSessionType(session.stype), session.players])
    context_dict = {"live_sessions": live_session_list, "dead_sessions": dead_session_list}
    return render(request, 'group/controls/profile.html', context_dict)

@login_required
def create_session(request):
    if request.method == "POST":
        from time import strftime
        date = strftime("%b-%d-%Y")
        sessionName = request.POST['sessionName']
        sessionPlayers = int(request.POST['players'])
        sessionType = int(request.POST['sessionType'])
        groups = json.dumps({"0": 0})
        # add session to database
        try:
            s = Session(name=sessionName, players=sessionPlayers, date=date, stype=sessionType, live=1, groups=groups)
            s.save()
            sessionType = getSessionType(sessionType)
            from time import strftime
            now = strftime("%b-%d-%Y")
            td = [sessionName, now, sessionType, sessionPlayers]
            context_dict = {'td': td}
            return render(request, 'group/controls/ajax/new_session.html', context_dict)
        except IntegrityError:
            print 'error'
    return

# @login_required
# def get_data(request, session):
#     import csv
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(session)
#     writer = csv.writer(response)
#     players = Player.objects.filter(session=session)
#     keys = ''
#     page_time_keys = ''
#     for player in players:
#         if not keys:
#             keys = sorted(json.loads(player.answers).keys())
#         if keys and len(sorted(json.loads(player.answers).keys())) > keys:
#             keys = sorted(json.loads(player.answers).keys())
#         # add header data for time
#         if not page_time_keys:
#             visited_pages = sorted(json.loads(player.time).keys())[:-1]
#             visited_pages = sorted([int(element) for element in visited_pages])
#             page_time_keys = range(3, int(visited_pages[-1])+1)
#         if page_time_keys:
#             visited_pages = sorted(json.loads(player.time).keys())[:-1]
#             visited_pages = sorted([int(element) for element in visited_pages])
#             if visited_pages[-1] > page_time_keys[-1]:
#                 page_time_keys = range(3, int(visited_pages[-1])+1)
#     header = ["username", "session", "type", "group", "info_set"]
#     key_ans_length = dict((el,0) for el in keys)
#     for key in keys:
#         print key
#         for i in range(len(json.loads(players[0].answers)[key])): # fix single player dependency
#             key_ans_length[key] += 1
#             header.append(key + '-' + str(i+1))
#     header += page_time_keys
#     print page_time_keys
#     data = []
#     data.insert(0, header)
#     for player in players: # fix single player dependency
#         username = player.username
#         stype = Session.objects.filter(name=session)[0].stype
#         group = player.group
#         info_set = player.info_set
#         row = [username, session, stype, group, info_set]
#         for key in keys:
#             try:
#                 row += json.loads(player.answers)[key]
#             except KeyError:
#                 # find out how many cells to fill
#                 count = key_ans_length[key]
#                 row += ['No Response']*count
#         for page in page_time_keys:
#             visited_pages = json.loads(player.time)
#             try:
#                 # row += visited_pages[str(page)]
#                 row.append(visited_pages[str(page)])
#             except KeyError:
#                 row.append('No Data')
#         data.append(row)
#     for row in data:
#         writer.writerow(row)
    # return response
    
@login_required
def get_data(request, session):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(session)
    writer = csv.writer(response)
    players = Player.objects.filter(session=session)
    stype = Session.objects.filter(name=session)[0].stype
    # load the header file
    with open('header.csv', 'rb') as f:
        reader = csv.reader(f)
        header = list(reader)
    # remove empty strings where necessary
    data = []
    
    for i in range(len(header)):
        header[i] = filter(None, header[i])
    if int(stype) == 0:
        key_ans_length = {'dam1_group': 6, 'dam2_group': 6, 'dam3_group': 6, 'damChoiceGroup': 1, 'damChoice': 5}
        keys = key_ans_length.keys()
        page_time_keys = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        data.insert(0, header[0])
    else:
        key_ans_length = {'damChoiceGroup': 5, 'damChoice': 5}
        keys = key_ans_length.keys()
        page_time_keys = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        data.insert(0, header[1])
    for player in players:
        username = player.username
        stype = Session.objects.filter(name=session)[0].stype
        group = player.group
        info_set = player.info_set
        row = [username, session, stype, group, info_set]
        for key in keys:
            try:
                value = json.loads(player.answers)[key]
                if type(value) == unicode:
                    print value
                    row += [value]
                else:
                    row += json.loads(player.answers)[key]
            except KeyError:
                # find out how many cells to fill
                count = key_ans_length[key]
                row += ['No Response']*count
        for page in page_time_keys:
            visited_pages = json.loads(player.time)
            try:
                # row += visited_pages[str(page)]
                row.append(visited_pages[str(page)])
            except KeyError:
                row.append('No Data')
        data.append(row)
    for row in data:
        writer.writerow(row)
    return response

@login_required
def get_chat_data(request, session):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.txt"'.format(session)
    writer = csv.writer(response)
    players = Player.objects.filter(session=session)
    chat_rooms = set([player.chat_room for player in players])
    writer.writerow(["<Session>: " + session])
    for chat_room in chat_rooms:
        writer.writerow(["<Chat Room>: " + chat_room])
        r = Message.objects.filter(room=chat_room)
        pages = set([msg.page for msg in r])
        for page in pages:
    	    writer.writerow(["<Page>: " + str(page)])
    	    r = Message.objects.filter(room=chat_room, page=page)
            for msgs in reversed(r) :
        # 		res.append({'id':msgs.id,'user':msgs.user,'msg':msgs.message,'time':msgs.time.strftime('%I:%M:%S %p').lstrip('0'),'gravatar':msgs.gravatar})
        	    writer.writerow([msgs.user + ": " + msgs.message])
    return response


def getSessionType(num):
    sessionTypes = {"0": "Category 3Dams", "1": "Free 3Dams", "2": "Priming 3Dams"}
    num = str(num)
    if num in sessionTypes.keys():
        return sessionTypes[num]
    else:
        return "None"

@login_required
def end_session(request):
    if request.method == "POST":
        sessionName = request.POST["sessionName"]
        s = Session.objects.filter(name=sessionName)
        if s:
            s[0].live = 0
            s[0].save()
    return HttpResponse('')

@login_required
def get_player_states(request, session):
    players = Player.objects.filter(session=session)
    # header = ["username", "session", "group", "location"]
    data = []
    for player in players:
        username = player.username
        group = player.group
        location = player.state
        row = [username, session, group, location]
        data.append(row)
    context_dict = {"data": data}
    return render(request, "group/controls/player_states.html", context_dict)

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'group/index.html')

@ensure_csrf_cookie
def Category3Dams(request, num="0"):
    '''All of the pages are handled via this function. The ajax requests
        are passed here so the view can return each of the appropriate
        html pages
    '''
    num = skip_pages(num)
    stop = stop_backpage(request, num)
    if stop != True:
        num = stop
    context_dict = {}
    context_dict = admin_options(context_dict)
    if num == "0":
        return render(request, 'group/Category3Dams.html')
    elif num == "1":
        context_dict = {}
        if request.method == "POST":
            session = request.POST["session"]
            print session
            username = request.POST['username']
            session = Session.objects.filter(name=session)
            if not session:
                message = "The session name is incorrect. Try again."
                context_dict = {"message": message}
                return render(request, 'group/Category3Dams.html', context_dict)
            db_usernames = [element.username for element in Player.objects.all()]
            if username in db_usernames:
                message = "The username has already been used. Try something else."
                context_dict = {"message": message}
                return render(request, 'group/Category3Dams.html', context_dict)
            if not session[0].active_players:
                session[0].active_players = json.dumps([username])
                session[0].save()
            else:
                active_players = json.loads(session[0].active_players)
                if not username in active_players:
                    active_players += [username]
                    session[0].active_players = json.dumps(active_players)
                    session[0].save()
                else:
                    message = "The username has already been used. Try something else."
                    context_dict = {"message": message}
                    return render(request, 'group/Category3Dams.html', context_dict)
            request.session["session"] = session[0].name
            request.session["username"] = username
            request.session["stype"] = session[0].stype
            return checkSType(request, num, context_dict)
        # else:
        #     context_dict["username"] = "None"
        # return render(request, 'group/Category3Dams_p1.html', context_dict)
    elif num == "2":
        player_check = check_initial_wait(request, num)
        if player_check == True:
            username = request.session["username"]
            session = Session.objects.filter(name=request.session["session"])[0]
            create_player(request, username, session)
            return checkSType(request, num, context_dict)
        else:
            print "is something wrong"
            if request.method == "POST" and "button_flag" in request.POST.keys() and request.POST["button_flag"] == "true":
                print "here"
                return render(request, 'group/Category3Dams_p1.html', context_dict)

            # return player_check
    # elif num == "2":
    #     player_check = check_initial_wait(request, num)
    #     if player_check == True:
    #         username = request.session["username"]
    #         session = Session.objects.filter(name=request.session["session"])[0]
    #         create_player(request, username, session)
    #         return checkSType(request, num, context_dict)
    #     else:
    #         print "is something wrong"
    #         return player_check
    elif num == "3":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p3.html', context_dict)
    elif num == "4":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p4.html', context_dict)
    elif num == "5":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p5.html', context_dict)
    elif num == "6":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p6.html', context_dict)
    elif num == "7":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p7.html', context_dict)
    elif num == "8":
        update_player_state(request.session["username"], num)
        context_dict = {"cjs": "p8"}
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p8.html', context_dict)
    elif num == "9":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p9.html', context_dict)
    elif num == "10":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p10.html', context_dict)
    elif num == "11":
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        # set the template extend path
        context_dict = {'template': 'group/Category3Dams_p11.html'}
        return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "12":
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        # set the template extend path
        context_dict = {'template': 'group/Category3Dams_p12.html'}
        return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "13":
        if request.method == "POST":
            # get user selections for dam 1 and store in session
            dam1 = request.POST['data']
            dam1 = [str(element) for element in json.loads(dam1)]
            request.session['dam1'] = dam1
            addPlayerData(request.session["username"], {"dam1": dam1})
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        # set the template extend path
        context_dict = {'template': 'group/Category3Dams_p13.html'}
        return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "14":
        if request.method == "POST":
            # get user selections for dam 2 and store in session
            dam2 = request.POST['data']
            dam2 = [str(element) for element in json.loads(dam2)]
            request.session['dam2'] = dam2
            addPlayerData(request.session["username"], {"dam2": dam2})
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        # set the template extend path
        context_dict = {'template': 'group/Category3Dams_p14.html'}
        return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "15":
        if request.method == "POST":
            # get user selections for dam 3 and store in session
            dam3 = request.POST['data']
            dam3 = [str(element) for element in json.loads(dam3)]
            request.session['dam3'] = dam3
            addPlayerData(request.session["username"], {"dam3": dam3})
        update_player_state(request.session["username"], num)
        dam1 = request.session['dam1']

        dam2 = request.session['dam2']
        # try:
        #     dam3 = request.session['dam3']
        # except KeyError:
        dam3 = json.loads(Player.objects.filter(username=request.session['username'])[0].answers)["dam3"]
        count = [dam1.count('present'), dam2.count('present'), dam3.count('present')]
        prob1 = [5, 10, 15, 20, 30, 40, 50]
        prob2 = [5, 9, 13, 17, 30, 43, 56]
        prob3 = [5, 8, 11, 14, 26, 42, 62]
        probs = [prob1[count[0]], prob2[count[1]], prob3[count[2]]]
        context_dict = {'dam1': dam1, 'dam2': dam2, 'dam3': dam3, 'count': count, 'probs': probs}
        return render(request, 'group/Category3Dams_p15.html', context_dict)
    elif num == "16-1":
        if request.method == "POST":
            damChoice = request.POST['data']
            damChoice = [str(element) for element in json.loads(damChoice)]
            print damChoice
            request.session['damChoice'] = damChoice
            addPlayerData(request.session["username"], {"damChoice": damChoice})
        update_player_state(request.session["username"], num[:2])
        ans1 = ['present', 'present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'not present']
        ans2 = ['present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'present', 'not present']
        ans3 = ['present', 'present', 'not present', 'not present', 'not present', 'not present', 'present', 'present', 'present']
        ans1_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'not present', 'present', 'not present', 'present']
        ans2_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'present', 'present', 'not present', 'not present']
        ans3_2 = ['not present', 'not present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'not present']
        userAns = request.session['dam1']
        # dam2 = request.session['dam2']
        # dam3 = request.session['dam3']
        ans_dict = {'1': ans1+ans1_2, '2': ans2+ans2_2, '3': ans3+ans3_2}
        set_num = request.session["info_set"]
        ans = ans_dict[str(set_num)][0::3]
        results = []
        for i, j in zip(ans, userAns):
            if i == j:
                results.append('correctly')
            else:
                results.append('wrong')
        context_dict = {'ans': ans, 'results': results, 'num': '1'}
        return render(request, 'group/Category3Dams_p16.html', context_dict)
    elif num == "16-2":
        if request.method == "POST":
            damChoice = request.POST['data']
            damChoice = [str(element) for element in json.loads(damChoice)]
            print damChoice
            request.session['damChoice'] = damChoice
            addPlayerData(request.session["username"], {"damChoice": damChoice})
        update_player_state(request.session["username"], num[:2])
        ans1 = ['present', 'present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'not present']
        ans2 = ['present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'present', 'not present']
        ans3 = ['present', 'present', 'not present', 'not present', 'not present', 'not present', 'present', 'present', 'present']
        ans1_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'not present', 'present', 'not present', 'present']
        ans2_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'present', 'present', 'not present', 'not present']
        ans3_2 = ['not present', 'not present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'not present']
        userAns = request.session['dam1']
        # dam2 = request.session['dam2']
        # dam3 = request.session['dam3']
        ans_dict = {'1': ans1+ans1_2, '2': ans2+ans2_2, '3': ans3+ans3_2}
        set_num = request.session["info_set"]
        ans = ans_dict[str(set_num)][1::3]
        results = []
        for i, j in zip(ans, userAns):
            if i == j:
                results.append('correctly')
            else:
                results.append('wrong')
        context_dict = {'ans': ans, 'results': results, 'num': '2'}
        return render(request, 'group/Category3Dams_p16.html', context_dict)
    elif num == "16-3":
        if request.method == "POST":
            damChoice = request.POST['data']
            damChoice = [str(element) for element in json.loads(damChoice)]
            print damChoice
            request.session['damChoice'] = damChoice
            addPlayerData(request.session["username"], {"damChoice": damChoice})
        update_player_state(request.session["username"], num[:2])
        ans1 = ['present', 'present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'not present']
        ans2 = ['present', 'present', 'not present', 'not present', 'not present', 'present', 'present', 'present', 'not present']
        ans3 = ['present', 'present', 'not present', 'not present', 'not present', 'not present', 'present', 'present', 'present']
        ans1_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'not present', 'present', 'not present', 'present']
        ans2_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'present', 'present', 'not present', 'not present']
        ans3_2 = ['not present', 'not present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'not present']
        userAns = request.session['dam1']
        # dam2 = request.session['dam2']
        # dam3 = request.session['dam3']
        ans_dict = {'1': ans1+ans1_2, '2': ans2+ans2_2, '3': ans3+ans3_2}
        set_num = request.session["info_set"]
        ans = ans_dict[str(set_num)][2::3]
        results = []
        for i, j in zip(ans, userAns):
            if i == j:
                results.append('correctly')
            else:
                results.append('wrong')
        context_dict = {'ans': ans, 'results': results, 'num': '3'}
        return render(request, 'group/Category3Dams_p16.html', context_dict)
    # elif num == "17":
    #     update_player_state(request.session["username"], num)
    #     # ans1 = ['present', 'present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'present']
    #     # ans2 = ['present', 'present', 'present', 'present', 'not present', 'present', 'present', 'not present', 'not present']
    #     # ans3 = ['not present', 'not present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'not present']
    #     ans1_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'not present', 'present', 'not present', 'present']
    #     ans2_2 = ['not present', 'not present', 'not present', 'present', 'not present', 'present', 'present', 'not present', 'not present']
    #     ans3_2 = ['not present', 'not present', 'present', 'present', 'not present', 'not present', 'present', 'not present', 'not present']
    #     dam1 = request.session['dam1'][3:]
    #     dam2 = request.session['dam2'][3:]
    #     dam3 = request.session['dam3'][3:]
    #     ans_dict = {'1': ans1, '2': ans2, '3': ans3}
    #     set_num = request.session["info_set"]
    #     ans = ans_dict[str(set_num)]
    #     userAns = []
    #     for i in range(3):
    #         userAns += [dam1[i], dam2[i], dam3[i]]
    #     results = []
    #     for i, j in zip(ans, userAns):
    #         if i == j:
    #             results.append('correctly')
    #         else:
    #             results.append('wrong')
    #     damChoice = request.session['damChoice']
    #     if damChoice[0] != 'Dam 1':
    #         damChoice = "wrong"
    #     else:
    #         damChoice = "correct"
    #     context_dict = {'ans': ans, 'results': results, 'damChoice': damChoice}
    #     return render(request, 'group/Category3Dams_p17.html', context_dict)
    elif num == "18":
        update_player_state(request.session["username"], num)
        if request.method == "POST" and add_data(request, "damChoice"):
            damChoice = request.POST['damChoice']
            request.session['damChoice'] = damChoice
            addPlayerData(request.session["username"], {"damChoice": damChoice})
        # return checkWait(request, num, context_dict, flag=True) # check flag=False
        return render(request, 'group/Category3Dams_p18.html', context_dict)
    elif num == "19":
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        chat_room = request.session["chat_room"]
        damChoice = request.session["damChoice"]
        if type(damChoice) == list:
            damChoice = request.session['damChoice'][0]
        else:
            damChoice = request.session['damChoice']
        # set the template extend path
        context_dict = {'damChoice': damChoice, 'username': request.session["username"], "chat_room": chat_room}
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            return checkSType(request, num, context_dict, set_num)
        # return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "20":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p20.html', context_dict)
    elif num == "21":
        update_player_state(request.session["username"], num)
        if request.method == "POST" and "data" in request.POST.keys() and add_data(request, "dam1_group"):
            # get user selections for dam 1 and store in session
            dam1 = request.POST['data']
            dam1 = [str(element) for element in json.loads(dam1)]
            request.session['dam1_group'] = dam1
            addPlayerData(request.session["username"], {"dam1_group": dam1})
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            print "here"
            chat_room = request.session["chat_room"]
            set_num = request.session["info_set"]
            damChoice = request.session['damChoice']
            # set the template extend path
            context_dict = {'template': 'group/Category3Dams_p21.html', 'damChoice': damChoice, 'username': request.session["username"], "chat_room": chat_room}
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "22":
        update_player_state(request.session["username"], num)
        return render(request, 'group/Category3Dams_p22.html', context_dict)
    elif num == "23":
        update_player_state(request.session["username"], num)
        if request.method == "POST" and "data" in request.POST.keys() and add_data(request, "dam2_group"):
            # get user selections for dam 1 and store in session
            dam2 = request.POST['data']
            dam2 = [str(element) for element in json.loads(dam2)]
            request.session['dam2_group'] = dam2
            addPlayerData(request.session["username"], {"dam2_group": dam2})
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            chat_room = request.session["chat_room"]
            set_num = request.session["info_set"]
            damChoice = request.session['damChoice']
            # set the template extend path
            context_dict = {'template': 'group/Category3Dams_p23.html', 'damChoice': damChoice, 'username': request.session["username"], "chat_room": chat_room}
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "24":
        update_player_state(request.session["username"], num)
        return render(request, 'group/Category3Dams_p24.html', context_dict)
    elif num == "25":
        update_player_state(request.session["username"], num)
        if request.method == "POST" and "data" in request.POST.keys() and add_data(request, "dam3_group"):
            # get user selections for dam 1 and store in session
            dam3 = request.POST['data']
            dam3 = [str(element) for element in json.loads(dam3)]
            print dam3
            request.session['dam3_group'] = dam3
            addPlayerData(request.session["username"], {"dam3_group": dam3})
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            chat_room = request.session["chat_room"]
            set_num = request.session["info_set"]
            damChoice = request.session['damChoice']
            # set the template extend path
            context_dict = {'template': 'group/Category3Dams_p25.html', 'damChoice': damChoice, 'username': request.session["username"], "chat_room": chat_room}
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "26":
        update_player_state(request.session["username"], num)
        return render(request, 'group/Category3Dams_p26.html', context_dict)
    elif num == "27":
        if request.method == "POST" and "data" in request.POST.keys() and add_data(request, "damChoiceGroup"):
            finalDam = request.POST["data"]
            finalDam = [str(element) for element in json.loads(finalDam)]
            request.session["damChoiceGroup"] = finalDam
            addPlayerData(request.session["username"], {"damChoiceGroup": finalDam})
        update_player_state(request.session["username"], num)
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            session = request.session["session"]
            chat_room = request.session["chat_room"]
            players = Player.objects.filter(session=session, chat_room=chat_room, state=num)
            final_choice = []
            for player in players:
                ans_dict = json.loads(player.answers)
                final_choice.append(ans_dict["damChoiceGroup"][0])
            context_dict["count"] = [final_choice.count("Dam 1"), final_choice.count("Dam 2"), final_choice.count("Dam 3")]
            def argmax(lst):
                return lst.index(max(lst))
            group_choice = argmax(context_dict["count"]) + 1
            context_dict["selection"] = group_choice
            return render(request, 'group/Category3Dams_p27.html', context_dict)
        # return render(request, 'group/Category3Dams_p27.html', context_dict)
    elif num == "28":
        update_player_state(request.session["username"], num)
        return render(request, 'group/Category3Dams_p28.html', context_dict)


def Free3Dams(request, num):
    context_dict = {}
    stop = stop_backpage(request, num)
    if stop != True:
        num = stop
    context_dict = admin_options(context_dict)
    if num == "18":
        update_player_state(request.session["username"], num)
        return checkWait(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p18.html', context_dict)
    elif num == "19":
        update_player_state(request.session["username"], num)
        set_num = request.session["info_set"]
        chat_room = request.session["chat_room"]
        print "chat_room", chat_room
        damChoice = request.session['damChoice'][0]
        # set the template extend path
        context_dict = {'damChoice': damChoice, 'username': request.session["username"], "chat_room": chat_room}
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            return checkSType(request, num, context_dict, set_num)
        # return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
    elif num == "20":
        update_player_state(request.session["username"], num)
        return checkSType(request, num, context_dict)
        # return render(request, 'group/Category3Dams_p20.html', context_dict)
    elif num == "21":
        if request.method == "POST" and "finalDamChoice" in request.POST.keys() and add_data(request, "damChoiceGroup"):
            finalDam = request.POST["finalDamChoice"]
            request.session["damChoiceGroup"] = finalDam
            addPlayerData(request.session["username"], {"damChoiceGroup": finalDam})
        update_player_state(request.session["username"], num)
        context_dict = {}
        out = checkWait(request, num, context_dict, check=True)
        if out != True:
            return out
        else:
            session = request.session["session"]
            chat_room = request.session["chat_room"]
            players = Player.objects.filter(session=session, chat_room=chat_room, state=num)
            final_choice = []
            for player in players:
                ans_dict = json.loads(player.answers)
                final_choice.append(ans_dict["damChoiceGroup"])
            context_dict["count"] = [final_choice.count("Dam 1"), final_choice.count("Dam 2"), final_choice.count("Dam 3")]
            def argmax(lst):
                return lst.index(max(lst))
            group_choice = argmax(context_dict["count"]) + 1
            # if context_dict["count"][0] == context_dict["count"][1] == context_dict["count"][2]:
            #     for player in players:
            #         ans_dict = json.loads(player.answers)
            #         if "tie_choice" in ans_dict:
            #             tie_choice = ans_dict["tie_choice"]
            #             break
            #         else:
            #             addPlayerData(request.session["username"], {"tie_choice": group_choice})
            context_dict["selection"] = group_choice
            return render(request, 'group/Free3Dams/Free3Dams_p21.html', context_dict)
    elif num == "22":
        update_player_state(request.session["username"], num)
        return render(request, 'group/Free3Dams/Free3Dams_p22.html', context_dict)

def check_initial_wait(request, num):
    if request.method == "POST":
        session = request.session["session"]
        session = Session.objects.filter(name=session)
        active_players = json.loads(session[0].active_players)
        print session[0].players
        # if 3 == 3:
        if len(active_players) == int(session[0].players):
            return True
        else:
            print "not enough active players"
            # return render(request, 'group/wait.html', {"num": num})
            return HttpResponse('')

def checkWait(request, num, context_dict, check=False, flag=True):
    if request.method == "POST" and flag: # why do we have the flag
        session = request.session["session"]
        chat_room = request.session["chat_room"]
        players = Player.objects.filter(session=session, chat_room=chat_room)
        players = [player for player in players if int(player.state) >= int(num)]
        print 'test', players
        # if 3 == 3: # change to len(players)
        if len(players) == 3:
            if check == True:
                return True
            return render(request, 'group/Category3Dams_p{0}.html'.format(num), context_dict)
        # don't break js by returning a new page via ajax
        # if "button_flag" in request.POST.keys() and request.POST["button_flag"] == "true":
        # check if the request is via ajax or a form/button
        # only return something if it is the latter
        if "ajax" in request.POST.keys():
            print "ajax"
            return HttpResponse('')
        if request.session["stype"] == 0:
            return render(request, 'group/wait.html', {"num": num})
        if request.session["stype"] == 1:
            return render(request, 'group/Free3Dams/wait.html', {"num": num})
        if request.session["stype"] == 2:
            return render(request, 'group/Priming3Dams/wait.html', {"num": num})
    if request.session["stype"] == 0:
        return render(request, 'group/wait.html', {"num": num})
    if request.session["stype"] == 1:
        return render(request, 'group/Free3Dams/wait.html', {"num": num})
    if request.session["stype"] == 2:
        return render(request, 'group/Priming3Dams/wait.html', {"num": num})

def add_data(request, key):
        username = request.session["username"]
        player = Player.objects.filter(username=username)[0]
        try:
            ans_dict = json.loads(player.answers)
        except ValueError:
            return True
        if key not in ans_dict.keys():
            return True
        return False


def getInfoSet(request):
    '''attempt to retrieve info_set from the session
        if no info_set then generate one randomly format
        debugging purposes
    '''
    if request.session['set_num']:
        return request.session['set_num']
    return randomInfoSet()


def randomInfoSet():
    '''this function determins which info_set to present to the user
        this is only a temporary implementation
    '''

    return randint(1,3)

# def create_player(request, username, session):
#     from random import randint
#     if not "group" in request.session.keys():
#         total_num_players = session.players
#         num_groups = int(total_num_players)/float(3)
#         num_groups = range(int(num_groups))
#         groups = json.loads(session.groups)
#         full_groups = []
#         for key in groups.keys():
#             if groups[str(key)] == 3:
#                 full_groups.append(int(key))
#         useable_groups = list(set(num_groups)-set(full_groups))
#         rand_index = randint(0,len(useable_groups)-1)
#         group = useable_groups[rand_index]
#         groups[str(group)] += 1
#         session.groups = json.dumps(groups)
#         session.save()
#         request.session["group"] = group

#     if not "info_set" and not "chat_room" in request.session.keys():
#         if groups[str(group)] < 0:
#             chat_room = create_chat_room()
#             info_set = randint(1,3)
#         else:
#             chat_room = Player.objects.filter(session=session.name, group=group)[0].chat_room
#             info_sets = [player.info_set for player in Player.objects.filter(session=session.name, group=group)]
#             available_info_sets = list({1,2,3} - set(info_sets))
#             info_set = available_info_sets[randint(0,len(available_info_sets)-1)]
#         request.session['info_set'] = info_set
#         request.session["chat_room"] = chat_room
#     info_set = request.session['info_set']
#     chat_room = request.session["chat_room"]
#     group = request.session["group"]
#     state = 2
#     p = Player(username=username, session=session.name, group=group, info_set=info_set, state=state, chat_room=chat_room)
#     p.save()
#     return

def create_player(request, username, session):
    '''this function determins which info_set to present to the user
        and creates the player in the db
    '''
    from random import randint
    groups = json.loads(session.groups)
    group = max([int(key) for key in groups.keys()])
    if groups[str(group)] == 3:
        group += 1
        groups[str(group)] = 1
        info_set = randint(1,3)
        state = 2
        chat_room = create_chat_room()

        print "chat_room", chat_room
        p = Player(username=username, session=session.name, group=group, info_set=info_set, state=state, chat_room=chat_room)
        p.save()
        request.session['info_set'] = info_set
        request.session["chat_room"] = chat_room
        session.groups = json.dumps(groups)
        session.save()
        return
    if groups[str(group)] < 3:
        groups[str(group)] += 1
        if Player.objects.filter(session=session.name, group=group):
            chat_room = Player.objects.filter(session=session.name, group=group)[0].chat_room
            info_sets = [player.info_set for player in Player.objects.filter(session=session.name, group=group)]
            available_info_sets = list({1,2,3} - set(info_sets))
            info_set = available_info_sets[randint(0,len(available_info_sets)-1)]

        else:
            chat_room = create_chat_room()
            info_set = randint(1,3)
        state = 2
        print group
        p = Player(username=username, session=session.name, group=group, info_set=info_set, state=state, chat_room=chat_room)
        p.save()
        request.session['info_set'] = info_set
        request.session["chat_room"] = chat_room
        session.groups = json.dumps(groups)
        session.save()
        return

def addPlayerData(username, data):
    player = Player.objects.filter(username=username)[0]
    if not player.answers:
        ans_dict = {}
    else:
        ans_dict = json.loads(player.answers)
    ans_dict.update(data)
    player.answers = json.dumps(ans_dict)
    player.save()
    return

def create_chat_room():
    import random
    randRoom = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
    return randRoom

def update_player_state(username, num):
    player = Player.objects.filter(username=username)[0]
    if player.time:
        time = json.loads(player.time)
        last_time = parser.parse(time["last_time"])
        time["last_time"] = str(datetime.datetime.now())
        print last_time
        delta = datetime.datetime.now()-last_time
        delta = delta.total_seconds()
        time[str(int(num)-1)] = delta
        player.time = json.dumps(time)
        player.save()
    else:
        time = {"last_time": str(datetime.datetime.now())}
        player.time = json.dumps(time)
        player.save()
    player.state = num
    player.save()
    return

def stop_backpage(request, num):
    try:
        if int(num) <= 3:
            return True
        if "username" in request.session.keys():
            username = request.session['username']
            if len(Player.objects.filter(username=username)) > 0:
                player = Player.objects.filter(username=username)[0]
            else:
                return True
            current_page = player.state
            try:
                if int(num) <= int(current_page):
                    print "we made it"
                    print num, current_page
                    return current_page
                    # return HttpResponse("Please click your forward button!")
            except ValueError:
                print "stop1"
                return True
    except AttributeError:
        print "stop2"
        return True
    print "stop3"
    return True


def checkSType(request, num, context_dict, set_num=False):
    print type(request.session["stype"])
    if request.session["stype"] == 0:
        print "wrong"
        if set_num:
            context_dict['template'] = 'group/Category3Dams_p{0}.html'.format(num)
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
        return render(request, 'group/Category3Dams_p{0}.html'.format(num), context_dict)
    if request.session["stype"] == 1:
        # print "Free", request.session["chat_room"]
        if set_num:
            context_dict['template'] = 'group/Free3Dams/Free3Dams_p{0}.html'.format(num)
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
        return render(request, 'group/Free3Dams/Free3Dams_p{0}.html'.format(num), context_dict)
    if request.session["stype"] == 2:
        # print "here"
        if set_num:
            context_dict['template'] = 'group/Priming3Dams/Priming3Dams_p{0}.html'.format(num)
            return render(request, 'group/info_sets/set{0}.html'.format(set_num), context_dict)
        return render(request, 'group/Priming3Dams/Priming3Dams_p{0}.html'.format(num), context_dict)

def skip_pages(num):
    # pages to skip
    pages = [8, 9, 12, 13, 14, 15, 16, 17]
    try:
        num = int(num)
        while int(num) in pages:
            num += 1
        return str(num)
    except ValueError:
        return num

def admin_options(context_dict):
    payment = False
    context_dict["payment_flag"] = payment
    return context_dict

