import sys

from tomlkit import dumps
from tomlkit import nl
from tomlkit import parse
from tomlkit import table


def check_toml_integrity(file_path):
	# print("function: check_toml_integrity")

	doc = read_toml(file_path)
	content = check_syntax(doc)
	check_valid_keys(content)

	return content



def read_toml(file_path):
	# print("function: read_toml")

	# check if file exists
	try:
		with open(file_path, 'r') as f:
			doc = f.read()
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)

	return doc



def check_syntax(doc):
	# print("function: check_syntax")

	# check if toml is valid
	try:
		content = parse(doc)
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)

	return content



def check_valid_keys(content):
	# print("function: check_valid_keys")

	# check if toml scripts have valid keys
	if content.get('scripts') is not None:
		for script in content['scripts']:
			if script.get('name') is None or \
				script.get('path') is None or \
				script.get('executor') is None or \
				script.get('tags') is None:
				print("ERROR: Invalid script key")
				sys.exit(1)

	# check if toml executors have valid keys
	if content.get('executor') is not None:
		for executor in content['executor']:
			if executor.get('name') is None or \
				executor.get('command') is None or \
				executor.get('tags') is None:
				print("ERROR: Invalid executor key")
				sys.exit(1)



def write_toml(CONFIG_FILE, content):
	# print("function: write_toml")

	check_valid_keys(check_syntax(dumps(content)))

	try:
		with open(CONFIG_FILE, 'w') as f:
			f.write(dumps(content))
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)



def toml_script_create(CONFIG_FILE, content, new_script):
	# print("function: toml_script_create")

	for item in new_script:
		try:
			script = table()
			script.add('name', item['name'])
			script.add('path', item['path'])
			script.add('executor', item['executor'])
			script.add('tags', item['tags'])
			script.add(nl())

			content['scripts'].append(script)

			write_toml(CONFIG_FILE, content)
		except Exception as e:
			print("ERROR: General Exception")
			print(e)
			sys.exit(1)



def toml_executor_create(CONFIG_FILE, content, new_executor):
	# print("function: toml_executor_create")

	for item in new_executor:
		try:
			executor = table()
			executor.add('name', item['name'])
			executor.add('command', item['command'])
			executor.add('tags', item['tags'])
			executor.add(nl())

			content['executor'].append(executor)

			write_toml(CONFIG_FILE, content)
		except Exception as e:
			print("ERROR: General Exception")
			print(e)
			sys.exit(1)


