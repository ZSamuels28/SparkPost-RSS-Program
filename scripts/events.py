import PySimpleGUI as sg
import requests
import feedparser
from scripts.build_window import center_of_window

# Feed in the RSS items, and send the selected template to the selected recipient list.
# Note there are a number of error checks before sending.
def send(window, window_values, sparkpost):
    window_center = center_of_window(window)
    if feedparser.parse(window_values["rss-url"]).entries == []:
        # If RSS URL is invalid, throw a popup error
        sg.popup(
            "Invalid RSS URL",
            location=window_center,
            font="Any 16",
            keep_on_top=True,
        )
    elif (
        window_values["template-id"] == []
    ):  # If a template hasn't been selected, throw a popup error
        sg.popup(
            "No templates have been selected",
            location=window_center,
            font="Any 16",
            keep_on_top=True,
        )
    else:
        if (
            window_values["rss-number"] == ""
        ):  # If no number of RSS feeds have been selected, throw a popup error.
            sg.popup(
                "No number of feeds selected",
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )
        elif (
            window_values["rss-number"].isnumeric() == False
        ):  # If number of RSS feeds is non-numeric, throw a popup error.
            sg.popup(
                "Invalid number",
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )
        elif int(window_values["rss-number"]) > len(
            feedparser.parse(window_values["rss-url"]).entries
        ):  # If number of RSS feeds is more than are available, throw a popup error.
            sg.popup(
                "Too many elements selected",
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )
        else:
            # Read in each RSS feed item
            feed = feedparser.parse(window_values["rss-url"])
            items = []
            for item in range(int(window_values["rss-number"])):
                items.append(feed.entries[item])

            # Send the transmission
            sparkpost.transmissions.send(
                campaign=window_values["campaign-id"],
                recipient_list=window_values["recipient-id"],
                template=window_values["template-id"],
                substitution_data={"items": items},
            )
            sg.popup(
                "Email Sent!",
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )


# Parse the RSS URL provided and show the elements in a GUI selection.
# If the RSS URL is invalid (contains no elements) an error will be thrown.
def read_rss(window, window_values, rss_elements):
    window_center = center_of_window(window)
    feed = feedparser.parse(window_values["rss-url"])
    if feed.feed.keys():
        for entry in feed.entries:
            for key in entry.keys():
                if key not in rss_elements:
                    rss_elements.append(key)
        rss_elements.sort()
        window["rss-elements"].update(values=rss_elements)
    else:
        sg.popup(
            "No keys found in this RSS Feed, please check the RSS URL.",
            location=window_center,
            font="Any 16",
            keep_on_top=True,
        )
        rss_elements = []
        window["rss-elements"].update(values=rss_elements)


# Throw a prompt and if confirmed, update the template HTML with the template HTML in the GUI box
def update_template(window, window_values, sparkpost, host, api_key):
    window_center = center_of_window(window)
    confirm = sg.popup_yes_no(
        "Are you sure you want to update this template?",
        location=window_center,
        font="Any 16",
        keep_on_top=True,
    )
    if confirm == "Yes":
        template = sparkpost.templates.get(window_values["template-id"])
        template["content"]["html"] = window_values["template"]
        params = {"update_published": "true"}
        headers = {"Authorization": api_key}
        response = requests.put(
            "".join([host, "/api/v1/templates/", template["id"]]),
            headers=headers,
            params=params,
            json=template,
        )
        if response.status_code == 200:
            sg.popup(
                "Template successfully updated.",
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )
        else:
            sg.popup(
                "".join(
                    [
                        "Template update failed with status code ",
                        str(response.status_code),
                        ": ",
                        response.reason,
                    ]
                ),
                location=window_center,
                font="Any 16",
                keep_on_top=True,
            )


def rss_elements(window, window_values):
    window["template"].Widget.insert(sg.tk.INSERT, window_values["rss-elements"])
    window["rss-elements"].update(set_to_index=-1)
    window["template"].set_focus()


def filter(window, window_values, rss_elements):
    if window_values["filter"] == "":
        window["rss-elements"].update(rss_elements)
    else:
        search = window_values["filter"]
        new_values = [x for x in rss_elements if search in x]  # do the filtering
        window["rss-elements"].update(new_values)  # display in the listbox


# If a template is selected from the dropdown, get that template using the SparkPost API library and display it in the template box
def template_id(window, window_values, sparkpost):
    template = sparkpost.templates.get(window_values["template-id"])
    window["template"].update(template["content"]["html"])
