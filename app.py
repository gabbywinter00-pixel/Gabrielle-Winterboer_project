#import flask, import API keys from keys.json, import requests
import requests
from flask import Flask, render_template, request
from keys import TICKETMASTER_KEY, EVENTBRITE_TOKEN

app = Flask(__name__)

from asyncio import events

from data import get_all_events

@app.route("/")
def home():

    html = """
    <html>

<head>

    <title>KC Events</title>
    <style> 

        body {
            font-family: Impact, sans-serif;
            background-color: #d2f8ff;
            margin: 0;
            padding: 0;

            display: flex;
            justify-content: center;
            align-items: center;

            height: 100vh;
        }

        .container {

            background-color: white;

            padding: 40px;

            border-radius: 12px;

            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);

            text-align: center;
        }

        h1 {
            color: #333333;
            margin-bottom: 25px;
        }

        input[type="text"] {

            width: 300px;

            padding: 12px;

            border-radius: 8px;

            border: 1px solid #cccccc;

            font-size: 16px;
        }

        input[type="submit"] {

            padding: 12px 20px;

            background-color: #c81e8e;

            color: white;

            border: none;

            border-radius: 8px;

            font-size: 16px;

            cursor: pointer;

            margin-left: 10px;
        }

        input[type="submit"]:hover {

            background-color: #890c5e;
        }
        body {
            overflow: hidden;
        }

        

    </style>

</head>

<body>
 

    <div class="container">

        <h1>KC Event Search</h1>

        <form action="/results/" method="GET">
   
             <label>Date:</label>
                <input type="date" name="date" value="{{ selected_date }}">

             <label>Starts after:</label>
             <input type="time" name="time" value="{{ selected_time }}">

            <input type="submit" value="Search">

        </form>

    </div>

</body>

</html>
"""

    return html


@app.route("/results/")
def results():

    print("ROUTE HIT")

    selected_date = request.args.get("date")
    selected_time = request.args.get("time")
    selected_category = request.args.get("category")

    data = get_all_events() # NEED STARTDT AND ENDDT PARAMETERS

    # Apply remaining filters
    filtered = data

    from datetime import datetime

    filtered = data

    # TIME FILTER
    if selected_time:
        try:
            selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()

            filtered = [
                e for e in filtered
                if e.get("time")
                and datetime.strptime(e["time"], "%H:%M").time() >= selected_time_obj
            ]

        except:
            filtered = filtered


    # DATE FILTER
    if selected_date:
        try:
            filtered = [
                e for e in filtered
                if e.get("date") == selected_date
            ]
        except:
            filtered = filtered

    # Build final display list
    events = []

    for event in filtered:

        display_time = "TBD"

        if event.get("time"):
            try:
                display_time = datetime.strptime(
                    event["time"],
                    "%H:%M"
                ).strftime("%I:%M %p")
            except:
                display_time = event["time"]

        if selected_category:
            filtered = [
                e for e in filtered
                if e.get("category") == selected_category]

        events.append({
            "name": event.get("name"),
            "date": event.get("date"),
            "time": display_time,
            "source": event.get("source"),
            "lat": event.get("lat"),
            "lon": event.get("lon"),
            "classification": event.get("class"),
        })

    print("EVENT COUNT:", len(events))
    
    return render_template(
        "index.html",
        events=events,
        selected_date=selected_date,
        selected_time=selected_time
    )

#run Flask app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True, use_reloader=False)
