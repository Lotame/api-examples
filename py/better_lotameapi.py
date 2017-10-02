'''
    Filename: better_lotameapi.py
    Author: Brett Coker
    Version: 1.1.5
    Python Version: 3.6.1

    A better Python interface for the Lotame API.

    Call authenticate(username, password) once in order to authenticate, and
    don't worry about passing around credentials or tickets after that.

    Call any of the four main requests by passing in an endpoint as an
    parameter. If you need to send a JSON file (or Python dict) along with your
    request, use that as the second parameter.

    The objects returned from the four main requests are Resonse objects. This
    decision was made so that status codes and the like could be read. If you
    need the response JSON, just use .json() on the resulting object.

    If you want to be nice to our API, be sure to cleanup() after yourself when
    you're done.
'''
import json
import requests

API_URL = 'https://api.lotame.com/2/'
AUTH_URL = 'https://crowdcontrol.lotame.com/auth/v1/tickets'
TGT = ''


def authenticate(username, password):
    """Authenticate with the Lotame API.

    Args:
        username: your Lotame username (email address)
        password: your Lotame password
    Raises:
        AuthenticationError: if username/password combo is invalid
    """
    global TGT
    payload = {'username': username, 'password': password}

    try:
        TGT = requests.post(AUTH_URL, data=payload).headers['location']
    except KeyError:
        raise AuthenticationError('Error: Username and/or password invalid.')


def cleanup():
    """Delete the ticket-granting ticket."""
    global TGT
    requests.delete(TGT)
    TGT = ''


def not_authenticated(TGT):
    """Return if ticket-granting ticket has been received."""
    return TGT == ''


def get(endpoint):
    """Perform a GET request on the Lotame API.

    Args:
        endpoint: the endpoint to use (ex. 'clients/25')
    Returns:
        response: the response from the request
    Raises:
        ConnectionError: when connection to API server fails
    """
    attempts = 0
    while attempts < 3:
        try:
            full_url = _prepare_endpoint(endpoint.strip())
            response = requests.get(full_url)
            response.json()
            return response
        except (ConnectionError, TimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                json.decoder.JSONDecodeError):
            attempts += 1

    # Only raised if 3 attempts to hit the API fail
    error_message = 'Failed to get response from ' + full_url
    raise ConnectionError(error_message)


def post(endpoint, options={}):
    """Perform a POST request on the Lotame API.

    Args:
        endpoint: the endpoint to use (ex. 'clients/25')
        options: dict of options to be passed as a JSON, if any (default = {})
    Returns:
        response: the response from the request
    Raises:
        ConnectionError: when connection to API server fails
    """
    attempts = 0
    while attempts < 3:
        try:
            full_url = _prepare_endpoint(endpoint.strip())
            response = requests.post(full_url, json=options)
            if response.status_code != 204:
                response.json()
            return response
        except (ConnectionError, TimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                json.decoder.JSONDecodeError):
            attempts += 1

    # Only raised if 3 attempts to hit the API fail
    error_message = 'Failed to get response from ' + full_url
    raise ConnectionError(error_message)


def put(endpoint, options={}):
    """Perform a PUT request on the Lotame API.

    Args:
        endpoint: the endpoint to use (ex. 'clients/25')
        options: dict of options to be passed as a JSON, if any (default = {})
    Returns:
        response: the response from the request
    Raises:
        ConnectionError: when connection to API server fails
    """
    attempts = 0
    while attempts < 3:
        try:
            full_url = _prepare_endpoint(endpoint.strip())
            response = requests.put(full_url, json=options)
            if response.status_code != 204:
                response.json()
            return response
        except (ConnectionError, TimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                json.decoder.JSONDecodeError):
            attempts += 1

    # Only raised if 3 attempts to hit the API fail
    error_message = 'Failed to get response from ' + full_url
    raise ConnectionError(error_message)


def delete(endpoint):
    """Perform a DELETE request on the Lotame API.

    Args:
        endpoint: the endpoint to use (ex. 'clients/25')
    Returns:
        response: the response from the request
    Raises:
        ConnectionError: when connection to API server fails
    """
    attempts = 0
    while attempts < 3:
        try:
            full_url = _prepare_endpoint(endpoint.strip())
            response = requests.delete(full_url)
            return response
        except (ConnectionError, TimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError):
            attempts += 1

    # Only raised if 3 attempts to hit the API fail
    error_message = 'Failed to get response from ' + full_url
    raise ConnectionError(error_message)


def _prepare_endpoint(endpoint):
    """Prepare endpoint for execution.

    Args:
        endpoint: the endpoint to use (ex. 'clients/25')
    Returns:
        full_url: the URL to be used in the request
    Raises:
        AuthenticationError: if there is no ticket-granting ticket
    """
    if not_authenticated(TGT):
        raise AuthenticationError('Error: Not authenticated.')

    # Remove preceding slash from endpoint, if any
    if endpoint[0] == '/':
        endpoint = endpoint[1:]

    service_call = API_URL + endpoint
    payload = {'service': service_call}
    service_ticket = requests.post(TGT, data=payload).text

    # Use proper character to append ticket, depending on endpoint
    if '?' in endpoint:
        full_url = service_call + '&ticket=' + service_ticket
    else:
        full_url = service_call + '?ticket=' + service_ticket

    return full_url


class AuthenticationError(Exception):
    """Raise when authentication has not been granted."""
