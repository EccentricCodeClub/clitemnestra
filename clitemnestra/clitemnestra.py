#! /usr/bin/env python3

import os
import sys

from tomlkit import nl, table
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text

from clitemnestra.parser import parse_args
from clitemnestra.toml import check_toml_integrity
from clitemnestra.toml import write_toml
from clitemnestra.info import info

# CONSTANTS
CONFIG_FILE_PATH = "clitemnestra/clitemnestra.toml"



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
		command_script(parser)
	elif parser.command == 'executor':
		command_executor(parser)
	else:
		info()



def command_exec(nickname):
	# print("function: command_exec")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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



def command_executor(parser):
	# print("function: command_executor")

	if parser.executor_command == 'create':
		command_executor_create(parser.nickname, parser.runner)
	elif parser.executor_command == 'read':
		command_executor_read(parser.nickname)
	elif parser.executor_command == 'update':
		command_executor_update(parser.nickname, parser.new_nickname, parser.new_runner)
	elif parser.executor_command == 'delete':
		command_executor_delete(parser.nickname)
	else:
		print("Invalid executor command")
		sys.exit(1)



def command_executor_create(nickname, runner):
	# print("function: command_executor_create")

	content = check_toml_integrity(CONFIG_FILE_PATH)

	# check if name already exists
	for executor in content['executor']:
		if executor['name'] == nickname:
			print("ERROR: name already exists")
			print("Please use a different name")
			sys.exit(1)

	executor = table()
	executor.add('name', nickname)
	executor.add('command', runner)
	executor.add('tags', [])
	executor.add(nl())

	content['executor'].append(executor)

	write_toml(CONFIG_FILE_PATH, content)



def command_executor_read(nickname):
	# print("function: command_executor_read")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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

	console = Console()

	table_executor = Table(title="Executor: " + nickname, show_lines=True, safe_box=True)
	table_executor.add_column("Variable", style="dodger_blue1", no_wrap=True)
	table_executor.add_column("Value", style="white")

	table_executor.add_row("Name", target['name'], style="bold cyan")
	table_executor.add_row("Command", target['command'], style="bold green")
	table_executor.add_row("Tags", '\n'.join(target['tags']), style="bold dodger_blue1")

	console.print(table_executor)



def command_executor_update(nickname, new_nickname, new_runner):
	# print("function: command_executor_update")
	
	content = check_toml_integrity(CONFIG_FILE_PATH)

	# check if nickname exists
	nickname_exists = False
	for executor in content['executor']:
		# Find and update the executor
		if executor['name'] == nickname:
			nickname_exists = True
			executor["name"] = new_nickname
			executor["command"] = new_runner
			break

	if not nickname_exists:
		print("ERROR: nickname not found")
		sys.exit(1)

	# write content to file
	write_toml(CONFIG_FILE_PATH, content)



def command_executor_delete(nickname):
	# print("function: command_executor_delete")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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
	write_toml(CONFIG_FILE_PATH, content)



def command_script(parser):
	# print("function: command_script")

	if parser.script_command == 'create':
		command_script_create(parser.nickname, parser.path, parser.executor)
	elif parser.script_command == 'read':
		command_script_read(parser.nickname)
	elif parser.script_command == 'update':
		command_script_update(parser.nickname, parser.new_nickname, parser.new_path, parser.new_executor)
	elif parser.script_command == 'delete':
		command_script_delete(parser.nickname)
	else:
		print("Invalid script command")
		sys.exit(1)



def command_script_create(nickname, path, executor):
	# print("function: command_script_create")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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

	script = table()
	script.add('name', nickname)
	script.add('path', path)
	script.add('executor', executor)
	script.add('tags', [])
	script.add(nl())

	content['scripts'].append(script)

	write_toml(CONFIG_FILE_PATH, content)



def command_script_read(nickname):
	# print("function: command_script_read")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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

	console = Console()

	table_script = Table(title="Script: " + nickname, show_lines=True, safe_box=True)
	table_script.add_column("Variable", style="dodger_blue1", no_wrap=True)
	table_script.add_column("Value", style="white")

	# table_config.add_row("Name", "[bright_red]" + str(content['config'][items]))
	table_script.add_row("Name", target['name'], style="bold cyan")
	table_script.add_row("Path", target['path'], style="bold magenta")
	table_script.add_row("Executor", target['executor'], style="bold green")

	for items in content['executor']:
		if items['name'] == target['executor']:
			table_script.add_row("Executor Command", items['command'], style="green")
			table_script.add_row("Executor Tags", '\n'.join(items['tags']), style="dodger_blue2")

			execution = items['command'] + " " + target['path']

			break

	table_script.add_row("Script Tags", '\n'.join(target['tags']), style="bold dodger_blue1")

	console.print(table_script)

	if execution is not None:
		print()
		execution = Text(execution)
		execution.stylize("bold gold1")
		console.print(Columns(["Execution command looks like this:", execution]))
		print()



