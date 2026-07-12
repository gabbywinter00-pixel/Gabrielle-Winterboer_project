#import flask, import API keys from keys.json, import requests
import requests
from flask import Flask, render_template, request
from keys import TICKETMASTER_KEY, EVENTBRITE_TOKEN
from datetime import datetime

app = Flask(__name__)

# Pull events from Ticketmaster
def get_ticketmaster_events(startDT, endDT):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
       "apikey": TICKETMASTER_KEY,
         "city": "Kansas City",
           "countryCode": "US",
           "size": 50,
           "startDateTime": startDT,
           "endDateTime": endDT
    } 
    
    response = requests.get(url, params=params)
    return response.json()

# Pull events from Eventbrite
def get_eventbrite_events():
    url = "https://www.eventbriteapi.com/v3/get"

    headers = {
        "Authorization": f"Bearer {EVENTBRITE_TOKEN}"
    }

    params = {
        "location.address": "Kansas City",
        "page_size": 50
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#normalize Ticketmaster data
def normalize_ticketmaster(data):
    events = []
    
    if "_embedded" in data:
        for event in data["_embedded"]["events"]:

            start = event.get("dates", {}).get("start", {})

            raw_time = start.get("localTime")
            time = raw_time[:5] if raw_time else None

            venue = {}

            if "_embedded" in event:
                venues = event["_embedded"].get("venues", [])
                if venues:
                    venue = venues[0]

            # GET CATEGORY
            classification = event.get("classifications", [])

            category = "Other"

            if classification:
                category = classification[0].get(
                    "segment", {}
                ).get(
                    "name",
                    "Other"
                )

            # NORMALIZE CATEGORY NAMES
            if category == "Arts & Theatre":
                category = "Theater"

            elif category not in [
                "Music",
                "Sports",
                "Theater",
                "Comedy"
            ]:
                category = "Other"
        

            events.append({
                "name": event.get("name"),
                "date": start.get("localDate"),
                "time": time,
                "source": "ticketmaster",
                "lat": venue.get("location", {}).get("latitude"),
                "lon": venue.get("location", {}).get("longitude"),
                "city": venue.get("city", {}).get("name"),
                "class": event["classifications"][0]["segment"]["name"]
            })

    return events
    
 #normalize Eventbrite data
def normalize_eventbrite(data):
    events = []

    for event in data.get("events", []):

        name = event.get("name", {}).get("text")
        start = event.get("start", {}).get("local")

        date = None
        time = None
        city = event.get("venue", {}).get("address", {}).get("city")

        if start:
            date = start[:10]
            time = start[11:16]

        events.append({
            "name": name,
            "date": date,
            "time": time,
            "source": "eventbrite",
            "lat": None,
            "lon": None,
            "city": city 
        })

    return events

def get_all_events(startDT, endDT):

    ticketmaster_data = get_ticketmaster_events(startDT, endDT)
    eventbrite_data = get_eventbrite_events()

    ticketmaster_events = normalize_ticketmaster(ticketmaster_data)
    eventbrite_events = normalize_eventbrite(eventbrite_data)
    return ticketmaster_events + eventbrite_events

   