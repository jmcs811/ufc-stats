import requests
from bs4 import BeautifulSoup
from models.UFCEvent import UFCEvent

def get_events():
    ALL_EVENTS_URL = "http://ufcstats.com/statistics/events/completed?page=all"

    ufc_events = []
    events_response = requests.get(ALL_EVENTS_URL)
    events_soup = BeautifulSoup(events_response.text, 'html.parser')
    events_table = events_soup.find_all('tr', class_='b-statistics__table-row')

    for event_row in events_table:
        event_location = ""
        event_name = ""
        event_date = ""
        event_id = ""

        event_names_td = event_row.find_all('td', class_="b-statistics__table-col")
        for event_rows in event_names_td:
            event_names_a = event_rows.find_all('i', class_='b-statistics__table-content')
            for event_names in event_names_a:
                events = event_names.find_all('a', class_= 'b-link b-link_style_black')
                for i in events:
                    if i.text != "":
                        event_name = str(i.text).strip()
                        event_id = i['href'].split('/')[-1]
                
                event_dates = event_names.find_all('span')
                for i in event_dates:
                    if i.text != "":
                        event_date = str(i.text).strip()

        # get event location
        event_locations = event_row.find_all('td', class_=['b-statistics__table-col b-statistics__table-col_style_big-top-padding'])
        for i in event_locations:
            if i.text != "":
                event_location = str(i.text).strip()
        
        ufc_events.append(UFCEvent(event_name, event_location, event_date))

        ufc_events = _clean_lists(ufc_events)

    return ufc_events

def _clean_lists(events):
    for i in events:
        if i.name == "" and i.date == "" and i.location == "":
            events.remove(i)
    return events
