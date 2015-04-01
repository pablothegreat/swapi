# SPICEWORKS API ACCESS
# mike.stiers@gmail.com
# 03.31.2015

import urllib
import urllib2
import cookielib
import json

# enter your login informaiton and the Spiceworks URL
user_email = "your login email address"
user_password = "your password"
spiceworks_url = "http://your.spiceworks.url"
pickaxe = "\\" # not sure why this is required for the form

# create a cookie jar and install the handler for urllib2
cookiejar = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
# set the agent to Firefox to avoid incompatible browser detection
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

# browse to the page and store a cookie
request = urllib2.Request(spiceworks_url, None)
f = urllib2.urlopen(request)
html = f.read()

# find the authenticity token that is needed to submit the login form
token = html.split("<")
for tokens in token:
	if "token" in tokens:
		token2 = tokens.split('"')
		authenticity_token = token2[5]
		print "authenticity_token: ", authenticity_token
f.close()

# encode the data that is to be posted from the form and then submit the form
data = urllib.urlencode({"authenticity_token" : authenticity_token, "user[email]" : user_email, "user[password]" : user_password, "_pickaxe" : pickaxe})
request = urllib2.Request(spiceworks_url + "/login", data)
f = urllib2.urlopen(request)
f.close()

# you should now be logged in and able to access the API

# here is an example of getting the JSON for a ticket #1 and then printing some key fields
request = urllib2.Request(spiceworks_url + "/api/tickets/1.json", None)
f = urllib2.urlopen(request)
html = f.read()
f.close()
#print html

json_data = json.loads(html)
print "Creator: ", json_data['creator']['email']
print "Assigned to: ", json_data['assigned_to']
description = json_data['description'].replace("\r\n","")
print description
