#import flask, import API keys from keys.json, import requests
from pkgutil import get_data

import requests
from flask import Flask, render_template, request
from keys import TICKETMASTER_KEY
from datetime import datetime

app = Flask(__name__)

# Pull events from Ticketmaster
def get_ticketmaster_events(startDT, endDT):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
        "apikey": TICKETMASTER_KEY,
        "city": "Kansas City",
        "countryCode": "US",
        "size": 50
    }

    if startDT:
        params["startDateTime"] = startDT

    if endDT:
        params["endDateTime"] = endDT

    response = requests.get(url, params=params)
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
                "url": event.get("url"),
                "lat": venue.get("location", {}).get("latitude"),
                "lon": venue.get("location", {}).get("longitude"),
                "city": venue.get("city", {}).get("name"),
                "class": event["classifications"][0]["segment"]["name"]
            })

    return events
    


def get_all_events(startDT=None, endDT=None):
    ticketmaster_data = get_ticketmaster_events(startDT, endDT)
    return normalize_ticketmaster(ticketmaster_data)

   