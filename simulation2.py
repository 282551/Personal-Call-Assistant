from importlib.machinery import SourceFileLoader
from playsound import playsound
import os
from gtts import gTTS
import time
import webbrowser

language = 'en'

nlp = SourceFileLoader("module.name", "nlp.py").load_module()
#trans = SourceFileLoader("module.name", "tota.py").load_module()
contacts = SourceFileLoader("module.name", "contact.py").load_module()
calen = SourceFileLoader("module.name", "meeting.py").load_module()
Gorgias = SourceFileLoader("module.name", "gorgias.py").load_module()
rec = SourceFileLoader("module.name", "join_audio.py").load_module()
tr = SourceFileLoader("module.name", "Speech2Text Hugging Face.py").load_module()
#print(calen.Busy())
#print(contacts.if_memebership('0662959698','Amis'))
facts=[]
facts.append("at_work")
Bus=calen.Busy()
#print(Bus)




prof_thesaurus=['Professional','work','taf','boss','colleague','co-worker','human resources','client','Secretary','provider','job','meeting','reunion']
school_thesaurus=['school','study','academy','teacher','professor','schoolmate','department','faculty','institute','institution','seminary','university','college','discipline','establishment','schoolhouse']
fam_thesaurus=['brother','personal','family','household','sister','son','aunt','mother','cousin','family line','family unit','kinsperson','father','wife','parents','uncles','familial','dad','daddy','daughter','daughter in law','children','caring','breadwinner','husband','in-law','mama','niece','papa','twin brother','twin sister','son','spouse','nephew','mother in law','mom','mommy','child','ex wife','ex husband','married','fam','born','half-sister','grandmother','grandfather','half-brother','fiancee','marital','parent','familie','marriage','dynasty','couple']
friend_thesaurus=['friend','personal','companion','boon companion','bosom friend','best friend','close friend','intimate','confidante','confidant','soul mate','alter ego','second self','shadow','playmate','playfellow','classmate','schoolmate','workmate','ally','comrade','pal','bosom pal','buddy','bosom buddy','chum','sidekick','cully','crony','main man','mate','amigo','compadre','homie','bro']


def reason_choice_identify(txt):
    if(len(nlp.find_keywords(txt,prof_thesaurus))!=0):
        return 2
    elif(len(nlp.find_keywords(txt,school_thesaurus))!=0):
        return 3
    elif (len(nlp.find_keywords(txt, friend_thesaurus)) != 0):
        return 1
    elif (len(nlp.find_keywords(txt, fam_thesaurus)) != 0):
        return 1
    else:
        return 4


def identity(txt,num):
    if(len(nlp.find_keywords(txt,fam_thesaurus))!=0) and contacts.if_memebership(num,'family'):
        st="familly_member("+str(num)+")"
        facts.append(st)
    return num


def decision_reason(n):
    if n==1:
        personal()
    else:
        sorry()

def decision_staf(num):
    if len(Bus) != 0:
        facts.append("at_meeting")
    #print(facts)

    if  Gorgias.Allow(facts, num):
        wait_pls()
    else:
        if len(Bus) != 0:
            sorry_w_ex()
        else:
            sorry()


def Agent_response(audio):
    #txt=trans.transcribe(audio)
    txt = tr.transc(audio)
    rec.Add_conv(audio)
    print(txt)
    webbrowser.open(audio)
    time.sleep(7)
    return txt

def welcome():
    mytext = "Personal assistant, to Mr. Donald, Hello.\nWhat is the reason for your call? . \n'Personal', 'Professional', 'School' or 'Other'."
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\debian.wav")
    print(mytext)
    rec.Add_conv("records\\debian.wav")
    webbrowser.open('records\\debian.wav')
    time.sleep(13)


def personal():
    mytext = "Are you family or friends of Mr. Donald?"
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\staf.wav")
    print(mytext)
    rec.Add_conv("records\\staf.wav")
    webbrowser.open('records\\staf.wav')
    time.sleep(5)

def wait_pls():
    mytext = "Wait a moment, Mr. Donald will be yours."
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\wai.wav")
    print(mytext)
    rec.Add_conv("records\\wai.wav")
    webbrowser.open('records\\wai.wav')
    time.sleep(5)
    Exit()

def Rendez_vous():
    mytext = "he will call you back at  "+calen.Check_free(contacts.Get_name())+" ."
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\meet.wav")
    print(mytext)
    rec.Add_conv("records\\meet.wav")
    return "meet.wav"

def sorry_w_ex():
    mytext = "I'm sorry, but Mr. Donald, is in, a " + Bus[0] + " ."
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\sorry.wav")
    print(mytext)
    rec.Add_conv("records\\sorry.wav")
    webbrowser.open('records\\sorry.wav')
    time.sleep(4)
    webbrowser.open(Rendez_vous())
    time.sleep(9)
    Exit()

def sorry():
    mytext = "I'm sorry, but Mr. Donald is not available at the moment."
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("records\\sorry.wav")
    print(mytext)
    rec.Add_conv("records\\sorry.wav")
    webbrowser.open('records\\sorry.wav')
    time.sleep(5)
    webbrowser.open(Rendez_vous())
    time.sleep(9)
    Exit()

def Exit():
    rec.Recap()
    exit(1)


#simulation
#0767959699
#0662959698
num='0767959699'
st="phone_call("+num+")"
facts.append(st)
print("**Mr. A is calling.... ",num)
print("**Call assistant reply")
welcome()
print("**Mr. A")
txt=Agent_response("records\\rep_per.wav")
print("**Call assistant")
decision_reason(reason_choice_identify(txt))
print("**Mr. A")
#rep_fam
#rep_am
txt=Agent_response('records\\rep_fam.wav')
print("**Call assistant")
decision_staf(identity(txt,num))










