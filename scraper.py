from bs4 import BeautifulSoup
import time
import datetime
import urllib.request
import curses

from mailjet_rest import Client
import tokens


def check_availability():
    target_page = 'https://studybox.studentenrabatt.com/products/study-box'
    target_phrase = 'Ausverkauft'
    page = urllib.request.urlopen(target_page)
    soup = BeautifulSoup(page, features="html.parser")

    if target_phrase in soup.text:
        return False
    return True

def main(avb):
    available = check_availability()

    if avb and available:
        return True

    elif(available):
        #send mail
        api_key=tokens.ApiKey
        api_secret=tokens.SecretKey
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")
        recipiants=[["lexi.haeberle@gmail.com","lexi"],["wolkenstein.f@gmail.com","Wolki"]]
        for i in range(len(recipiants)):
            data = {
                'Messages': [
                                {
                                        "From": {
                                                "Email": "studybox.checker@gmail.com",
                                                "Name": "Studybox checker"
                                        },
                                        "To": [
                                                {
                                                    "Email": recipiants[i][0],
                                                    "Name": recipiants[i][1]
                                                }
                                        ],
                                        "Subject": "Studybox available NOW!",
                                        "TextPart": "Get yours on https://studybox.studentenrabatt.com/products/study-box!",
                                        
                                }
                        ]
                }
            mailjet.send.create(data=data)
        return True
    
    elif(avb):
        return False
    else:
        return False

def program(stdscr):
    availability = True
    y,x=curses.window.getmaxyx(stdscr)
    y-=2
    stdscr.clear()
    screen.addstr(5,7,"┌─────────────────────────┐")
    screen.addstr(6,7,"│ StudyboxScraper by Lexi │")
    screen.addstr(7,7,"└─────────────────────────┘")
    screen.addstr(0,0,"┌"+(x-2)*"─"+"┐")
    screen.addstr(y,0,"└"+(x-2)*"─"+"┘")
    while True:
        now = datetime.datetime.now()
        availability = main(availability)

        for i in range(y-1):
            screen.addstr(i+1,0,"│")
            screen.addstr(i+1,x-1,"│")

        if(availability):
            screen.addstr(10,7,"┌──────────┬────────────────────────┐")
            screen.addstr(11,7,"| "+now.strftime("%H:%M:%S ")+"│   Studybox available!   │")
            screen.addstr(12,7,"└──────────┴────────────────────────┘")
        else:
            screen.addstr(10,7,"┌──────────┬────────────────────────┐")
            screen.addstr(11,7,"| "+now.strftime("%H:%M:%S ")+"│ Studybox not available │")
            screen.addstr(12,7,"└──────────┴────────────────────────┘")
        screen.refresh()
        time.sleep(29)

screen = curses.initscr()

curses.wrapper(program)