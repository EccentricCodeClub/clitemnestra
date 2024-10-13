#! /usr/bin/env python3

import os
import sys

from clitemnestra.toml import check_toml_integrity
from clitemnestra.toml import write_toml
from clitemnestra.toml import toml_script_create
from clitemnestra.toml import toml_executor_create

from clitemnestra.rich import rich_execution
from clitemnestra.rich import rich_script_read
from clitemnestra.rich import rich_executor_read



def command_executor(CONFIG_FILE, parser):
	# print("function: command_executor")

	if parser.executor_command == 'create':
		command_create(CONFIG_FILE, 0, parser.nickname, parser.runner, None, None)
	elif parser.executor_command == 'read':
		command_read(CONFIG_FILE, 0, parser.nickname)
	elif parser.executor_command == 'update':
		command_update(CONFIG_FILE, 0, parser.nickname, parser.new_nickname, parser.new_runner, None, None)
	elif parser.executor_command == 'delete':
		command_delete(CONFIG_FILE, 0, parser.nickname)
	else:
		print("Invalid executor command")
		sys.exit(1)



def command_script(CONFIG_FILE, parser):
	# print("function: command_script")

	if parser.script_command == 'create':
		command_create(CONFIG_FILE, 1, parser.nickname, None, parser.path, parser.executor)
	elif parser.script_command == 'read':
		command_read(CONFIG_FILE, 1, parser.nickname)
	elif parser.script_command == 'update':
		command_update(CONFIG_FILE, 1, parser.nickname, parser.new_nickname, None, parser.new_path, parser.new_executor)
	elif parser.script_command == 'delete':
		command_delete(CONFIG_FILE, 1, parser.nickname)
	else:
		print("Invalid script command")
		sys.exit(1)



def command_create(CONFIG_FILE, item_type, nickname, runner=None, path=None, executor=None):
	# print("function: command_create")

	# check if parameters are valid
	if item_type == 0:
		# CONFIG_FILE, item_type, parser.nickname, parser.runner
		if CONFIG_FILE is None or nickname is None or runner is None:
			print("ERROR: create executor requires nickname and runner")
			sys.exit(1)
	elif item_type == 1:
		# CONFIG_FILE, item_type, parser.nickname, parser.path, parser.executor
		if CONFIG_FILE is None or nickname is None or path is None or executor is None:
			print("ERROR: create script requires nickname, path and executor")
			sys.exit(1)

	content = check_toml_integrity(CONFIG_FILE)

	if item_type == 0:
		# check if name already exists
		for executor in content['executor']:
			if executor['name'] == nickname:
				print("ERROR: name already exists")
				print("Please use a different name")
				sys.exit(1)

		new_executor = [
			{
				'name': nickname,
				'command': runner,
				'tags': []
			}
		]

		toml_executor_create(CONFIG_FILE, content, new_executor)

	elif item_type == 1:

		# check if nickname already exists
		for script in content['scripts']:
			if script['name'] == nickname:
				print("ERROR: nickname already exists")
				print("Please use a different nickname")
				sys.exit(1)

		# check if executor exists
		executor_exists = False
		for exec in content['executor']:
			if exec['name'] == executor:
				executor_exists = True
				break

		if not executor_exists:
			print("ERROR: executor not found")
			print("Please create the executor first")
			sys.exit(1)

		new_script = [
			{
				'name': nickname,
				'path': path,
				'executor': executor,
				'tags': []
			}
		]

		toml_script_create(CONFIG_FILE, content, new_script)



def command_read(CONFIG_FILE, item_type, nickname):
	# print("function: command_read")

	content = check_toml_integrity(CONFIG_FILE)

	if item_type == 0:

		# check if nickname exists
		nickname_exists = False
		target = None

		for executor in content['executor']:
			if executor['name'] == nickname:
				nickname_exists = True
				target = executor
				break

		if not nickname_exists or target is None:
			print("ERROR: nickname not found")
			sys.exit(1)

		matrix_executor = []
		matrix_executor.append([target['name'], target['command'], '\n'.join(target['tags'])])

		rich_executor_read(nickname, matrix_executor)

	elif item_type == 1:
		# check if nickname exists
		nickname_exists = False
		target = None
		execution = None

		for script in content['scripts']:
			if script['name'] == nickname:
				nickname_exists = True
				target = script
				break

		if not nickname_exists or target is None:
			print("ERROR: nickname not found")
			sys.exit(1)

		rich_script_read(nickname, target, content['executor'])

		for items in content['executor']:
			if items['name'] == target['executor']:
				execution = items['command'] + " " + target['path']

				break

		if execution is not None:
			print()
			rich_execution(execution)
			print()



def command_update(CONFIG_FILE, item_type, nickname, new_nickname, new_runner, new_path, new_executor):
	# print("function: command_update")

	content = check_toml_integrity(CONFIG_FILE)

	if item_type == 0:
		# check if nickname exists
		nickname_exists = False
		for executor in content['executor']:
			# Find and update the executor
			if executor['name'] == nickname:
				nickname_exists = True
				executor["name"] = new_nickname
				executor["command"] = new_runner
				break

		new_nickname_exists = False
		for executor in content['executor']:
			# Find and update the executor
			if executor['name'] == new_nickname:
				new_nickname_exists = True
				break

		if not nickname_exists:
			print("ERROR: nickname not found")
			sys.exit(1)

		if new_nickname_exists:
			print("ERROR: new nickname already exists")
			sys.exit(1)

		# write content to file
		write_toml(CONFIG_FILE, content)

	elif item_type == 1:

		# check if executor exists
		executor_exists = False
		for exec in content['executor']:
			if exec['name'] == new_executor:
				executor_exists = True
				break

		if not executor_exists:
			print("ERROR: executor not found")
			print("Please create the executor first")
			sys.exit(1)

		# check if nickname exists
		nickname_exists = False
		for script in content['scripts']:
			# Find and update the script with the name of nickname arg
			if script['name'] == nickname:
				nickname_exists = True
				script["name"] = new_nickname
				script["path"] = new_path
				script["executor"] = new_executor
				break

		new_nickname_exists = False
		for script in content['scripts']:
			# Find and update the script with the name of nickname arg
			if script['name'] == new_nickname:
				new_nickname_exists = True
				break

		if not nickname_exists:
			print("ERROR: nickname not found")
			sys.exit(1)

		if new_nickname_exists:
			print("ERROR: new nickname already exists")
			sys.exit(1)

		# write content to file
		write_toml(CONFIG_FILE, content)



def command_delete(CONFIG_FILE, item_type, nickname):
	# print("function: command_delete")

	content = check_toml_integrity(CONFIG_FILE)

	if item_type == 0:

		# check if nickname exists
		nickname_exists = False
		for executor in content['executor']:
			if executor['name'] == nickname:
				nickname_exists = True
				break

		if not nickname_exists:
			print("ERROR: nickname not found")
			sys.exit(1)

		# Find and remove the script with the name of nickname arg
		for i, executor in enumerate(content["executor"]):
			if executor["name"] == nickname:
				del content["executor"][i]
				break

		# write content to file
		write_toml(CONFIG_FILE, content)

	elif item_type == 1:

		# check if nickname exists
		nickname_exists = False
		for script in content['scripts']:
			if script['name'] == nickname:
				nickname_exists = True
				break

		if not nickname_exists:
			print("ERROR: nickname not found")
			sys.exit(1)

		# Find and remove the script with the name of nickname arg
		for i, script in enumerate(content["scripts"]):
			if script["name"] == nickname:
				del content["scripts"][i]
				break

		# write content to file
		write_toml(CONFIG_FILE, content)


