"""Script to find emails based on first name, last name and domain name using Hunter.io"""

import requests # To make get and post requests to APIs
import json # To deal with json responses from APIs
from pprint import pprint # To pretty print json info in a more readable format


# Global variables
hunter_api_key = "48208a1a898e1aa968ba499e6267a03c24980fea" # API key that tells Hunter who we are when we make a GET request
contacts = [] # list where we'll store our contacts
contact_info = {} # dictionary where we'll store each contact's information

# TODO: SECTION A — Ask Hunter to find emails based on first name, last name and domain name
def get_email_from_hunter(first_name, last_name, domain_name):

    url = "https://api.hunter.io/v2/email-finder" #defining the URL we need to make the GET request

    # defining the parameters we're passing to the GET request
    params = {
        "domain": domain_name,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": hunter_api_key
    }

    response = requests.get(url, params=params) # stocking response of GET request in a variable

    if response.status_code != 200: # If the API's response is other than 200, I want to return an empty list and quit the function
        return []

    json_data = response.json() # making the API's response readable in a JSON (documentation told us output was a JSON)

    # extracting the email address and confidence score from the JSON
    email_address = json_data["data"]["email"]
    confidence_score = json_data["data"]["score"]

    # storing a contact's data into contact_info dictionary
    contact_info["first_name"] = first_name 
    contact_info["last_name"] = last_name
    contact_info["domain"] = domain_name
    contact_info["email_address"] = email_address
    contact_info["confidence_score"] = confidence_score

    print(contact_info)
    return contact_info # everytime the function is called with new arguments, it returns a new contact_info dictionary

get_email_from_hunter("Joyce", "Kettering", "creativeandproductive.com")

# TODO: SECTION B — Run get email function through a list of people hard-coded in script



# TODO: SECTION C — Run get email function through a list of people in a Google Sheet and updated sheet with emails found
 







