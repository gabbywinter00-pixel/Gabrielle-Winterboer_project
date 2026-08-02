# User's Guide
The main task of the application would be to simplify event discovery by combining information from multiple sources into one searchable and visual platform. Users would interact with the application by selecting interests, searching for activities, filtering by date or price, and exploring events through an interactive map.

This project requires Python 13.3. It was originally created using Visual Studio Code. 

## Before editing: 
- Get an API Key for ticketmaster (https://developer-acct.ticketmaster.com/user/login). 
- Create a keys.py file and add the following: 
- [ ] #keys.py
- [ ] #Ticketmaster API
- [ ] TICKETMASTER_KEY = "PASTE KEY HERE"
- Put the keys.py file in your gitignore

## Necessary imports:
Make sure that you are importing 
- Requests
- Pandas
- Datetime
- Flask
- API Key

<img width="599" height="188" alt="Imports" src="https://github.com/user-attachments/assets/2fad6d85-7336-47e7-830e-f05513c785b8" />


## Data filtering: 
All data filtering is done in data.py.
This includes: 
- Pulling events from ticketmaster
- Normalizing events
- Converting the datatime to standard format 

The app.py then pulls the data from the get all events function 

## App output
App.py allows you to: 
- Control filtering of events pulled from data.py
- It also contains HTML that controls display of first home page, the filters the user utilizes before seeing results of the API pull 

## Display: 
Index.html, found in templates, is what controls the interface and look of the app. 
This controls: 
- Leaflet map script
- Leaflet map markers
- The two column design
- Filter displays 
- Buttons that outbound to ticketmaster
- Fonts and colors

## Customizing for other cities: 
If you want the app to pull a place other than Kansas city, you simply adjust the params function at the top of data.py. Ticketmaster events formats in a way that you can filter by city, so simply putting "Detroit" or “Minneapolis” is sufficient for the API. The code should flow accordingly. 
However, you will have to adjust the H1 titles in the HTML to reflect the city of your choosing, rather than “KC events”

<img width="597" height="279" alt="Params" src="https://github.com/user-attachments/assets/a1535264-07a0-44f3-8d66-1f38a46abede" />

There are h1 in app.py and index.html

<img width="598" height="528" alt="KC h1" src="https://github.com/user-attachments/assets/3bd85772-1341-407f-b208-f2860a971ce8" />

## Amount of events pulled
Size refers to the amount of events pulled. Through testing 100 is recommended as Ticketmaster allows only a limited number of events pulled at a single time from a single API. 


