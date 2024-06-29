# #! /usr/bin/env python3

import argparse
import sys
import tomlkit
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
import random
import os
from rich.text import Text

# CONSTANTS
CONFIG_FILE_PATH = "clitemnestra/clitemnestra.toml"


def main():
	print("function: main")

	input_args = sys.argv[1:]

	parser = parse_args(input_args)

	if parser.command == 'list':		# Done
		command_list(parser.tag)
	elif parser.command == 'search':	# Done
		command_search(parser.term)
	elif parser.command == 'edit':
		print("Under Construction")
	elif parser.command == 'config':	# WIP
		print("Under Construction")
	elif parser.command == 'exec':
		print("Under Construction")
	elif parser.command == 'script':
		print("Under Construction")
	elif parser.command == 'executor':
		print("Under Construction")
	else:
		# print("Invalid command")
		# sys.exit(1)
		default_info()

def default_info():
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
		"  config          Manage configuration",
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
	print("function: command_search")

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
	print("function: command_list")

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
	if isinstance(obj, dict):
		for val in obj.values():
			yield from flatten(val)
	elif isinstance(obj, list):
		for val in obj:
			yield from flatten(val)
	else:
		yield obj



def check_toml_integrity(file_path):
	print("function: check_toml_integrity")

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
		doc = tomlkit.parse(content)
	except tomlkit.exceptions.TOMLKitError as e:
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



def parse_args(args):
	print("function: parse_args")

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
	# 		> clitemnestra executor create <tag> <command>
	# 		> clitemnestra executor read <tag>
	# 		> clitemnestra executor update <tag> <new_tag> <new_command>
	# 		> clitemnestra executor delete <tag>

	# > clitemnestra list <tag?>
	list_parser = subparsers.add_parser('list', help='list scripts')
	list_parser.add_argument('tag', nargs='?', type=str, help='filter by tag')

	# > clitemnestra search <term>
	search_parser = subparsers.add_parser('search', help='search records by term')
	search_parser.add_argument('term', type=str, help='term for search')

	# > clitemnestra edit
	edit_parser = subparsers.add_parser('edit', help='edit configuration file')

	# > clitemnestra config
	config_parser = subparsers.add_parser('config', help='manage configuration')

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

	# > clitemnestra executor create <tag> <command>
	create_executor_parser = executor_subparsers.add_parser('create', help='create a new executor')
	create_executor_parser.add_argument('tag', type=str, help='tag for the executor')
	create_executor_parser.add_argument('runner', type=str, help='command for the executor')

	# > clitemnestra executor read <tag>
	read_executor_parser = executor_subparsers.add_parser('read', help='read a executor')
	read_executor_parser.add_argument('tag', type=str, help='tag of the executor')

	# > clitemnestra executor update <tag> <new_tag> <new_command>
	update_executor_parser = executor_subparsers.add_parser('update', help='update a executor')
	update_executor_parser.add_argument('tag', type=str, help='tag of the executor')
	update_executor_parser.add_argument('new_tag', type=str, help='new tag for the executor')
	update_executor_parser.add_argument('new_runner', type=str, help='new command for the executor')

	# > clitemnestra executor delete <tag>
	delete_executor_parser = executor_subparsers.add_parser('delete', help='delete a executor')
	delete_executor_parser.add_argument('tag', type=str, help='tag of the executor')

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
