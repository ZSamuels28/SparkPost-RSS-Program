<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

## Pre-requisites

Firstly ensure you have `python` installed.

Then install the following libraries with the following command:
`pip install LIBRARYNAME`
Or if on Mac/Linux:
`pip3 install LIBRARYNAME`

Necessary Libraries:
`os`
`sparkpost`
`dotenv`
`pathlib`
`PySimpleGUI`
`requests`
`feedparser`
`ssl`

Once installed, clone this repo.

Input your SparkPost API Key into the `sample.env` file and rename the file `variables.env`. Note these care case sensitive:

```
SPARKPOST_HOST
    The URL of the SparkPost API service you're using. Defaults to https://api.sparkpost.com.

SPARKPOST_API_KEY
    API key on your SparkPost account, with Recipient Validation rights.
```

The variables.env file should look something like the following:
```
# .env
SPARKPOST_API_KEY=1234567890ABCDEFGHIJKLMNOPQRSTUVXYZ
SPARKPOST_HOST=https://api.sparkpost.com
```

NOTE: You must have templates and receipient lists created in SparkPost, if you do not have any, make sure they are created prior to using this program.

## Usage

Locate and open the SparkPost-RSS.py file utilizing the command prompt or terminal with `python SparkPost-RSS.py` or `python3 SparkPost-RSS.py`.

You will see the SparkPost RSS Transmission program with the following inputs/options:

 Option | Description |
|--|--|
 Enter RSS URL: | Enter your RSS URL here to read the elements from. |
 Read RSS | Button to read the RSS URL elements. |
 How many RSS items to send? | Determines how many RSS records should be sent. |
 Enter Campaign ID | Campaign ID to be used with SparkPost.|
 Choose Template | Drop-down to select which template will be used to be sent. Note, this template will appear below and can be edited here as well. |
 Choose Recipient List | Drop-down to select the SparkPost recipient list to be sent to. |
 Update Template | Updates the selected template HTML with the HTML in the textbox. Note, this has a confirmation dialog as well. |
 < | When an RSS element is selected, add it to the left side HTML. |
Send | Sends the email.|
Close | Closes the program. |