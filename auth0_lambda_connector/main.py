import datetime
import json
import os
import requests
from urllib.parse import quote

def lambda_handler(req, context):
  access_token = get_auth0_access_token(req["secrets"])
  headers = {
    'authorization': 'Bearer {}'.format(access_token)
  }
  last_updated_at = req['state'].get('updated_last', '2021-07-14T00')

  
  search_params = 'updated_at:[{} TO *]'.format(last_updated_at)
  page = 0
  records = []

  while True:  
    new_records = get_user_records(req["secrets"]['auth0_api_base_url'], headers, search_params, page)

    if len(new_records) == 0:
      break

    records.extend(new_records)
    page += 1

  return build_response(records)

def get_user_records(base_url, headers, search_params, page):
  url = '{base_url}users?q={search_params}&page={page}'.format(
    base_url=base_url,
    search_params=quote(search_params),
    page=page
  )
  result = requests.get(url, headers=headers)

  if result.status_code != 200:
    raise Exception("Auth0 api error: status {}, {}".format(result.status_code, result.content))

  data = json.loads(result.content)
  return [format_user_data(user) for user in data]
  

def build_response(records):
  return {
    "state": {
      "updated_last": datetime.datetime.now().strftime('%Y-%m-%dT%H')
    },
    "schema": {
      "user_data": {
        "primary_key": ["user_id"] 
      }
    },
    "insert": {
      "user_data": records
    },
    "hasMore": False
  }

def format_user_data(user):
  return {
    'email': user['email'],
    'updated_at': user['updated_at'],
    'created_at': user['created_at'],
    'user_id': user['user_id'],
    'last_login': user.get('last_login', ''),
    'logins_count': user.get('logins_count', '')
  }

def get_auth0_access_token(config):
  url = config['auth0_api_auth_url']
  payload = {
    'client_id': config['auth0_client_key'],
    'client_secret': config['auth0_client_secret'],
    'audience': config['auth0_api_base_url'],
    'grant_type': 'client_credentials'
  }
  result = requests.post(url, data=payload)

  return json.loads(result.content)['access_token']