from __future__ import print_function
import time

print('==============================')
print('+ BOTAMINDER TOKEN GENERATOR +')
print('==============================')
print('''This script can be used to generate the token used to update the arduino with latest time and events\
in a quick fashion. If youre opening running this file for the first time, Try googlecalendar mode which can automatically 
fetch your events from your google calendar.  
\nONLY EMAIL IDS REGISTERED UNDER THE IIT MANDI ORGANISATION WORK IN GOOGLECALENDAR MODE!! (EG: XXXXXX@students.iitmandi.ac.in)\n
SEE FULL DOCUMENTATION ON THE GITHUB REPO FOR STEP BY STEP INSTRUCTIONS FOR EVERY MODE.\n''')

print("modes available:\n1. googlecalendar\n2. manual\n3. eventsonly\n4. healthonly\n5. silent\n")

mode, mode1 = "",""

def ask_for_mode():
    global mode, mode1
    mode=input('enter user mode:').lower()
    mode1 = mode



def manual():
    no=int(input('enter the number of events'))
    s_name=[]
    s_st=[]
    s_et=[]
    
    global mode
    for i in range(no):
        q='enter the title of event '+str(i+1)+':'
        name=input(q)
        st=(input('enter start time hour:'))
        et=(input('enter end time hour:'))
        s_name.append(name)
        s_st.append(st)
        s_et.append(et)
    n='"'+s_name[0]+'"'
    st1='(long)'+str(s_st[0])+'*3600'
    et1='(long)'+str(s_et[0])+'*3600'
    for i in s_name[1:]:
        n+=','+'"'+i+'"'
    for i in s_st[1:]:
        st1+=','+'(long)'+str(i)+'*3600'
    for i in s_et[1:]:
        et1+=','+'(long)'+str(i)+'*3600'
        
    lt=(time.localtime(time.time())[3:6])
    print("COPY THIS TOKEN TO ARDUINO SKETCH")
    print('\n\n\n') 
    print('long time[3] = {'+str(lt[0])+','+str(lt[1])+','+str(lt[2])+'};')
    print('int events = ',no,';')
    print('String eventName[',no,'] = {',n,'};')
    print('long eventStartTime[2] = {',st1,'};')
    print('long eventEndTime[2] = {',et1,'};')
    print('int eventScrollingSpeed = 4;'+'\n'+\
          'long waterReminder = 3*3600;'+'\n'+\
          'long breakReminder = 4*3600;'+'\n'+\
          'long skippingBreak = 17*3600;')
    print('String userMode = "'+mode+'";')
    print('\n\n')



