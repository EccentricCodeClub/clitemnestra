#! /usr/bin/env python3

import argparse
import os
import random
import sys

from tomlkit import nl, table
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text

from clitemnestra.toml import check_toml_integrity
from clitemnestra.toml import write_toml

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
		default_info()



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



def default_info():
	# print("function: default_info")

	data = [
		"Clitemnestra",
		"Version: -",
		"",
		"Script management tool for helping you to organize and execute your code.",
		"Usage: clitemnestra <command> [<args>]",
		"",
		"Commands:",
		"  list <tag>      List scripts",
		"  search <term>   Search records by term",
		"  edit            Edit configuration file",
		"  config          Show configuration",
		"  exec <nickname> Execute a script",
		"  script          Manage scripts",
		"  executor        Manage executors",
		"  help            Show this message",
	]

	# Get the list of files in the assets folder
	assets_folder = "clitemnestra/assets"
	files = os.listdir(assets_folder)

	# Pick a random file from the list
	random_file = random.choice(files)

	# Open the random file and read its contents
	with open(os.path.join(assets_folder, random_file), "r") as f:
		logo = f.read()

	display = Table(
		show_header=False,
		box=None,
		safe_box=True
	)

	console = Console()

	display.add_column("Logo", style="bright_white", vertical='middle')
	display.add_column("Info", style="white", vertical='middle')
	display.add_row(Text.from_ansi(logo), '\n'.join(data))
	console.print(display)



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



def parse_args(args):
	# print("function: parse_args")

	parser = argparse.ArgumentParser(
		prog='clitemnestra',
		description='script management',
		exit_on_error=False
	)
	subparsers = parser.add_subparsers(dest='command')

	# > clitemnestra
	# 	> clitemnestra list
	# 		> clitemnestra list <tag>
	# 	> clitemnestra search <term>
	# 	> clitemnestra edit
	# 	> clitemnestra config
	# 	> clitemnestra exec <nickname>
	# 	> clitemnestra script
	# 		> clitemnestra script create <nickname> <path> <executor>
	# 		> clitemnestra script read <nickname>
	# 		> clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
	# 		> clitemnestra script delete <nickname>
	# 	> clitemnestra executor
	# 		> clitemnestra executor create <nickname> <command>
	# 		> clitemnestra executor read <nickname>
	# 		> clitemnestra executor update <nickname> <new_nickname> <new_command>
	# 		> clitemnestra executor delete <nickname>

	# > clitemnestra list <tag?>
	list_parser = subparsers.add_parser('list', help='list scripts')
	list_parser.add_argument('tag', nargs='?', type=str, help='filter by tag')

	# > clitemnestra search <term>
	search_parser = subparsers.add_parser('search', help='search records by term')
	search_parser.add_argument('term', type=str, help='term for search')

	# > clitemnestra edit
	edit_parser = subparsers.add_parser('edit', help='edit configuration file')

	# > clitemnestra config
	config_parser = subparsers.add_parser('config', help='show configuration')

	# > clitemnestra exec <nickname>
	exec_parser = subparsers.add_parser('exec', help='execute a script')
	exec_parser.add_argument('nickname', type=str, help='nickname of the script')


	# create script command
	script_parser = subparsers.add_parser('script', help='manage scripts')
	script_subparsers = script_parser.add_subparsers(dest='script_command')

	# > clitemnestra script create <nickname> <path> <executor>
	create_script_parser = script_subparsers.add_parser('create', help='create a new script')
	create_script_parser.add_argument('nickname', type=str, help='nickname for the script')
	create_script_parser.add_argument('path', type=str, help='path to the script')
	create_script_parser.add_argument('executor', type=str, help='executor for the script')

	# > clitemnestra script read <nickname>
	read_script_parser = script_subparsers.add_parser('read', help='read a script')
	read_script_parser.add_argument('nickname', type=str, help='nickname of the script')

	# > clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
	update_script_parser = script_subparsers.add_parser('update', help='update a script')
	update_script_parser.add_argument('nickname', type=str, help='nickname of the script')
	update_script_parser.add_argument('new_nickname', type=str, help='new nickname for the script')
	update_script_parser.add_argument('new_path', type=str, help='new path to the script')
	update_script_parser.add_argument('new_executor', type=str, help='new executor for the script')

	# > clitemnestra script delete <nickname>
	delete_script_parser = script_subparsers.add_parser('delete', help='delete a script')
	delete_script_parser.add_argument('nickname', type=str, help='nickname of the script')


	# create executor command
	executor_parser = subparsers.add_parser('executor', help='manage executors')
	executor_subparsers = executor_parser.add_subparsers(dest='executor_command')

	# > clitemnestra executor create <nickname> <runner>
	create_executor_parser = executor_subparsers.add_parser('create', help='create a new executor')
	create_executor_parser.add_argument('nickname', type=str, help='nickname for the executor')
	create_executor_parser.add_argument('runner', type=str, help='command for the executor')

	# > clitemnestra executor read <nickname>
	read_executor_parser = executor_subparsers.add_parser('read', help='read a executor')
	read_executor_parser.add_argument('nickname', type=str, help='nickname of the executor')

	# > clitemnestra executor update <nickname> <new_nickname> <new_runner>
	update_executor_parser = executor_subparsers.add_parser('update', help='update a executor')
	update_executor_parser.add_argument('nickname', type=str, help='nickname of the executor')
	update_executor_parser.add_argument('new_nickname', type=str, help='new nickname for the executor')
	update_executor_parser.add_argument('new_runner', type=str, help='new command for the executor')

	# > clitemnestra executor delete <nickname>
	delete_executor_parser = executor_subparsers.add_parser('delete', help='delete a executor')
	delete_executor_parser.add_argument('nickname', type=str, help='nickname of the executor')

	try:
		parsed_args = parser.parse_args(args)
	except argparse.ArgumentError as e:
		print("ERROR: argparse.ArgumentError")
		print(e)
		sys.exit(1)
	except argparse.ArgumentTypeError as e:
		print("ERROR: argparse.ArgumentTypeError")
		print(e)
		sys.exit(1)
	except Exception as e:
		print("ERROR: General Exception")
		print(e)
		sys.exit(1)

	return parsed_args



if __name__ == "__main__":
	main()