def command_script_update(nickname, new_nickname, new_path, new_executor):
	# print("function: command_script_update")
	
	content = check_toml_integrity(CONFIG_FILE_PATH)

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

	if not nickname_exists:
		print("ERROR: nickname not found")
		sys.exit(1)

	# write content to file
	write_toml(CONFIG_FILE_PATH, content)



def command_script_delete(nickname):
	# print("function: command_script_delete")

	content = check_toml_integrity(CONFIG_FILE_PATH)

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
	write_toml(CONFIG_FILE_PATH, content)



def command_edit():
	# print("function: command_edit")
	# common editors: nano, neovim, vim, vi, emacs, gedit, code

	content = check_toml_integrity(CONFIG_FILE_PATH)

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
			os.system(f"{editor} {CONFIG_FILE_PATH}")
		except Exception as e:
			print("ERROR: editor error")
			print(e)
			sys.exit(1)



def command_config():
	# print("function: command_config")

	content = check_toml_integrity(CONFIG_FILE_PATH)

	console = Console()

	table_config = Table(title="Config File", show_lines=True, safe_box=True)
	table_config.add_column("Variable", style="dodger_blue1", no_wrap=True)
	table_config.add_column("Value", style="white")

	try:
		for items in content['config']:
			if content['config'][items] is False:
				table_config.add_row(items, "[bright_red]" + str(content['config'][items]))
			elif content['config'][items] is True:
				table_config.add_row(items, "[bright_green]" + str(content['config'][items]))
			else:
				table_config.add_row(items, str(content['config'][items]))
	except Exception as e:
		print("No config found")
		sys.exit(1)

	console.print(table_config)



def command_search(term):
	# print("function: command_search")

	content = check_toml_integrity(CONFIG_FILE_PATH)

	console = Console()

	table_script = Table(title="Scripts", show_lines=True, safe_box=True)
	table_script.add_column("Name", style="cyan", no_wrap=True)
	table_script.add_column("Path", style="magenta")
	table_script.add_column("Executor", style="green")
	table_script.add_column("Tag", style="dodger_blue1")

	table_executor = Table(title="Executors", show_lines=True, safe_box=True)
	table_executor.add_column("Name", style="cyan", no_wrap=True)
	table_executor.add_column("Command", style="green")
	table_executor.add_column("Tag", style="dodger_blue1")

	try:
		for script in content['scripts']:
			flatten_script = set(flatten(script))
			for item in flatten_script:
				if term in item:
					table_script.add_row(script['name'], script['path'], script['executor'], '\n'.join(script['tags']))
					break
	except Exception as e:
		print("No scripts found")

	try:
		for executor in content['executor']:
			flatten_executor = set(flatten(executor))
			for item in flatten_executor:
				if term in item:
					table_executor.add_row(executor['name'], executor['command'], '\n'.join(executor['tags']))
					break
	except Exception as e:
		print("No executors found")

	console.print(Columns([table_script, table_executor]))



def command_list(tag):
	# print("function: command_list")

	content = check_toml_integrity(CONFIG_FILE_PATH)

	console = Console()

	table_script = Table(title="Scripts", show_lines=True, safe_box=True)
	table_script.add_column("Name", style="cyan", no_wrap=True)
	table_script.add_column("Path", style="magenta")
	table_script.add_column("Executor", style="green")
	table_script.add_column("Tag", style="dodger_blue1")

	table_executor = Table(title="Executors", show_lines=True, safe_box=True)
	table_executor.add_column("Name", style="cyan", no_wrap=True)
	table_executor.add_column("Command", style="green")
	table_executor.add_column("Tag", style="dodger_blue1")

	if tag:
		print(f"Filtering by tag: {tag}\n")

	try:
		for script in content['scripts']:
			if tag is None or tag in script['tags']:
				table_script.add_row(script['name'], script['path'], script['executor'], '\n'.join(script['tags']))
	except Exception as e:
		print("No scripts found")

	try:
		for executor in content['executor']:
			if tag is None or tag in executor['tags']:
				table_executor.add_row(executor['name'], executor['command'], '\n'.join(executor['tags']))
	except Exception as e:
		print("No executors found")

	console.print(Columns([table_script, table_executor]))



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
