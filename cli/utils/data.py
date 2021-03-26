import json


def load_json(file_path):
	# Read
	with open(file_path, 'r') as myfile:
		data = myfile.read()

	# Parse
	loaded = json.loads(data)

	return loaded
	# except error:
	# 	print(f'Error loading json: {error}')