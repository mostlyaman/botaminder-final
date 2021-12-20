from __future__ import print_function
import time
lt=(time.localtime(time.time())[2:5])
mode=input('enter user mode:')
no=0
s_name=[]
s_st=[]
s_et=[]
if mode=='manual':
    no=int(input('enter the number of events'))
    for i in range(no):
        q='enter the title of event '+str(i+1)+':'
        name=input(q)
        st=int(input('enter start time hour:'))
        et=int(input('enter end time hour:'))
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
elif mode=='googlecalendar':    
    import httplib2
    import os
     
    # from apiclient import discovery
    # Commented above import statement and replaced it below because of
    # reader Vishnukumar's comment
    # Src: https://stackoverflow.com/a/30811628
     
    import googleapiclient.discovery as discovery
    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage
     
    import datetime
    
    email=input('Enter your Email Id:').strip()
     
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
     
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'authorizeApp.json'
    APPLICATION_NAME = 'botaminder'
     
     
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
     
     
    def main():
        """Shows basic usage of the Google Calendar API.
     
        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
     
        # This code is to fetch the calendar ids shared with me
        # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
        page_token = None
        calendar_ids = []
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if email in calendar_list_entry['id']:
                    calendar_ids.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
     
        # This code is to look for all-day events in each calendar for the month of September
        # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
        # You need to get this from command line
        # Bother about it later!
        start_date = datetime.datetime(2021, 12, 19, 00, 00, 00, 0).isoformat() + 'Z'
        end_date = datetime.datetime(2021, 12, 21, 23, 59, 59, 0).isoformat() + 'Z'
     
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
                print('No upcoming events found.')
            
            
            
            s_name=[]
            s_st=[]
            s_et=[]
            no=0
            lt=(time.localtime(time.time())[2:5])
            for event in events:
                no+=1
                s_name.append(event['summary'])
                s_st.append(event['start']['dateTime'].split('T')[1].split('+')[0])
                s_et.append(event['end']['dateTime'].split('T')[1].split('+')[0])
            n='"'+s_name[0]+'"'
            st1='(long)'+str(s_st[0])+'*3600'
            et1='(long)'+str(s_et[0])+'*3600'
            for i in s_name[1:]:
                n+=','+'"'+i+'"'
            for i in s_st[1:]:
                st1+=','+'(long)'+str(i)+'*3600'
            for i in s_et[1:]:
                et1+=','+'(long)'+str(i)+'*3600'
                
            print('\n\n\n\n')    
            print('long time[3] = {'+str(lt[0])+','+str(lt[1])+','+str(lt[2])+'};')
            print('int events = ',no,';')
            print('String eventName[',no,'] = {',n,'};')
            print('long eventStartTime[2] = {',st1,'};')
            print('long eventEndTime[2] = {',et1,'};')
            print('int eventScrollingSpeed = 4;'+'\n'+\
                  'long waterReminder = 3*3600;'+'\n'+\
                  'long breakReminder = 4*3600;'+'\n'+\
                  'long skippingBreak = 17*3600;')
            print('String userMode = "'+'g cal'+'";')
            print('\n\n')
            
            
            
            
            
    main()
 
 

