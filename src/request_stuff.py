import sys
import requests

HTTP_METHODS = [ 'GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE' ]

def print_validation_error(param):
	print('mailman: invalid or missing "' + param + '" parameter.', file=sys.stderr)

def validate_and_modify(data):
	"""
	Validate and modify HTTP request data from JSON's.

	Params:
	data (dict): info about request directly from JSON.

	Return: ready-for-use data on success, otherwise None.
	"""

	keys = data.keys()

	if not 'method' in keys or type(data['method']) != str:
		print_validation_error('method')
		return None

	data['method'] = data['method'].upper()
	if not data['method'] in HTTP_METHODS:
		print_validation_error('method')
		return None

	if not 'url' in keys or type(data['url']) != str or data['url'] == '':
		print_validation_error('url')
		return None

	if 'description' in keys:
		data.pop('description')

	# requests.request takes data, not body.
	if 'body' in keys:
		data['data'] = data.pop('body')

	return data


def send_request(request_data):
	"""
	Send HTTP request.

	Params:
	request_data (dict): formatted* data on http request. [method, url, data]

	Return: Response object, or None on failure.
	"""
	try:
		return requests.request(**request_data)
	except requests.exceptions.MissingSchema:
		# Invalid URL
		print('mailman: invalid url "' + request_data['url'] + '."', file=sys.stderr)
	except requests.exceptions.ConnectionError:
		# Failed to connect
		print('mailman: failed to connect to "' + request_data['url'] + '."', file=sys.stderr)

	return None


def response_to_dict(res):
	"""
	Pull out response data.

	Params:
	res (Response): return value of requests.request.

	Return: dict of data in res.
	"""

	headers = dict(res.headers)

	return {
		'url': res.url,
		'status_code': res.status_code,
		'headers': headers,
		'text': dict(res.json()) if 'Content-Type' in headers and 'application/json' in headers['Content-Type'].lower() else res.text
	}