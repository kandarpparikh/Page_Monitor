import json
import os
import smtplib
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date , timedelta , datetime

#call api
#check under 18
#send mail


def CallApi(headers,pincodes,tomorrow,mycount,thismail):
    class AppURLopener(urllib.request.FancyURLopener):
        version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'
    opener = AppURLopener()


    for mypincode in pincodes:
        print(mypincode)
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={0}&date={1}'.format(
                str(mypincode), tomorrow)
        #print(url)
        response = requests.get(url ,headers = headers)
        if(response.status_code==200):
            data = response.json()
            print(data)
            getData(data,thismail)
        else:
            print("API call not successfull")
            response = opener.open('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={0}&date={1}'.format(
                str(mypincode), present)).read()
            url_output = json.dumps(response[2:-1])
            url_output = eval(url_output)
            print("Session Available [GET TIME]")
            print(url_output)
            getData(url_output,thismail)
        print("Pause & avoid [403] , 3 secs")
        time.sleep(3)


def getData(api_data,thismail):
    for i in api_data['sessions']:
        #print(bool(i['min_age_limit'] == 45))
        if (i['min_age_limit'] == 18) and (i['center_id'] not in Center_set) and (i["available_capacity"] > 0):
            now=time.localtime()
            current_time = time.strftime("%H:%M:%S",now)
            Center_set.add(i['center_id'])
            text_file = open("sessions.json", "a")
            text_file.write("Slot opened at : "+current_time+"\n")
            text_file.write("Center Name :" +str(i['name'])+"\n")
            text_file.write("Pincode :" +str(i['pincode'])+"\n")
            text_file.write("Name of Vaccine : "+str(i['vaccine']) +"\n")
            text_file.write("Vaccines Available for DOSE 1:" +str(i['available_capacity_dose1'])+"\n")
            text_file.write("Vaccines Available for DOSE 2:" +str(i['available_capacity_dose2'])+"\n")
            text_file.write("Book your slot at https://selfregistration.cowin.gov.in/"+"\n"+"\n")
            text_file.close()
            print("\n Pincode : ",i['pincode'])
            print(" Name : ",i['name'])
            print("\n Vaccines available : ",i['available_capacity'])
    sendmail(thismail)



    #stats(count)

def sendmail(recievermail):
    text_file = open("sessions.json", "rt")
    data = text_file.read()
    words = data.split()
    print("word length",len(words))
    if(len(words)>0):
        print("--Initiate Email Session--")

        sender_email = "bludhound221@gmail.com"
        receiver_email=[]
        receiver_email.append(str(recievermail))
        receiver_email.append("15it065@charusat.edu.in")
        if (str(recievermail) == "nihar_parikh@hotmail.com"):
            receiver_email.append("itsap159@gmail.com")
            receiver_email.append("sompura_nishit@rediff.com")
        print("Reciever mail : ",receiver_email[0])
        print("Reciever mail : ",receiver_email[1])
        password = "Lazarus@123"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Vaccine Availability Notification"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_email)

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
        receiver_email.clear()

    f = open('sessions.json', 'r+')
    f.truncate(0)
    f.close()


def stats():
    print(Center_set)



if __name__ == '__main__':
    #PINCODES
    pin_array_nihar=[380013,380015]
    pin_array_kp=[383325]
    pin_array_paulmi=[383350]
    pin_array_govind=[382443,380008]
    pin_array_fenil=[380007]
    email_govind = "govindmanghnani3@gmail.com"
    email_nihar = "nihar_parikh@hotmail.com"
    email_pranav = "pam24365@yahoo.com"
    email_kp = "15it065@charusat.edu.in"
    email_paulmi = "paulamiparikh1973@gmail.com"
    email_fenil="fenilshah312@gmail.com"
    pin_array_pranav=[390025,390019]
    #in_array=[382350,380022]


    Center_set = set()
    count =0
    #TIME
    start_time = time.time()
    today=date.today()
    present = today.strftime("%d-%m-20%y")
    tomorrow = today + timedelta(1)
    tomorrow = tomorrow.strftime("%d-%m-20%y")

    #HEADERS
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'}
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'}
    while True:
        count = count +1
        CallApi(headers,pin_array_nihar,tomorrow,count,email_nihar)
        #sendmail(email_nihar)
        stats()
        #CallApi(headers,pin_array_pranav,tomorrow,count,email_pranav)
        #sendmail(email_pranav)
        #stats()
        #CallApi(headers,pin_array_fenil,tomorrow,count,email_fenil)
        #stats()
        CallApi(headers,pin_array_govind,tomorrow,count,email_govind)
        stats()

        endtime=time.time()
        print("Runtime : ",endtime-start_time)
        '''
        CallApi(headers,pin_array_paulmi,tomorrow,count,email_paulmi)
        #sendmail(email_paulmi)
        stats()

        CallApi(headers,pin_array_kp,tomorrow,count,email_kp)
        #sendmail(email_kp)
        stats()
        endtime=time.time()
        print("Runtime : ",endtime-start_time)
'''
