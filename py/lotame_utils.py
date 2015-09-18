import httplib, json, requests

AUTH_URL = "https://crowdcontrol.lotame.com/auth/v1/tickets"
API_URL = "https://api.lotame.com/2"

def getTicketGrandingTicket(username, password):
	payload= {'username':username,'password':password}
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
	response = requests.post(AUTH_URL, data=payload)
	grantLocation = response.headers['location']
	return grantLocation

def getServiceTicket(service, grantLocation):
	payload = {'service': service}
	serviceTicket = requests.post( grantLocation, data=payload ).text
	return serviceTicket

# make the supplied API call using the supplied credentials
def getRequest(username, password, service):
	grantLocation = getTicketGrandingTicket(username, password)
	serviceTicket = getServiceTicket(service, grantLocation)
	headers = {'Accept':'application/json'}
	if '?' in service:
		response = requests.get( ('%s&ticket=%s') % (service, serviceTicket), headers=headers)
	else:
		response = requests.get( ('%s?ticket=%s') % (service, serviceTicket), headers=headers)
	return response

def postRequest(username, password, service, payload):
	grantLocation = getTicketGrandingTicket(username, password)
	serviceTicket = getServiceTicket(service, grantLocation)
	headers = {'Accept':'application/json',"Content-type":"application/json"}
	if '?' in service:
		response = requests.post( ('%s&ticket=%s') % (service, serviceTicket), headers=headers, data=payload)
	else:
		response = requests.post( ('%s?ticket=%s') % (service, serviceTicket), headers=headers, data=payload)
	return response
