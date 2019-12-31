# English-ize

_English-ize_ is a web app that takes a Tweet that is composed in English, translate it into several other languages (using [Google Translate API](https://cloud.google.com/translate/)), and finally translate it back into English. 

## Architecture
This app uses various AWS services as its foundational framework. Aside from possible comedic effects, this app is built mainly to demonstrate the current state of app deployment in AWS. 

The following services are used:
- _Lambda_: lambda functions interact with Twitter API and Google Cloud Translate API to obtain the text of the tweet and go through translation layers. The function is written in Python 3.7
- _API Gateway_: receives requests from the user with the tweet, and triggers lambda functions 

## Deployment
This app uses [AWS CLI](https://aws.amazon.com/cli/) to deploy as much as possible, instead of deploying via the web UI. Credentials are never committed to this repo. 