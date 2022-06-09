from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
nom=[]
nom.append("Inconnu")
def Connexion():
    """Shows basic usage of the People API.
        Prints the name of the first 10 connections.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_conc.pickle'):
        with open('token_conc.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_conc.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_conc.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    return service

SERVICE=Connexion()

def Get_Groups():
    conect = SERVICE.contactGroups().list(
        pageSize=1000,
        groupFields='name,groupType,memberCount').execute()
    group = {}
    for person in conect['contactGroups']:
        if 'etag' in list(person.keys()):
            group[person['name'].lower()] = person['resourceName'].split('/')[1]
    #print(group)
    return group


def Get_code_group(num):

    results = SERVICE.people().connections().list(
        resourceName='people/me',
        pageSize=1500,
        personFields='names,phoneNumbers,memberships').execute()
    connections = results.get('connections', [])
    i = 1
    for person in connections:
        names = person.get('names', [])
        emails = person.get('emailAddresses', [])
        phones = person.get('phoneNumbers')
        mems = person.get('memberships')[0]['contactGroupMembership']['contactGroupId']

        if names :
            name = names[0].get('displayName')
            phone = phones[0]['value'].replace(' ', '')
            if phone==num:
                nom[0]=name
                return mems

            #print(f"\n{i}. {name} -     {phone} {phone.replace(' ', '')}")
            i += 1
    return None

def if_memebership(num,groupe):
    groups=Get_Groups()
    code_gp=Get_code_group(num)
    #print(code_gp)
    if code_gp is None:
        return False
    return code_gp==groups[groupe.lower()]

def Get_name():
    return nom[0]
#print(if_memebership('0662959698','Amis'))
#Get_code_group(12)