# General description of the project
This project is an interactive Kansas City event discovery application designed to help residents, students, and tourists find things to do in one place. Rather than searching multiple websites, users can browse concerts, festivals, museums, restaurants, coffee shops, parks, and other local activities through a single platform. The goal is to simplify event discovery and make it easier for people to explore the Kansas City area based on their interests and location.

The application will collect data from the Ticketmaster Discovery API, Eventbrite. Information such as event names, dates, locations, and categories will be processed and combined into a searchable database. Users will be able to filter activities by date, time, or category while the system removes duplicate events and organizes information into a user-friendly format.

## Technical flow

The flow of data travels like this:

User
  ↓
Search & Filter Interface
  ↓
Flask Backend
  ↓
API Data Collection
(Ticketmaster)
  ↓
Data Processing & Cleaning
  ↓
Event Database / Data Storage
  ↓
Interactive Map + Event Results
  ↓
User

## Further investigation
Leaflet has many capabilities, and depending on the city one is pulling in the params function, there may be map overlays or other customizable abilities that one can program through the leaflet script. This version was made for Kansas City, where there is less leaflet data, but for larger cities such as New York City, one may have more capabilities to filter the map further by neighborhood or burrough, for example, choosing to have a filter for Manhattan, Brooklyn, etc. 

## User flow/UI 

<img width="595" height="377" alt="Home page UI" src="https://github.com/user-attachments/assets/4ae09ac8-752f-4022-bed7-ef8fa116aabd" />

The user begins by inputting their desired date range into the filter, and can additionally say what time they would like the event to start after. After inputting, they click search. 


<img width="597" height="408" alt="MapUI" src="https://github.com/user-attachments/assets/8cdda8ba-1681-46ad-80f6-4543a2d8dda6" />


The map will pull a variety of events forward. The user can then apply more filtering, adjust dates, change time, or filter by event category. 

<img width="592" height="242" alt="Map zoom UI" src="https://github.com/user-attachments/assets/d12ab3b8-68ff-482b-bbf9-3f49c5efcd53" />

If the user clicks a specific event card, it will zoom in on the map to that specific card. This gives the user a better idea to the location of the event. 

If the user clicks on the blue Buy Tickets hyperlink, this will take them to ticketmaster where they have the ability to buy tickets. 


