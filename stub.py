#!/usr/bin/env python3
import requests
import base64


class Stubbie():
    def __init__(self, basic_token=None, username=None, password=None):
        self.base_uri = 'https://api.stubhub.com'
        self.api = self.login(basic_token, username, password)
        self.token = self.api['access_token']
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json'
        }

    def __getitem__(self, item):
        return self.api[item]

    def set_url(self, url):
        if url[0] == '/':
            return self.base_uri + url
        else:
            return self.base_uri + '/' + url

    def add_header(self, header, value):
        self.headers[header] = value

    def login(self, basic_token, username, password, retries=3):
        creds = {
            'basic_token': basic_token,
            'username': username,
            'password': password
        }

        if not all(creds.values()):
            standard_creds = get_creds()
        for cred, cred_value in creds.items():
            if not cred_value:
                creds[cred] = standard_creds[cred]

        url = self.set_url('/sellers/oauth/accesstoken?' +
                           'grant_type=client_credentials')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + creds['basic_token'],
        }
        data = {
            'username': creds['username'],
            'password': creds['password']
        }
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()

        return r.json()

    def search_locations(self, params):
        '''Search for events in a particular location'''
        allowed_params = {
            'q',
            'city',
            'state',
            'country',
            'postalCode',
            'point',
            'radius',
            'units',
            'sort',
            'fieldList',
            'start',
            'rows'
        }

    def _check_params(self, params, allowed_params):
        disallowed_params = set(params) - set(allowed_params)

        if disallowed_params != set():
            print('The following parameters are not allowed:\n' +
                  f'{disallowed_params}\nPlease only specify parameters from' +
                  f'the following list:\n{allowed_params}')
            return False
        else:
            return True


def get_creds():
    data = {
        'consumer_key': '.secrets/consumer.key',
        'consumer_secret': '.secrets/consumer.secret',
        'username': '.secrets/username',
        'password': '.secrets/password',
    }

    for key, val in data.items():
        try:
            with open(val) as f:
                data[key] = f.read().strip()
        except OSError:
            print('Please store your credentials in the .secrets folder or' +
                  ' add them into the class when initialising.')
            exit()

    token_combo = data['consumer_key'] + ':' + data['consumer_secret']
    data['basic_token'] = str(base64.b64encode(token_combo.encode('utf-8')),
                              'utf-8')

    return data


if __name__ == '__main__':
    stub = Stubbie()
    print(stub.api)
