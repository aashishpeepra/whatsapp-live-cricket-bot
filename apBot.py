#Do pip install twilio and requests
from twilio.rest import Client
import requests
import datetime
import time

# Your Account SID from twilio.com/console
account_sid = "YouSID"
# Your Auth Token from twilio.com/console
auth_token  = "YouAuthToken"

client = Client(account_sid, auth_token)
#using the API to get match details from recently happend and going to happen matches
resp=requests.get("https://cricapi.com/api/matches?apikey=YourAPIKEY");
data=resp.json()["matches"]

#Returns filtered matches on the basis of the team whose match you want
def return_all_match(teamName,data):
    """
    teamName: any cricket team name 
    data: the data that we get from the API call
    """
    allMatch=[]
    for each in data:
        if (teamName in each["team-1"]) or (teamName in each["team-2"]):
            allMatch.append(each)
    return allMatch

result=return_all_match("India",data) #storing list of matches in which either team was "India"

#Filters out the matches on the basis of current date
def filter_date(data):
    """
    data: a list of all the matches to filter by date
    """
    current_date=str(datetime.datetime.now())
    current_date=current_date[:current_date.index(' ')]
    results=[]
    for each in data:
        if current_date in each["date"]:
            results.append(each)
    return results

result2=filter_date(result) #Filtered the result list down to by only returning matches with todays date

#return detailed information about the match(single) that you pass
def return_score(id):
    """
    id: you pass the "unique_id" of the match who's info you want
    """
    id=str(id)
    response=requests.get("https://cricapi.com/api/cricketScore?apikey=YourAPIKEY&unique_id="+id)
    if response.status_code!=200:
        return 0
    else:
        return response.json()

#Returns detailed information about the matches through return_score() function
def return_detailed_info(matches):
    """
    matches: list of the matches
    """
    allPresent=[]
    for each in matches:
        allPresent.append(return_score(each["unique_id"]))
    return allPresent
    
print("-"*20)
print("Starting AP BOT")
allPresent=return_detailed_info(result2) #list of matches with detailed info of every match

#Converts JSON into a better readable and good looking format
def readable(data):
    """
    data: Single JSON value from the API
    """
    text=""
    keys=["stat","score","team-1","team-2","v","ttl","matchStarted","dateTimeGMT","type"]
    for elements in keys:
        if elements in data.keys():
            text+="*"+elements+"* "+str(data[elements])+"\n"
    return text


if __name__=="__main__": 
    #The message sending part
    counter=0  #Just to bound check
    #allPresent sotres the final list of matches 
    for each in allPresent:
        to_send=readable(each) 
        message = client.messages.create(
            to="whatsapp:+910000000000", #replace zeros with sender's number
            from_="whatsapp:+1000000000", #Replace zeros with twilio's number
            body=to_send)
        time.sleep(2)
        print(message.sid)
        if counter>15:
            #Security check loop , so in case somehow anything make list big enough it don't kill their server
            break
    print("Process Finished","\nTotal messages send = ",counter)