def googlecalendar():
    '''
    Workflow for OAUTH Authentication referenced from https://qxf2.com/blog/google-calendar-python/
    '''
    import httplib2
    import os
    import googleapiclient.discovery as discovery
    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage
     
    import datetime
    
    global mode, mode1
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'auth/authorizeApp.json'
    APPLICATION_NAME = 'botaminder'
    if mode ==  "googlecalendar":
        mode = "gcal"
     
     
    def get_credentials():
        """Gets valid user credentials from storage.
     
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
     
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')
     
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
 
    # This code is to fetch the calendar ids shared with me
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
    page_token = None
    calendar_ids = []
    count = 1
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        print("\nThe following calendars are available in your google account. Please select one:\n\
        (Note: The calendar name is your email, if you do not have multiple calendars)\n")
        for calendar_list_entry in calendar_list['items']:
            print(count, calendar_list_entry['id'])
            count+=1
            print('\n')
        calendar_id = input("Please enter one of the above or enter 1,2,3 to select: ").strip()
        
        if len(calendar_id) == 1:
            calendar_ids.append(calendar_list['items'][int(calendar_id)-1]['id'])
        else:
            for calendar_list_entry in calendar_list['items']:
                if calendar_id in calendar_list_entry['id']:
                    calendar_ids.append(calendar_list_entry['id'])
        
        if not calendar_ids:
            print('''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                     + NO SUCH CALENDAR FOUND. PLEASE SELECT ONE OF THE DISPLAYED IDS+
                     +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++''')
        else:
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    current_date = datetime.date.today()
    start_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 00, 00, 00, 0).isoformat() + 'Z'
    end_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59, 0).isoformat() + 'Z'
 
    for calendar_id in calendar_ids:
        count = 0
        eventsResult = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents = True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            print('No upcoming events found in your calendar.')
            tryagain = input("Retry Again?.  Enter y/n:").strip()
            if tryagain == "y":
                googlecalendar()
            elif tryagain == "n":
                print("Switching to Manual mode...\n")
                manual()
            else:
                print("Wrong Input. Just enter y or n.")
        else:
            s_name=[]
            s_st=[]
            s_et=[]
            no=0
            for event in events:
                no+=1
                s_name.append(event['summary'])
                s_st.append(event['start']['dateTime'].split('T')[1].split('+')[0].split(':')[0:2])
                s_et.append(event['end']['dateTime'].split('T')[1].split('+')[0].split(':')[0:2])
            n='"'+s_name[0]+'"'
            st1='(long)'+str(s_st[0][0])+'*3600+(long)'+str(s_st[0][1])+'*60'
            et1='(long)'+str(s_et[0][0])+'*3600+(long)'+str(s_et[0][1])+'*60'
            for i in s_name[1:]:
                n+=','+'"'+i+'"'
            for i in s_st[1:]:
                st1+=','+'(long)'+str(i[0])+'*3600+(long)'+str(i[1])+'*60'
            for i in s_et[1:]:
                et1+=','+'(long)'+str(i[0])+'*3600+(long)'+str(i[1])+'*60'
            
            lt=(time.localtime(time.time())[3:6]) 
            print(lt)
            print('\n\n\n\n')    
            print('long time[3] = {'+str(lt[0])+','+str(lt[1])+','+str(lt[2])+'};')
            print('int events = ',no,';')
            print('String eventName[',no,'] = {',n,'};')
            print('long eventStartTime[', no, '] = {',st1,'};')
            print('long eventEndTime[',no,'] = {',et1,'};')
            print('int eventScrollingSpeed = 4;'+'\n'+\
                  'long waterReminder = 3*3600;'+'\n'+\
                  'long breakReminder = 4*3600;'+'\n'+\
                  'long skippingBreak = 17*3600;')
            print('String userMode = "'+mode+'";')
            print('\n\n')



ask_for_mode()
if mode == "googlecalendar" or mode == "1":
    mode = "googlecalendar"
    googlecalendar()

elif mode == "manual" or mode == "2":
    mode = "manual"
    manual()

elif mode == "healthonly" or mode == "4":
    mode = "health"
    print("HEALTH MODE SELECTED")
    print("======================")
    print("Only Health events will ring a alarm.")
    mode1 = input("Select one of the methods to fetch events:\n1. manual\n2. googlecalendar\n\nSelect One: ").strip()
    if mode1 == "manual" or mode1 == "1":
        manual()
    elif mode1 == "googlecalendar" or mode1 == "2":
        googlecalendar()
    else:
        print("Wrong Input.. TRY AGAIN")

elif mode == "eventsonly" or mode == "3":
    mode='events'
    print("Events ONLY MODE SELECTED")
    print("======================")
    print("Only Calendar events will ring a alarm.")
    mode1 = input("Select one of the methods to fetch events:\n1. manual\n2. googlecalendar\n\nSelect One: ").strip()
    if mode1 == "manual" or mode1 =="1" :
        manual()
    elif mode1 == "googlecalendar" or mode1=="2":
        googlecalendar()
    else:
        print("Wrong Input.. TRY AGAIN")

elif mode == "silent" or mode == "5":
    mode='silent'
    print("SILENT MODE SELECTED")
    print("====================")
    mode1 = input("NO EVENTS WILL RING AN ALARM.\nIf you want your events to be available in the arduino to display, \
    Select one of the methods to fetch events:\n1. manual\n2. googlecalendar\n\nSelect One or leave blank to use the project as a desk clock: ").strip()
    if mode1 == "":
        print('\n\n\n\n')
        lt=(time.localtime(time.time())[3:6])  
        print('long time[3] = {'+str(lt[0])+','+str(lt[1])+','+str(lt[2])+'};')
        print('int events = 0;')
        print('String eventName[1] = {"No Events"};')
        print('long eventStartTime[1] = {(long)86399};')
        print('long eventEndTime[1] = {(long)86399};')
        print('int eventScrollingSpeed = 4;'+'\n'+\
              'long waterReminder = (long)86399;'+'\n'+\
              'long breakReminder = (long)86399;'+'\n'+\
              'long skippingBreak = (long)86399;')
        print('String userMode = "'+'silent'+'";')
        print('\n\n')
    elif mode1 == "manual" or  mode1=="1":
        manual()
    elif mode1 == "googlecalendar" or mode1=="2" :
        googlecalendar()
    else:
        print("Wrong Input. TRY AGAIN")
        
else:
    print("WRONG INPUT! SELECT ONE OF THE ABOVE!!!\ntry again")
    
        
    
    

