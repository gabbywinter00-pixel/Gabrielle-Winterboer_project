import requests
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request
from keys import TICKETMASTER_KEY, EVENTBRITE_TOKEN

app = Flask(__name__)

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
   
              <label>From:</label>
                <input 
                type="date" 
                name="start_date" 
                value="{{ start_date }}"
                >

                <label>To:</label>
                <input 
                type="date" 
                name="end_date" 
                value="{{ end_date }}"
                >

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

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    selected_time = request.args.get("time")
    selected_category = request.args.get("category")

    # Create date range for Ticketmaster
    startDT = f"{start_date}T00:00:00Z" if start_date else None
    endDT = f"{end_date}T23:59:59Z" if end_date else None
    
    df = get_all_events(startDT, endDT)

    # TIME FILTER
    if selected_time and not df.empty:
        selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()
        df = df.loc[df["time"].notna() & (df["time"] >= selected_time_obj)]

    # CATEGORY FILTER
    if selected_category and not df.empty:
        df = df.loc[df["class"] == selected_category]

    print("EVENT COUNT:", len(df))
    
    return render_template(
        "index.html",
        events=df,
        start_date=start_date,
        end_date=end_date,
        selected_time=selected_time,
        selected_category=selected_category
    )

#run Flask app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True, use_reloader=False)