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
params = {"draft": "false"}
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
        font="Any 16",
        keep_on_top=True,
    )
    os._exit(0)
elif recipient_ids == []:
    sg.popup(
        "No recipient lists, please login to SparkPost.com and create a recipient list to use.",
        font="Any 16",
        keep_on_top=True,
    )
    os._exit(0)

# Creates the layout of the GUI
layout = [
    [
        sg.Text("Enter RSS URL:", auto_size_text=True),
        sg.InputText(key="rss-url"),
        sg.Button("Read RSS"),
    ],
    [
        sg.Text("How many RSS items to send?", auto_size_text=True),
        sg.InputText(key="rss-number", size=(2, 1)),
    ],
    [
        sg.Text("Enter Campaign ID:", auto_size_text=True),
        sg.InputText(size=(30, 1), key="campaign-id"),
    ],
    [
        sg.Text("Choose Template", auto_size_text=True),
        sg.Combo(
            template_ids,
            auto_size_text=True,
            enable_events=True,
            readonly=True,
            key="template-id",
        ),
    ],
    [
        sg.Text("Choose Recipient List", auto_size_text=True),
        sg.Combo(
            recipient_ids,
            default_value=recipient_ids[0],
            auto_size_text=True,
            readonly=True,
            key="recipient-id",
        ),
    ],
    [
        sg.Multiline(
            size=(50, 20),
            sbar_arrow_width=15,
            enable_events=True,
            key="template",
        ),
        sg.Button("<", font="Any 30"),
        sg.Listbox(
            values=[],
            size=(30, 19),
            sbar_arrow_width=15,
            key="rss-elements",
        ),
    ],
    [sg.Button("Send"), sg.Button("Update Template"), sg.Button("Close")],
]

window = sg.Window(
    "SparkPost RSS Tranmission", layout, finalize=True, font="Any 16"
)  # Define the window to be shown with the above objects
sp = SparkPost(SPARKPOST_API_KEY)  # Initializing SparkPost
rss_elements = (
    []
)  # Required to store the RSS elements so they do not get overwritten on window events


def center_of_window(window_size, window_location):
    x = window.size[0] / 2
    y = window.size[1] / 2
    center = (window_location[0] + x - 110, window_location[1] + y)
    return center


while True:

    # Read in the window events and values of the objects
    event, values = window.read()
    window.bring_to_front()

    if event != sg.WIN_CLOSED or event == "Close":
        center = center_of_window(
            window.current_size_accurate(), window.current_location()
        )
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
            "Are you sure you want to update this template?",
            location=center,
            font="Any 16",
            keep_on_top=True,
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
            for entry in feed.entries:
                for key in entry.keys():
                    if key not in rss_elements:
                        rss_elements.append(key)
            window["rss-elements"].update(rss_elements)
        else:
            sg.popup(
                "No keys found in this RSS Feed, please check the RSS URL.",
                location=center,
                font="Any 16",
                keep_on_top=True,
            )
            window["rss-elements"].update([])

    # If the Send button is clicked go through a number of error checks.
    # Feed in the RSS items, and send the selected template to the selected recipient list.
    elif event == "Send":
        if feedparser.parse(values["rss-url"]).entries == []:
            # If RSS URL is invalid, throw a popup error
            sg.popup(
                "Invalid RSS URL",
                location=center,
                font="Any 16",
                keep_on_top=True,
            )
        elif (
            values["template-id"] == []
        ):  # If a template hasn't been selected, throw a popup error
            sg.popup(
                "No templates have been selected",
                location=center,
                font="Any 16",
                keep_on_top=True,
            )
        else:
            if (
                values["rss-number"] == ""
            ):  # If no number of RSS feeds have been selected, throw a popup error.
                sg.popup(
                    "No number of feeds selected",
                    location=center,
                    font="Any 16",
                    keep_on_top=True,
                )
            elif (
                values["rss-number"].isnumeric() == False
            ):  # If number of RSS feeds is non-numeric, throw a popup error.
                sg.popup(
                    "Invalid number",
                    location=center,
                    font="Any 16",
                    keep_on_top=True,
                )
            elif int(values["rss-number"]) > len(
                feedparser.parse(values["rss-url"]).entries
            ):  # If number of RSS feeds is more than are available, throw a popup error.
                sg.popup(
                    "Too many elements selected",
                    location=center,
                    font="Any 16",
                    keep_on_top=True,
                )
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
                sg.popup(
                    "Email Sent!",
                    location=center,
                    font="Any 16",
                    keep_on_top=True,
                )

    # If window is closed or "Close" button is clicked, break out of the while loop
    elif event == sg.WIN_CLOSED or event == "Close":
        break

window.close()
