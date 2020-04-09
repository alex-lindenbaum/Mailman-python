import os
import sys
import json

DEFAULT_REQUEST_DICT = { 'method': '', 'url': '', 'description': '', 'params': {}, 'body': {}, 'headers': {} }

def generate_request_file(path, file, content=DEFAULT_REQUEST_DICT):
	"""
	Generate blank.json file.

	Params:
	path (str): full path to directory
	file (str): name of file that is created,
	content (dict) request file data.

	Return: None.
	"""

	# Create directory if it doesn't exist
	if not os.path.exists(path):
		os.makedirs(path)

	with open(path + '/' + file, 'w') as file_wrapper:
		json.dump(content, file_wrapper, indent=4)


def open_with_editor(file, editor):
	"""
	Open file with preferred editor.

	Params:
	file (str): name of file (including path) that opens,
	editor (str): preferred text editor.

	Return: None.
	"""

	os.system(editor + ' ' + file + ' > /dev/tty')	# redirect to terminal in case stdout not tty


def read_into_dict(file):
	"""
	Open file and reads contents.

	Params:
	file (str): name of file (including path) that is read.

	Return: dict of contents on success, None on failure.
	"""

	try:
		# Open file, load default dict as JSON
		with open(file, 'r') as file_wrapper:
			return json.load(file_wrapper)
	except json.decoder.JSONDecodeError as e:
		# File not in JSON
		print('mailman: ' + file + ' is not in valid JSON format.', file=sys.stderr)
		return None


def is_file_exists(file):
	"""Return True if file exists, False otherwise."""
	return os.path.exists(file)


def remove_file(file):
	"""Remove file."""

	os.remove(file)


def get_presets(path):
	"""
	Get all preset files in directory.

	Params:
	path (str): path to directory.

	Return: (dict) of names (keys) and request data (values), None on failure.
	"""
	
	# Create directory if it doesn't exist
	if not os.path.exists(path):
		os.makedirs(path)
		# No need to do more work
		return {}

	dir_names = os.listdir(path)
	dir_dict = {}

	for name in dir_names:
		if name.endswith('.json'):
			# Most likely a preset file
			content = read_into_dict(path + '/' + name)

			if content == None:
				# Invalid JSON
				return None

			dir_dict[name[0:-5]] = content

	return dir_dict


def print_res(res_dict):
	"""Print to stdout."""

	json.dump(res_dict, sys.stdout, indent=4)


def get_env():
	"""Get environment variables MAILMAN_EDITOR and MAILMAN_PATH_TO_FILES."""

	return os.environ['MAILMAN_EDITOR'], os.environ['MAILMAN_PATH_TO_FILES']