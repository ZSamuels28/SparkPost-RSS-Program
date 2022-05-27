"""
GUI tool which pulls RSS data, passes into SparkPost as substitution data, and sends an email to a specific recipient list
Also allows for editing template and adding objects
"""
import os
from sparkpost import SparkPost
from dotenv import load_dotenv
from pathlib import Path
import PySimpleGUI as sg
import requests
import feedparser
import ssl

# Loads the SparkPost API Key and Host from the varaibles.env file
dotenv_path = Path("./variables.env")
load_dotenv(dotenv_path=dotenv_path)
SPARKPOST_API_KEY = os.getenv("SPARKPOST_API_KEY")
SPARKPOST_HOST = os.getenv("SPARKPOST_HOST")

ssl._create_default_https_context = ssl._create_unverified_context

# Pulls a list of template IDs into the variable template_ids
headers = {"Authorization": SPARKPOST_API_KEY}
params = {"drafts": "false"}
response = requests.get(
    SPARKPOST_HOST + "/api/v1/templates", headers=headers, params=params
)
template_ids = []
for item in response.json()["results"]:
    template_ids.append(item["id"])

# Pulls a list of recipient list IDs into the variable recipient_ids
recipient_ids = []
response = requests.get(SPARKPOST_HOST + "/api/v1/recipient-lists", headers=headers)
for item in response.json()["results"]:
    recipient_ids.append(item["id"])

# If no templates or recipient lists exist, throw a popup window and exit the program
if template_ids == []:
    sg.popup(
        "No templates, please login to SparkPost.com and create a template to use.",
        keep_on_top=True,
    )
    os._exit(0)
elif recipient_ids == []:
    sg.popup(
        "No recipient lists, please login to SparkPost.com and create a recipient list to use.",
        keep_on_top=True,
    )
    os._exit(0)

# Creates the layout of the GUI
layout = [
    [
        sg.Text("Enter RSS URL:", size=(13, 1)),
        sg.InputText(key="rss-url"),
        sg.Button("Read RSS"),
    ],
    [
        sg.Text("How many RSS items to send?", size=(24, 1)),
        sg.InputText(key="rss-number", size=(2, 1)),
    ],
    [sg.Text("Enter Campaign ID", size=(15, 1)), sg.InputText(key="campaign-id")],
    [
        sg.Text("Choose Template", size=(15, 1)),
        sg.Combo(template_ids, size=(50, 1), enable_events=True, key="template-id"),
    ],
    [
        sg.Text("Choose Recipient List", size=(18, 1)),
        sg.Combo(
            recipient_ids,
            default_value=recipient_ids[0],
            size=(50, 1),
            key="recipient-id",
        ),
    ],
    [sg.Button("Update Template")],
    [
        sg.Multiline(size=(80, 30), enable_events=True, key="template"),
        sg.Button("<"),
        sg.Listbox(values=[], size=(30, 25), key="rss-elements"),
    ],
    [sg.Button("Send"), sg.Button("Close")],
]


window = sg.Window(
    "SparkPost RSS Tranmission", layout, finalize=True
)  # Define the window to be shown with the above objects
sp = SparkPost(SPARKPOST_API_KEY)  # Initializing SparkPost
rss_elements = (
    []
)  # Required to store the RSS elements so they do not get overwritten on window events

while True:
    # Read in the window events and values of the objects
    event, values = window.read()
    window.bring_to_front()

    # If a template is selected from the dropdown, get that template using the SparkPost API library and display it in the template box
    if event == "template-id":
        template = sp.templates.get(values["template-id"])
        window["template"].update(template["content"]["html"])

    # If the < button is selected, insert the selected element into the template box
    elif event == "<":
        window["template"].Widget.insert(sg.tk.INSERT, values["rss-elements"])
        window["template"].set_focus()

    # If the Update Template button is clicked, throw a prompt and if confirmed, update the template HTML with the template HTML in the GUI box
    elif event == "Update Template":
        confirm = sg.popup_yes_no(
            "Are you sure you want to update this template?", keep_on_top=True
        )
        if confirm == "Yes":
            template = sp.templates.get(values["template-id"])
            template["content"]["html"] = values["template"]
            params = {"update_published": "true"}
            response = requests.put(
                SPARKPOST_HOST + "/api/v1/templates/" + values["template-id"],
                headers=headers,
                params=params,
                json=template,
            )

    # If the Read RSS button is clicked, parse the RSS URL provided and show the elements in a GUI selection.
    # If the RSS URL is invalid an error will be thrown.
    elif event == "Read RSS":
        feed = feedparser.parse(values["rss-url"])
        if feed.feed.keys():
            keys = feed.feed.keys()
            rss_elements = keys
            window["rss-elements"].update(keys)
        else:
            sg.popup(
                "No keys found in this RSS Feed, please check the RSS URL.",
                keep_on_top=True,
            )

    # If the Send button is clicked go through a number of error checks.
    # Feed in the RSS items, and send the selected template to the selected recipient list.
    elif event == "Send":
        if (
            rss_elements == []
        ):  # If RSS elements haven't been read yet, throw a popup error
            sg.popup("No elements have been read", keep_on_top=True)
        elif (
            values["template-id"] == []
        ):  # If a template hasn't been selected, throw a popup error
            sg.popup("No templates have been selected", keep_on_top=True)
        else:
            feed = feedparser.parse(values["rss-url"])
            if (
                values["rss-number"] == ""
            ):  # If no number of RSS feeds have been selected, throw a popup error.
                sg.popup("No number of feeds selected", keep_on_top=True)
            elif (
                values["rss-number"].isnumeric() == False
            ):  # If number of RSS feeds is non-numeric, throw a popup error.
                sg.popup("Invalid number", keep_on_top=True)
            elif int(values["rss-number"]) > len(
                feed.entries
            ):  # If number of RSS feeds is more than are available, throw a popup error.
                sg.popup("Too many elements selected", keep_on_top=True)
            else:
                # Read in each RSS feed item
                feed = feedparser.parse(values["rss-url"])
                items = []
                for item in range(int(values["rss-number"])):
                    items.append(feed.entries[item])

                # Send the transmission
                sp.transmissions.send(
                    campaign=values["campaign-id"],
                    recipient_list=values["recipient-id"],
                    template=values["template-id"],
                    substitution_data={"items": items},
                )
                sg.popup("Email Sent!", keep_on_top=True)

    # If window is closed or "Close" button is clicked, break out of the while loop
    elif event == sg.WIN_CLOSED or event == "Close":
        break

window.close()
