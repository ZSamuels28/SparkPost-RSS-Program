"""
GUI tool which pulls RSS data, passes into SparkPost as substitution data, and sends an email to a specific recipient list
Also allows for editing template and adding objects
"""
import os
from sparkpost import SparkPost
from dotenv import load_dotenv
from pathlib import Path
import PySimpleGUI as sg
import ssl
import scripts.build_window as build_window
import scripts.events as events
import scripts.getids as getids

# Loads the SparkPost API Key and Host from the varaibles.env file
dotenv_path = Path("./config/variables.env")
load_dotenv(dotenv_path=dotenv_path)
SPARKPOST_API_KEY = os.getenv("SPARKPOST_API_KEY")
SPARKPOST_HOST = os.getenv("SPARKPOST_HOST")

sp = SparkPost(SPARKPOST_API_KEY)  # Initialize SparkPost

ssl._create_default_https_context = ssl._create_unverified_context
rss_elements = (
    []
)  # Required to store the RSS elements so they do not get overwritten on window events


template_ids, recipient_ids = (
    getids.get_template_ids(SPARKPOST_HOST, SPARKPOST_API_KEY),
    getids.get_recipient_ids(SPARKPOST_HOST, SPARKPOST_API_KEY),
)
window = build_window.build_window(template_ids, recipient_ids)

while True:

    center_of_window = build_window.center_of_window(window)
    # Read in the window events and values of the objects
    event, values = window.read()
    # window.bring_to_front()
    match event:
        case "template-id":
            events.template_id(window, values, sp)
        case "filter":
            events.filter(window, values, rss_elements)
        case "rss-elements":
            events.rss_elements(window, values)
        case "Update Template":
            events.update_template(
                values, center_of_window, sp, SPARKPOST_HOST, SPARKPOST_API_KEY
            )
        case "Read RSS":
            events.read_rss(window, center_of_window, values, rss_elements)
        case "Send":
            events.send(values, window, center_of_window, sp)
        case sg.WIN_CLOSED:
            break
        case "Close":
            break

build_window.close()
