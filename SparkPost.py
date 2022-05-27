"""
Script to pull RSS data and pass into SparkPost as substitution data
"""
import os
from sparkpost import SparkPost
from dotenv import load_dotenv
from pathlib import Path
import PySimpleGUI as sg
import requests
import feedparser
import ssl

#Loads the SparkPost API Key and Host from the varaibles.env file
dotenv_path = Path('./variables.env')
load_dotenv(dotenv_path=dotenv_path)
SPARKPOST_API_KEY = os.getenv('SPARKPOST_API_KEY')
SPARKPOST_HOST = os.getenv('SPARKPOST_HOST')


ssl._create_default_https_context = ssl._create_unverified_context

headers = {'Authorization' : SPARKPOST_API_KEY}
response = requests.get(SPARKPOST_HOST + '/api/v1/templates?draft=false',headers=headers)
template_ids = []
recipient_ids = []
for item in response.json()['results']:
    template_ids.append(item['id'])

response = requests.get(SPARKPOST_HOST + '/api/v1/recipient-lists',headers=headers)
for item in response.json()['results']:
    recipient_ids.append(item['id'])

if template_ids == []:
    sg.popup("No templates, please login to SparkPost.com and create a template to use.")
    os._exit(0)
elif recipient_ids == []:
    sg.popup("No recipient lists, please login to SparkPost.com and create a recipient list to use.")
    os._exit(0)

layout = [
    [sg.Text('Enter RSS URL',size=(15,1)),sg.InputText(key='rss-url'),sg.Button('Read RSS')],
    [sg.Text('How many RSS items to send?', size =(25, 1)), sg.InputText(key='rss-number',size=(3,1))],
    [sg.Text('Enter Campaign ID', size =(15, 1)), sg.InputText(key='campaign-id')],
    [sg.Text('Choose Template', size =(15, 1)), sg.Combo(template_ids,size=(50,1),enable_events=True,key='template-id')],
    [sg.Text('Choose Recipient List', size =(18, 1)), sg.Combo(recipient_ids,default_value=recipient_ids[0],size=(50,1),key='recipient-id')],
    [sg.Button('Update Template')],
    [sg.Multiline(size=(80,30),enable_events=True,key='template'),
        sg.Button("<"),
        sg.Listbox(values=[],size=(30,25),key='rss-elements')],
    [sg.Button("Send"), sg.Button("Close")]
]
  
window = sg.Window('SparkPost RSS Tranmission', layout, return_keyboard_events=True, finalize=True)
window.bring_to_front()
template_box = window["template"]

sp = SparkPost(SPARKPOST_API_KEY)

rss_elements = []

while True:
    event, values = window.read()
    window.bring_to_front()

    if event == "template-id":
        template = sp.templates.get(values['template-id'])
        window['template'].update(template['content']['html'])

    #if event == "template":
        #m1.get_focus()
        #print("Hello!")

    elif (event == "<"):
        template_box.set_focus()
        template_box.update("Test",append=True)

    elif (event == 'Update Template'):
        confirm = sg.popup_yes_no("Are you sure you want to update this template?",keep_on_top=True)
        if confirm == "Yes":
            template = sp.templates.get(values['template-id'])
            template['content']['html'] = values['template']
            params = {'update_published' : 'true'}
            response = requests.put(SPARKPOST_HOST + '/api/v1/templates/' + values['template-id'],headers=headers,params=params,json=template)

    elif (event == 'Read RSS'):
        feed = feedparser.parse(values['rss-url'])
        if feed.feed.keys():
            keys = feed.feed.keys()
            rss_elements = keys
            window['rss-elements'].update(keys)
        else:
            sg.popup("No keys found in this RSS Feed, please check the RSS URL.",keep_on_top=True)
    
    elif (event == 'Send'):
        if rss_elements == []:
            sg.popup("No elements have been read",keep_on_top=True)
        elif values['template-id'] == []:
            sg.popup("No templates have been selected",keep_on_top=True)
        else:
            feed = feedparser.parse(values['rss-url'])
            if values['rss-number'] == "":
                sg.popup("No number of feeds selected", keep_on_top=True)
            elif values['rss-number'].isnumeric() == False:
                sg.popup("Invalid number", keep_on_top=True)
            elif int(values['rss-number']) > len(feed.entries):
                sg.popup("Too many elements selected", keep_on_top=True)
            else:
                feed = feedparser.parse(values['rss-url'])
                items = []
                for item in range(int(values['rss-number'])):
                    items.append(feed.entries[item])
                sp.transmissions.send(
                    campaign=values['campaign-id'],
                    recipient_list=values['recipient-id'],
                    template=values['template-id'],
                    substitution_data = {'items' : items}
                    )
                sg.popup("Email Sent!",keep_on_top=True)

    elif event == sg.WIN_CLOSED or event == 'Close':
        break

window.close()