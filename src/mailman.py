import sys
import file_stuff as fs
import request_stuff as rs

def validate(file_path):
	"""Check for valid JSON and params."""

	req_data = fs.read_into_dict(file_path)

	if req_data == None:
		return None

	modified_req = rs.validate_and_modify(req_data)

	return modified_req


def send_new_request():
	"""
	Send new HTTP request.

	Function sequence:
	NEW FILE --> USER WRITES --> TO_DICT --> VALIDATE --> COPY TO PREV --> SEND --> PRINT RES.

	Return: True on success, False on failure.
	"""

	file_path = path_to_files + '/blank.json'

	# NEW FILE
	fs.generate_request_file(path_to_files, 'blank.json')

	# USER WRITES
	fs.open_with_editor(file_path, editor)

	# TO_DICT - VALIDATE
	req_data = validate(file_path)

	while req_data == None:
		print('mailman: open editor again (y/N)? ', file=sys.stderr)

		if input().lower() == 'y':
			fs.open_with_editor(file_path, editor)
			req_data = validate(file_path)
		else:
			fs.remove_file(file_path)
			return False

	# COPY TO PREV
	fs.generate_request_file(path_to_files, 'PREV.json', content=req_data)

	# SEND REQUEST
	res = rs.send_request(req_data)

	if res == None:
		# Bad request
		fs.remove_file(file_path)
		return False

	# PRINT RESPONSE
	fs.print_res(rs.response_to_dict(res))

	# Cleanup
	fs.remove_file(file_path)
	return True


def send_preset_request(name):
	"""
	Send preset HTTP request.

	Function sequence:
	TO_DICT --> VALIDATE --> SEND --> PRINT RES.

	Return: True on success, False on failure.
	"""

	file_name = name + '.json'
	file_path = path_to_files + '/' + file_name

	if not fs.is_file_exists(file_path):
		# File does not exist
		if name == 'PREV':
			print('mailman: there was no previously sent request.', file=sys.stderr)
		else:
			print('mailman: preset "' + name + '" does not exist.', file=sys.stderr)

		return False

	# TO_DICT - VALIDATE
	req_data = validate(file_path)
	if req_data == None:
		# Bad request data
		# Print err statement made in validate()
		return False

	# SEND REQUEST
	res = rs.send_request(req_data)

	if res == None:
		# Bad request
		return False

	# PRINT RESPONSE
	fs.print_res(rs.response_to_dict(res))

	return True


def add_preset(name):
	"""Add or edit a preset request."""
	file_name = name + '.json'
	file_path = path_to_files + '/' + file_name

	if fs.is_file_exists(file_path):
		# File exists
		print('mailman: "' + name + '" already exists.')
	else:
		# File does not exist: create it
		fs.generate_request_file(path_to_files, file_name)

	fs.open_with_editor(file_path, editor)


def remove_preset(name):
	"""Remove a preset."""

	file_path = path_to_files + '/' + name + '.json'

	if fs.is_file_exists(file_path):
		fs.remove_file(file_path)
		print('mailman: "' + name + '" removed.', file=sys.stderr)
	else:
		print('mailman: "' + name + '" is not a preset.')


def print_all_presets():
	"""Print name and description of all presets."""

	dir_dict = fs.get_presets(path_to_files)
	if dir_dict == None:
		# Error in reading into dicts
		return False

	for name, content in dir_dict.items():
		if name != 'PREV':
			if not ('description' in content) or content['description'] == '':
				print(name)
			else:
				print(name + ': ' + content['description'])

	return True


if __name__ == '__main__':
	# Global variables
	editor, path_to_files = fs.get_env()

	if len(sys.argv) < 2:
		print('mailman: usage: ' + sys.argv[0] + ' <arg1> [arg2]', file=sys.stderr)
	else:
		command = sys.argv[1]
		
		if command == 'new':
			send_new_request()
		elif command == 'prev':
			send_preset_request('PREV')
		elif command == 'print':
			print_all_presets()
		else:
			if len(sys.argv) < 3:
				print('mailman: usage: ' + sys.argv[0] + ' <arg1> [arg2]', file=sys.stderr)
			else:
				option = sys.argv[2]

				if command == 'add' or command == 'edit':
					add_preset(option)
				elif command == 'remove':
					remove_preset(option)
				elif command == 'send':
					send_preset_request(option)