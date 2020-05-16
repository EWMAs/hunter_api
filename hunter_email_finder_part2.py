"""Script to find emails based on first name, last name and domain name using Hunter.io"""

import requests # To make get and post requests to APIs
import json # To deal with json responses from APIs
from pprint import pprint # To pretty print json info in a more readable format


# Global variables
hunter_api_key = "48208a1a898e1aa968ba499e6267a03c24980fea" # API key that tells Hunter who we are when we make a GET request

contact_info = {} # dictionary where we'll store each contact's information

people = [
    {
        "ID": 1, 
        "first_name": "Joyce", 
        "last_name": "Kettering", 
        "domain_name": "creativeandproductive.com"
        },
        {
            "ID": 2, 
            "first_name": "Quentin", 
            "last_name": "Durantay", 
            "domain_name": "dolead.com"
            }, 
            {
                "ID": 3, 
                "first_name": "Ziggy", 
                "last_name": "Stardust", 
                "domain_name": "mairie-paris.fr"
            }
            ]

# SECTION A — Ask Hunter to find emails based on first name, last name and domain name
def get_email_from_hunter(first_name, last_name, domain_name):

    url = "https://api.hunter.io/v2/email-finder" 

    parametres = {
        "domain": domain_name,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": hunter_api_key
    }

    response = requests.get(url, params=parametres)

    json_data = response.json()

    email_address = json_data["data"]["email"]
    confidence_score = json_data["data"]["score"]

    contact_info["first_name"] = first_name
    contact_info["last_name"] = last_name
    contact_info["domain_name"] = domain_name
    contact_info["email_address"] = email_address
    contact_info["confidence_score"] = confidence_score
    contact_info["twitter_handle"] = json_data["data"]["twitter"]

    print(contact_info)
    return contact_info


#get_email_from_hunter("Joyce", "Kettering", "creativeandproductive.com")

# TODO: SECTION B — Run get email function through a list of people hard-coded in script
def get_emails_from_list(people):
    for person in people: 
        first_name = person["first_name"]
        last_name = person["last_name"]
        domain_name = person["domain_name"]
        get_email_from_hunter(first_name, last_name, domain_name)

get_emails_from_list(people)


# TODO: SECTION C — Run get email function through a list of people in a Google Sheet and updated sheet with emails found
 







