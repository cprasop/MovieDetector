import datetime
import pymongo
from pymongo import MongoClient


#This script will run on a server, as a cronjob, running once a day to check if someone needs to be notified of a
#release date coming up

'''Connect to MovieDetector database'''
client = MongoClient()
db = client.users
twilio_token = '827119ae4c807c269e5f24b2c02cdd0e'

#calculating 10 days out from today
now = datetime.datetime.now()
goal = now + datetime.timedelta(days=10)
print(goal.date())

result = db.collection.find({"watchlist.release_date": goal.date()}, {"_id": 0, watchlist: 0})

#counting the number of people who have to notified
num = result.count("{")
for i in range(num):
    name_ind = result.index("\"name:\"")
    phone_ind = result.index("\"phone_number\"")
    name = result.substring(name_ind+10,phone_ind-3)
    phone = result.substring(phone_ind+18, phone_ind + 28)
    text(name, phone)
    result = result.substring(phone_ind + 28)

def text(name,phone):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC00192dda66594328c17c3ea44ff4153b'
    auth_token = twilio_token
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+18608524749',
        body="Hi " + name + "! You have a movie on your watchlist that will release in 10 days!",
        to='+1' + phone
    )
    print(message.sid)