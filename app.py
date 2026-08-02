import requests
import pandas as pd #the data relies on pandas, make sure to install it
from datetime import datetime #import datetime to normalize the time for date filtering
from flask import Flask, render_template, request
from keys import TICKETMASTER_KEY #create a key.py file with your ticketmaster API key in it, so you can import it here. 

app = Flask(__name__)

from data import get_all_events #this imports the get_all_events function from data.py, which is used to retrieve and normalize event data from Ticketmaster.


@app.route("/")
def home():
 #Below runs the HTML for the home page, and includes the first form for user input
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
    # Get query parameters from the request
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    selected_time = request.args.get("time")
    selected_category = request.args.get("category")

    # Create date range for Ticketmaster (keeps existing API call behavior)
    startDT = f"{start_date}T00:00:00Z" if start_date else None
    endDT = f"{end_date}T23:59:59Z" if end_date else None
    
    # MASTER: original dataset (preserved)
    master_df = get_all_events(startDT, endDT)
    master_df = master_df.copy(deep=True)

    # Ensure we have dedicated datetime/time columns for filtering (keeps formatted display columns untouched)
    if not master_df.empty:
        master_df["date_dt"] = pd.to_datetime(master_df["date"], format="%m/%d/%Y", errors="coerce")
        master_df["time_dt"] = pd.to_datetime(master_df["time"], format="%I:%M %p", errors="coerce").dt.time

    # WORKING COPY: apply all UI filters to this copy only
    df = master_df.copy()

    # Apply date-range filters (based on the date inputs from the form: YYYY-MM-DD)
    if start_date and not df.empty:
        start_dt = pd.to_datetime(start_date, format="%Y-%m-%d", errors="coerce")
        if pd.notna(start_dt):
            df = df.loc[df["date_dt"].notna() & (df["date_dt"].dt.date >= start_dt.date())]

    if end_date and not df.empty:
        end_dt = pd.to_datetime(end_date, format="%Y-%m-%d", errors="coerce")
        if pd.notna(end_dt):
            df = df.loc[df["date_dt"].notna() & (df["date_dt"].dt.date <= end_dt.date())]

    # TIME FILTER (compare against time_dt which is a time object)
    if selected_time and not df.empty:
        selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()
        df = df.loc[df["time_dt"].notna() & (df["time_dt"] >= selected_time_obj)]

    # CATEGORY FILTER
    # detect category-like column and normalize to 'class' for template compatibility
    possible_cols = ["class", "classification", "category", "segment", "type"]
    cat_col = next((c for c in possible_cols if c in df.columns), None)
    if cat_col and cat_col != "class":
        # rename in both master and working copies so templates can keep using row['class']
        master_df = master_df.rename(columns={cat_col: "class"})
        df = df.rename(columns={cat_col: "class"})
    if selected_category and not df.empty and "class" in df.columns:
        df = df.loc[df["class"] == selected_category]

    if not df.empty and "date_dt" in df.columns:
        sort_columns = ["date_dt"]
        if "time_dt" in df.columns:
            sort_columns.append("time_dt")
        df = df.sort_values(by=sort_columns, ascending=True)

    print("MASTER COUNT:", len(master_df), "FILTERED COUNT:", len(df)) #test print to see how many events are in the master dataset vs. the filtered dataset

    # Render the results template with the filtered DataFrame and the original query parameters
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