from google.cloud import translate_v2
from google.oauth2 import service_account
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import base64
from urllib.parse import quote_plus


TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
GCLOUD_SERVICE_ACCOUNT_STR = os.environ['GCLOUD_SERVICE_ACCOUNT_STR']


def lambda_handler(event, context):

	def twitter_app_auth():
		key = quote_plus(TWITTER_KEY)
		secret = quote_plus(TWITTER_SECRET)
		auth_token = base64.b64encode('{}:{}'.format(key, secret).encode('utf8'))
		r = requests.post("https://api.twitter.com/oauth2/token",
											data={'grant_type': 'client_credentials'},
											headers={'Authorization': f'Basic {auth_token.decode("utf8")}',
											 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})
		if r.status_code == 200:
			return r.json().get('access_token')

	def twitter_status_text(bearer_token, status_id):
		r = requests.get("https://api.twitter.com/1.1/statuses/show.json",
										 params={'id': f'{status_id}',
										 				 'tweet_mode': 'extended',
										 				 'trim_user': True,
										 				 'include_entities': False,
										 				 'include_ext_alt_text': False,
										 				 'include_card_uri': False
							 			 },
										 headers={'Authorization': f'Bearer {bearer_token}'})
		if r.status_code == 200:
			return r.json().get('full_text')

	def translate(input_string, source_lang='en', target_lang='es'):
		credentials = service_account.Credentials.from_service_account_info(json.loads(GCLOUD_SERVICE_ACCOUNT_STR))
		translate_client = translate_v2.Client(credentials=credentials)
		result = translate_client.translate(input_string, source_language=source_lang, target_language=target_lang, model='base')
		return result

	# Main operations
	bearer_token = twitter_app_auth()
	status_id = json.loads(event['body'])['tweet_id']
	status_text = twitter_status_text(bearer_token, status_id)
	
	langs = ['en', 'es', 'bn', 'zh-TW', 'fa', 'ru', 'en']
	translation = status_text
	for i in range(len(langs)-1):
		translation = translate(translation, langs[i], langs[i+1]).get('translatedText')

	res_body = json.dumps({
		'originalTweetText' : f'{status_text}',
		'translatedText': f'{translation}'
  })

	return {
		'statusCode': 200,
		'body': res_body
  }
