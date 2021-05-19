import json
import os
import io
import smtplib
import requests
import subprocess
import urllib.request
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date , timedelta , datetime
from collections import Counter
from os import path

#https://vfs-cic.mioot.com/forms/appointments/
#check if wordcount = 0
# if 0 , then  add len of string to txt file
# else compare len
# if len same do nothing
# if diff -> send mail and update file with new len

def HitPage(headers,link,emails):
        response = requests.get(link ,headers = headers)
        if(response.status_code==200):
            print(response.text)
            x = str(response.text)
            if(path.exists("Contents.txt")==False):
                with io.open("Contents.txt", "w+", encoding="utf-8") as f:
                    f.close()
            with io.open("Contents.txt", "r+", encoding="utf-8") as f:
                if(len(f.readlines())==0):
                    print("New file")
                    f.writelines(str(len(x)))
                    f.close()
                else:
                    with io.open("Contents.txt", "r+", encoding="utf-8") as f:
                        length = f.readlines()
                        print(length[0])
                        if(str(len(x))!=str(length[0])):
                            print("Doesnt equal")
                            f.close()
                            sendmail(emails)
                            open("Contents.txt","w").close()
                            with io.open("Contents.txt", "r+", encoding="utf-8") as f:
                                f.writelines(str(len(x)))
                                f.close()
                        else:
                            print("Same")

def sendmail(emails,data="VFS Global Site has some updates \n Inform Kandarp about this by calling him on 9712586540 \n website link :  https://vfs-cic.mioot.com/forms/appointments/"):
    sender_email = "bludhound221@gmail.com"
    receiver_email= emails
    password = "<Password>"
    message = MIMEMultipart("alternative")
    message["Subject"] = "VFS Global Site Update"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    #data = "VFS Global Site has some updates \n Inform Kandarp about this by calling him on 9712586540 \n website link :  https://vfs-cic.mioot.com/forms/appointments/"

    # Create the plain-text and HTML version of your message
    #mymessage = "Center Name : "+str(i['name']) + "\n" + "Pincode : "+str(i['pincode']) + "\n" +"Vaccines Available : "+ \
                    #str(i['available_capacity']) + "\n"
    part1 = MIMEText(data, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

#                f.close()
                #data = f.read()
                #words = data.split()
                #wordcount = Counter(f.read().split())
                #print("Length of file : ",wordcount.__sizeof__())
'''
                num_words = 0
                f.close()
                with open("Contents.txt", 'r') as f:
                    for line in f:
                        words = line.split()
                        num_words += len(words)
                #open('Contents.txt', 'w').close()
                print("Number of words:")
                print(num_words)
                print("len of string : ",len(x))
                with open("Contents.txt", 'r') as f:
                    print(f.readline())

        else:
            print("Response status not 200")
'''
def Isrunning():
    now = datetime.now()
    x = int(now.strftime("%H%M%S"))
    arr=["15it065@charusat.edu.in"]
    if((x>=90000 and x<90100) or (x>=120000 and x<120100) or (x>=150000 and x<150100) or (x>=180000 and x<180100) or
            (x>=210000 and x<210100) or (x>=000000 and x<100) or (x>=21300 and x<21500)):
        sendmail(arr,data="Script is running")



if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'}
    link = "https://vfs-cic.mioot.com/forms/appointments/"
    emails=[]
    HitPage(headers,link,emails)
    Isrunning()

