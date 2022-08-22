<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# SparkPost RSS Tool

[![Build Status](https://github.com/ZSamuels28/SparkPost-RSS-Program/actions/workflows/python-package.yml/badge.svg)](https://github.com/ZSamuels28/SparkPost-RSS-Program/actions/workflows/python-package.yml)

## Easy installation

Firstly ensure you have `python3`, `pip` and `git`.

Next, get the project. Install `pipenv` (`--user` option recommended, [see this article](https://stackoverflow.com/questions/42988977/what-is-the-purpose-pip-install-user)) and [this article for MacOS](https://stackoverflow.com/questions/60004431/pip-error-when-trying-to-run-pip-command-from-virtualenv-on-macos).

Once you have `pipenv`, you can use it to install the project dependencies.

```
git clone https://github.com/ZSamuels28/SparkPost-RSS-Program.git
cd SparkPost-RSS-Program
python3 -m pip install pipenv
pipenv install
```

_Note: In the above commands, you may need to run `pip3` instead of `pip`._

## Pre-requisites

Input your SparkPost API Key into the `sample.env` file and rename the file `variables.env`. Note these are case sensitive:

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

```
cd SparkPost-RSS-Program
pyenv shell
python SparkPost-RSS.py
```

You will see the SparkPost RSS Transmission program with the following inputs/options:

| Option                      | Description                                                                                                                       |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Enter RSS URL:              | Enter your RSS URL here to read the elements from.                                                                                |
| Read RSS                    | Button to read the RSS URL elements.                                                                                              |
| How many RSS items to send? | Determines how many RSS records should be sent.                                                                                   |
| Enter Campaign ID           | Campaign ID to be used with SparkPost.                                                                                            |
| Choose Template             | Drop-down to select which template will be used to be sent. Note, this template will appear below and can be edited here as well. |
| Choose Recipient List       | Drop-down to select the SparkPost recipient list to be sent to.                                                                   |
| Filter Elements             | Allows the user to filter for specific RSS elements in the feed                                                                   |
| Left text box               | When a template is selected, the HTML for that template will appear here. You can also edit this HTML and update it.              |
| Right text box              | When an RSS Feed is loeaded, a list of items will be shown. Clicking on those items will add them to the left text box.           |
| Send                        | Sends the email.                                                                                                                  |
| Update Template             | Updates the selected template HTML with the HTML in the textbox. Note, this has a confirmation dialog as well.                    |
| Close                       | Closes the program.                                                                                                               |

See sample template below for usage:

```html
<html>
  <body>
    {{ each items }}
    <p><a href="{{ loop_var.link }}"> {{ loop_var.title }} </a></p>
    <p>{{ loop_var.summary }}</p>
    {{ end }}
  </body>
</html>
```

Sample sample usage of program below:
![](https://github.com/ZSamuels28/SparkPost-RSS-Program/blob/master/samples/Sample_Usage.gif)
Test
