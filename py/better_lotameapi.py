'''
    Filename: better_lotameapi.py
    Author: Brett Coker
    Version: 2.0.0
    Python Version: 3.6+

    A better Python interface for the Lotame API.

    Relies on a token and access key for authentication. You can generate
    those by visiting this page:

    https://platform.lotame.com/user/tokens
    
    Those should be placed into a lotame.ini file in the same directory.
    Please see the sample on Github for formatting. Alternatively, you can
    specify a token and access key when creating a Lotame object.

    After creating a Lotame object, you can use it to make GET, POST,
    PUT, and DELETE commands against the Lotame API.

    Prior to version 2.0.0, this module used Lotame's previous authentication
    scheme. If you're upgrading from a previous version, you should make the
    following changes to any existing scripts:

        - Create a Lotame object
        - Remove references to authenticate(username, password)
        - Remove references to cleanup()
'''
import json
import logging
import configparser
import requests

API_URL = 'https://api.lotame.com/2/'


class Lotame():
    def __init__(self, token=None, access=None):
        if token and access:
            self.headers = {
                'x-lotame-token': token,
                'x-lotame-access': access
            }
            return

        config = configparser.ConfigParser()
        config.read('lotame.ini')
        try:
            self.headers = {
                'x-lotame-token': config['lotame']['token'],
                'x-lotame-access': config['lotame']['access']
            }
        except KeyError:
            raise ConfigError
    
    def get(self, endpoint):
        """Perform a GET request on the Lotame API.

        Args:
            endpoint: the endpoint to use (ex. 'audiences/12345')
        Returns:
            response: the response from the request
        Raises:
            ConnectionError: when connection to API server fails
        """
        for _ in range(3):
            try:
                full_url = self._create_full_url(endpoint)
                response = requests.get(full_url, headers=self.headers)
                response.json()
                return response
            except (ConnectionError, TimeoutError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError,
                    json.decoder.JSONDecodeError):
                logging.info(f'Attempt to hit {full_url} failed')

        # Only raised if 3 attempts to hit the API fail
        error_message = 'Failed to get response from ' + full_url
        raise ConnectionError(error_message)

    def post(self, endpoint, options={}):
        """Perform a POST request on the Lotame API.

        Args:
            endpoint: the endpoint to use (ex. 'audiences/12345')
            options: dict of options to be passed as a JSON, if any (default = {})
        Returns:
            response: the response from the request
        Raises:
            ConnectionError: when connection to API server fails
        """
        for _ in range(3):
            try:
                full_url = self._create_full_url(endpoint)
                response = requests.post(full_url, json=options, headers=self.headers)
                if response.status_code != 204:
                    response.json()
                return response
            except (ConnectionError, TimeoutError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError,
                    json.decoder.JSONDecodeError):
                logging.info(f'Attempt to hit {full_url} failed')

        # Only raised if 3 attempts to hit the API fail
        error_message = 'Failed to get response from ' + full_url
        raise ConnectionError(error_message)

    def put(self, endpoint, options={}):
        """Perform a PUT request on the Lotame API.

        Args:
            endpoint: the endpoint to use (ex. 'audiences/12345')
            options: dict of options to be passed as a JSON, if any (default = {})
        Returns:
            response: the response from the request
        Raises:
            ConnectionError: when connection to API server fails
        """
        for _ in range(3):
            try:
                full_url = self._create_full_url(endpoint)
                response = requests.put(full_url, json=options, headers=self.headers)
                if response.status_code != 204:
                    response.json()
                return response
            except (ConnectionError, TimeoutError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError,
                    json.decoder.JSONDecodeError):
                logging.info(f'Attempt to hit {full_url} failed')

        # Only raised if 3 attempts to hit the API fail
        error_message = 'Failed to get response from ' + full_url
        raise ConnectionError(error_message)

    def delete(self, endpoint):
        """Perform a DELETE request on the Lotame API.

        Args:
            endpoint: the endpoint to use (ex. 'clients/25')
        Returns:
            response: the response from the request
        Raises:
            ConnectionError: when connection to API server fails
        """
        for _ in range(3):
            try:
                full_url = self._create_full_url(endpoint, headers=self.headers)
                response = requests.delete(full_url)
                return response
            except (ConnectionError, TimeoutError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError):
                logging.info(f'Attempt to hit {full_url} failed')

        # Only raised if 3 attempts to hit the API fail
        error_message = 'Failed to get response from ' + full_url
        raise ConnectionError(error_message)

    def _create_full_url(self, endpoint):
        """Put the full API URL together.

        Args:
            endpoint: the endpoint to use (ex. 'audiences/12345')
        Returns:
            full_url: the URL to be used in the request
        """
        endpoint = endpoint.strip()
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        return API_URL + endpoint


class ConfigError(Exception):
    """Raised when lotame.ini is missing or improperly formatted"""
