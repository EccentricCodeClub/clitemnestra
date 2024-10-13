#! /usr/bin/env python3

import os
import sys

from clitemnestra.parser import parse_args

from clitemnestra.toml import check_toml_integrity

from clitemnestra.info import info

from clitemnestra.rich import rich_list_search
from clitemnestra.rich import rich_config

from clitemnestra.crud import command_executor
from clitemnestra.crud import command_script

# CONSTANTS
CONFIG_FILE = "clitemnestra/clitemnestra.toml"



def main():
	# print("function: main")

	input_args = sys.argv[1:]

	parser = parse_args(input_args)

	if parser.command == 'list':
		command_list(parser.tag)
	elif parser.command == 'search':
		command_search(parser.term)
	elif parser.command == 'edit':
		command_edit()
	elif parser.command == 'config':
		command_config()
	elif parser.command == 'exec':
		command_exec(parser.nickname)
	elif parser.command == 'script':
		command_script(CONFIG_FILE, parser)
	elif parser.command == 'executor':
		command_executor(CONFIG_FILE, parser)
	else:
		info()



def command_exec(nickname):
	# print("function: command_exec")

	content = check_toml_integrity(CONFIG_FILE)

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

	for items in content['executor']:
		if items['name'] == target['executor']:
			execution = items['command'] + " " + target['path']
			break

	if execution is not None:
		print(f"Executing: {execution}")
		try:
			os.system(execution)
		except Exception as e:
			print("ERROR: execution error")
			print(e)
			sys.exit(1)
	else:
		print("ERROR: executor not found")
		sys.exit(1)



def command_edit():
	# print("function: command_edit")
	# common editors: nano, neovim, vim, vi, emacs, gedit, code

	content = check_toml_integrity(CONFIG_FILE)

	editor = None
	# detect the editor of configuration file
	try:
		editor = content['config']['editor']
		print(f"Editor: {editor}")
	except Exception as e:
		print("No config found")
		print(e)
		sys.exit(1)

	if editor is None:
		print("Editor not found in config file")
		sys.exit(1)
	else:
		try:
			os.system(f"{editor} {CONFIG_FILE}")
		except Exception as e:
			print("ERROR: editor error")
			print(e)
			sys.exit(1)



def command_config():
	# print("function: command_config")

	content = check_toml_integrity(CONFIG_FILE)

	matrix_config = []

	try:
		for items in content['config']:
			matrix_config.append([items, content['config'][items]])
	except Exception as e:
		print("No config found")
		sys.exit(1)

	rich_config(matrix_config)



def command_search(term):
	# print("function: command_search")

	content = check_toml_integrity(CONFIG_FILE)

	matrix_scripts = []
	matrix_executors = []

	try:
		for script in content['scripts']:
			flatten_script = set(flatten(script))
			for item in flatten_script:
				if term in item:
					matrix_scripts.append([script['name'], script['path'], script['executor'], '\n'.join(script['tags'])])
					
					break
	except Exception as e:
		print("No scripts found")

	try:
		for executor in content['executor']:
			flatten_executor = set(flatten(executor))
			for item in flatten_executor:
				if term in item:
					matrix_executors.append([executor['name'], executor['command'], '\n'.join(executor['tags'])])
					break
	except Exception as e:
		print("No executors found")

	rich_list_search(matrix_scripts, matrix_executors, columns=True)



def command_list(tag):
	# print("function: command_list")

	content = check_toml_integrity(CONFIG_FILE)

	matrix_scripts = []
	matrix_executors = []

	if tag:
		print(f"Filtering by tag: {tag}\n")

	try:
		for script in content['scripts']:
			if tag is None or tag in script['tags']:
				matrix_scripts.append([script['name'], script['path'], script['executor'], '\n'.join(script['tags'])])
	except Exception as e:
		print("No scripts found")

	try:
		for executor in content['executor']:
			if tag is None or tag in executor['tags']:
				matrix_executors.append([executor['name'], executor['command'], '\n'.join(executor['tags'])])
	except Exception as e:
		print("No executors found")

	rich_list_search(matrix_scripts, matrix_executors, columns=True)



def flatten(obj):
	# print("function: flatten")

	if isinstance(obj, dict):
		for val in obj.values():
			yield from flatten(val)
	elif isinstance(obj, list):
		for val in obj:
			yield from flatten(val)
	else:
		yield obj



if __name__ == "__main__":
	main()
