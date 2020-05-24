"""Script to find emails based on first name, last name and domain name using Hunter.io"""

import requests # To make get and post requests to APIs
import json # To deal with json responses from APIs
from pprint import pprint # To pretty print json info in a more readable format
import gspread # Library to interact with Google Spreadsheets
from oauth2client.service_account import ServiceAccountCredentials # To access Google Account

# Global variables
hunter_api_key = "thiswillbeastringyoucreateinyourhunteraccount" # API key that tells Hunter who we are when we make a GET request

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

    # If nothing found, return an empty dictionary
    if response.status_code != 200: # If invalid response, return an empty list
        contact_info["email_address"] = "unknown"
        contact_info["confidence_score"] = "N/A"
        return contact_info


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

# SECTION B — Run get email function through a list of people hard-coded in script
def get_emails_from_list(people):
    for person in people: 
        first_name = person["first_name"]
        last_name = person["last_name"]
        domain_name = person["domain_name"]
        get_email_from_hunter(first_name, last_name, domain_name)

#get_emails_from_list(people)


# SECTION C — Run get email function through a list of people in a Google Sheet and updated sheet with emails found
## Set up worksheet where I'll want to get and push my data
workbook_url = "urlyougetwhenyoushareyourgooglesheet"

## Authenticate myself to Google 
json_file = "jsonfilename.json"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
gc = gspread.authorize(credentials)


## Get data from worksheet
def get_data_from_workbook():
    workbook = gc.open_by_url(workbook_url)
    get_data_sheet = workbook.get_worksheet(0)
    contacts = get_data_sheet.get_all_records()
    #print(contacts)
    return contacts

## Post results to worksheet
def push_data_to_workbook():
    workbook = gc.open_by_url(workbook_url)
    push_data_sheet = workbook.get_worksheet(1)
    index = 1
    contacts = get_data_from_workbook()

    for contact in contacts:
        first_name = contact["first_name"]
        last_name = contact["last_name"]
        domain_name = contact["domain_name"]

        contact_info = get_email_from_hunter(first_name, last_name, domain_name)

        email_address = contact_info["email_address"]
        confidence_score = contact_info["confidence_score"]

        row = [first_name, last_name, domain_name, email_address, confidence_score]
        index += 1 
        push_data_sheet.insert_row(row, index)


## Call Functions
get_data_from_workbook()
push_data_to_workbook()