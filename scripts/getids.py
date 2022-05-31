import os
import PySimpleGUI as sg
import requests


def get_template_ids(sparkpost_host, api_key):
    # Pulls a list of template IDs into the variable template_ids
    headers = {"Authorization": api_key}
    params = {"draft": "false"}
    response = requests.get(
        "".join([sparkpost_host, "/api/v1/templates"]),
        headers=headers,
        params=params,
    )
    template_ids = []
    for item in response.json()["results"]:
        template_ids.append(item["id"])
    # If no templates or recipient lists exist, throw a popup window and exit the program
    if template_ids == []:
        sg.popup(
            "No templates, please login to SparkPost.com and create a template to use.",
            font="Any 16",
            keep_on_top=True,
        )
        os._exit(0)
    return template_ids


def get_recipient_ids(sparkpost_host, api_key):
    # Pulls a list of recipient list IDs into the variable recipient_ids
    recipient_ids = []
    headers = {"Authorization": api_key}
    response = requests.get(
        "".join([sparkpost_host, "/api/v1/recipient-lists"]),
        headers=headers,
    )
    for item in response.json()["results"]:
        recipient_ids.append(item["id"])

    if recipient_ids == []:
        sg.popup(
            "No recipient lists, please login to SparkPost.com and create a recipient list to use.",
            font="Any 16",
            keep_on_top=True,
        )
        os._exit(0)
    return recipient_ids
