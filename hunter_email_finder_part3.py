"""Script to find emails based on first name, last name and domain name using Hunter.io"""

import requests # To make get and post requests to APIs
import json # To deal with json responses from APIs
from pprint import pprint # To pretty print json info in a more readable format
import gspread # Library to interact with Google Spreadsheets
from oauth2client.service_account import ServiceAccountCredentials # To access Google Account

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

# SECTION B — Run get email function through a list of people hard-coded in script
def get_emails_from_list(people):
    for person in people: 
        first_name = person["first_name"]
        last_name = person["last_name"]
        domain_name = person["domain_name"]
        get_email_from_hunter(first_name, last_name, domain_name)

#get_emails_from_list(people)


# TODO: SECTION C — Run get email function through a list of people in a Google Sheet and updated sheet with emails found
## Set up worksheet where I'll want to get and push my data
workbook_url = "https://docs.google.com/spreadsheets/d/1EY6xvufNfQ3_OPQA6yCWUjcl4dx4ydkdkJ1Of5BlCI8/edit?usp=sharing"

## Authenticate myself to Google 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"] # I want to access Google Sheets and Google Drive (this is my scope)
json_file = "enrich-contact-list-d77bde75bc8c.json" # I have a JSON file in my project folder to prove my credentials 
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope) # I tell Google "These are my credentials and the scope I want to access"
gc = gspread.authorize(credentials) # I ask for authorization to access my Google account

## Get data from worksheet
def get_data_from_workbook():
    workbook = gc.open_by_url(workbook_url) # Define workbook we're going to work with
    get_data_sheet = workbook.get_worksheet(0) # Define first sheet in workbook where we're going to fetch the list of people we want to lookup
    contacts = get_data_sheet.get_all_records() # Define where liste of people is
    print(contacts)
    return contacts

## Post results to worksheet
def push_data_to_workbook(contact_info):
    workbook = gc.open_by_url(workbook_url)
    push_data_sheet = workbook.get_worksheet(1) # Define second sheet in workbook where we're going to push the results of our API request
    index = 1 # start on line 2 (index 0 corresponds to line 1 with the titles of our columns)
    contacts = get_data_from_workbook()

    for contact in contacts:
        first_name = contact["first_name"]
        last_name = contact["last_name"]
        domain_name = contact["domain_name"]

        contact_info = get_email_from_hunter(first_name, last_name, domain_name)

        email_address = contact_info["email_address"]
        confidence_score = contact_info["confidence_score"]

        row = [first_name, last_name, domain_name, email_address, confidence_score] # Define in which columns values go
        index += 1 # Add a line every time you go through the loop
        push_data_sheet.insert_row(row,index) # Add row to index line


get_data_from_workbook()
push_data_to_workbook(contact_info)


