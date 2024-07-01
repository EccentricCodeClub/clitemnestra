import sys

from tomlkit import dumps
from tomlkit import exceptions
from tomlkit import parse


def check_toml_integrity(file_path):
	# print("function: check_toml_integrity")

	# check if file exists
	try:
		with open(file_path, 'r') as f:
			content = f.read()
	except FileNotFoundError as e:
		print("ERROR: FileNotFoundError")
		print(e)
		sys.exit(1)
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)

	# check if toml is valid
	try:
		doc = parse(content)
	except exceptions.TOMLKitError as e:
		print("ERROR: tomlkit.exceptions.TOMLKitError")
		print(e)
		sys.exit(1)
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)

	# check if toml scripts have valid keys
	if doc.get('scripts') is not None:
		for script in doc['scripts']:
			if script.get('name') is None or \
				script.get('path') is None or \
				script.get('executor') is None:
				print("ERROR: Invalid script key")
				sys.exit(1)

	# check if toml executors have valid keys
	if doc.get('executor') is not None:
		for executor in doc['executor']:
			if executor.get('name') is None or \
				executor.get('command') is None:
				print("ERROR: Invalid executor key")
				sys.exit(1)

	return doc



def write_toml(CONFIG_FILE_PATH, content):
	# print("function: write_toml")

	try:
		with open(CONFIG_FILE_PATH, 'w') as f:
			f.write(dumps(content))
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)
