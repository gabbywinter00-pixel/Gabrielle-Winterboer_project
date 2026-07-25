#import flask, import API keys from keys.json, import requests
from pkgutil import get_data

import requests
import pandas as pd
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
        "size": 100,
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
                category = "Arts & Theatre"
            # Convert explicit 'Undefined' values to Other
            elif category == "Undefined":
                category = "Other"

            elif category not in [
                "Music",
                "Sports",
                "Arts & Theatre",
                "Comedy",
                "Other"
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
                # store the normalized category so templates and filters align
                "class": category
            })

    return events
    

def get_all_events(startDT=None, endDT=None):
    ticketmaster_data = get_ticketmaster_events(startDT, endDT)
    events = normalize_ticketmaster(ticketmaster_data)

    df = pd.DataFrame(events)

    if not df.empty:
        # Convert to datetime, then format as MM/DD/YYYY
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%m/%d/%Y")
        
        # Convert to time, then format as HH:MM AM/PM
        df["time"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce").dt.strftime("%I:%M %p")
    
    

    return df
   