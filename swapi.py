# SPICEWORKS API ACCESS
# fern@fern-net.net
# 12.08.25

import urllib
import http.cookiejar
import json

# enter your login informaiton and the Spiceworks URL
user_email = "your login email address"
user_password = "your password"
spiceworks_url = "http://your.spiceworks.url"
pickaxe = "\\" # not sure why this is required for the form

# create a cookie jar and install the handler for urllib
cookiejar = http.cookiejar.LWPCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
# set the agent to Firefox to avoid incompatible browser detection
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# browse to the page and store a cookie
f = urllib.request.urlopen(spiceworks_url, None)
html = f.read()

# find the authenticity token that is needed to submit the login form

token = str(html).split("<")

for tokens in token:
    if "token" in tokens:
        token2 = tokens.split('"')
        authenticity_token = token2[3]
f.close()

# encode the data that is to be posted from the form and then submit the form
data = bytes(urllib.parse.urlencode({"authenticity_token" : authenticity_token, "email" : user_email, "password" : user_password, "_pickaxe" : pickaxe}), encoding='utf8')
request = urllib.request.Request("https://accounts.spiceworks.com/sign_in/", data)
f = urllib.request.urlopen(request)
f.close()

#should now be logged in and able to access the API

#visits ticket.json and pulls page contents into var "html""
request = urllib.request.Request(spiceworks_url + "/api/tickets.json", None)
f = urllib.request.urlopen(request)
html = f.read()
f.close()

#set list and dictionary up for loops ahead
ticketList=[] #stores a ticket in each entry, with nested lists
userDict={} #relationship between user IDs and their names and emails

json_data = json.loads(html)

for users in json_data['end_users']: #iterates through 'end_users' heading within json
    email = users['email']
    name = users['name']
    userDict.update({ users['id'] : [name,email] }) #adds ID as key value, with a 2 size list for name and email


for tickets in json_data['tickets']: #iterates through 'tickets' heading within json
    ticketList.append([tickets['id'],tickets['summary'],tickets['status'],userDict.get(tickets['creator']['id'],['null','null'])[0],userDict.get(tickets['creator']['id'],['null','null'])[1]]) #adds ticket information to 'ticketList[]'
    print (ticketList[len(ticketList)-1])
