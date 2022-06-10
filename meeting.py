
from datetime import datetime, timedelta
import pickle
import os.path
import datefinder
import pytz
from dateutil.parser import parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
def Connexion():
    """Shows basic usage of the People API.
        Prints the name of the first 10 connections.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    return service

service=Connexion()

def Busy():

    result = service.calendarList().list().execute()

    #calendar_id = result['items'][0]['id'] false
    calendar_id='thesaurusnlp@gmail.com' # ou calendar_id="primary"
    now = datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


    results = service.events().list(calendarId="primary",singleEvents=True,timeMin=now,orderBy='startTime').execute()
    #print(results['items'])
    c=results['items']
    busy=[]

    for i in c:
        #print(i)
        dt=i['summary']
        #print(dt)

        if In_event(i):
            busy.append(dt)
            #print(i)

    return busy

def Check_free(name):
    ex=True

    en_dt=datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")

    while ex:

        bor=Get_born(en_dt,3,25)
        #print(bor)
        results = service.events().list(calendarId="primary", singleEvents=True, timeMin=bor[0],
                                        timeMax=bor[1], orderBy='startTime').execute()
        c = results['items']
        #print(c)
        if(len(c)==0):
            ex=False
        else:
           en_dt = c[0]['end']['dateTime']

    service.events().insert(calendarId="primary", body=Create_event(en_dt,'Recall '+name)).execute()
    matches = list(datefinder.find_dates(en_dt))
    if len(matches):
        start_time = matches[0]
        ret = (start_time + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

    return ret

def Get_born(end_dt,inf,sup):
    born=[]
    now = end_dt
    matches = list(datefinder.find_dates(now))
    if len(matches):
        start_time = matches[0]
        st_time = (start_time + timedelta(minutes=inf)).strftime("%Y-%m-%dT%H:%M:%S%z")
        end_time = (start_time + timedelta(minutes=sup)).strftime("%Y-%m-%dT%H:%M:%S%z")

    born.append(st_time)
    born.append(end_time)
    return born

def In_event(inter):
    s_dt = parse(inter['start']['dateTime'])
    e_dt = parse(inter['end']['dateTime'])
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    #print(s_dt,now,e_dt)

    return s_dt<now<e_dt



def Pass_date(str):
    c = parse(str)
    ct = datetime.datetime.now().astimezone()
    return (c<ct)





def Create_event(start_time_str, summary, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        st_time = (start_time + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (start_time + timedelta(minutes=25)).strftime("%Y-%m-%dT%H:%M:%S")

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': st_time,
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Paris',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event


#print(Busy());

#print(Check_free("merd"))

