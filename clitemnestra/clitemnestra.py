# #! /usr/bin/env python3

import argparse
import sys

def main():
	print("function: main")

	print(f"sys.argv: {sys.argv}")

	parser = parse_args(sys.argv[1:])

	print(f"parser: {parser}")





def parse_args(args):
	print("function: parse_args")

	parser = argparse.ArgumentParser(description='script management')
	subparsers = parser.add_subparsers(dest='command')

	# > clitemnestra
	# 	> clitemnestra list
	# 		> clitemnestra list <tag>
	# 	> clitemnestra search <nickname>
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
	list_parser = subparsers.add_parser('list', help='List scripts')
	list_parser.add_argument('tag', nargs='?', type=str, help='Filter by tag')

	# > clitemnestra search <nickname>
	search_parser = subparsers.add_parser('search', help='Search for a script')
	search_parser.add_argument('nickname', type=str, help='Nickname of the script')

	# > clitemnestra edit
	edit_parser = subparsers.add_parser('edit', help='Edit a script')

	# > clitemnestra config
	config_parser = subparsers.add_parser('config', help='Manage configuration')

	# > clitemnestra exec <nickname>
	exec_parser = subparsers.add_parser('exec', help='Execute a script')
	exec_parser.add_argument('nickname', type=str, help='Nickname of the script')


	# Create script command
	script_parser = subparsers.add_parser('script', help='Manage scripts')
	script_subparsers = script_parser.add_subparsers(dest='script_command')

	# > clitemnestra script create <nickname> <path> <executor>
	create_script_parser = script_subparsers.add_parser('create', help='Create a new script')
	create_script_parser.add_argument('nickname', type=str, help='Nickname for the script')
	create_script_parser.add_argument('path', type=str, help='Path to the script')
	create_script_parser.add_argument('executor', type=str, help='Executor for the script')

	# > clitemnestra script read <nickname>
	read_script_parser = script_subparsers.add_parser('read', help='Read a script')
	read_script_parser.add_argument('nickname', type=str, help='Nickname of the script')

	# > clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
	update_script_parser = script_subparsers.add_parser('update', help='Update a script')
	update_script_parser.add_argument('nickname', type=str, help='Nickname of the script')
	update_script_parser.add_argument('new_nickname', type=str, help='New nickname for the script')
	update_script_parser.add_argument('new_path', type=str, help='New path to the script')
	update_script_parser.add_argument('new_executor', type=str, help='New executor for the script')

	# > clitemnestra script delete <nickname>
	delete_script_parser = script_subparsers.add_parser('delete', help='Delete a script')
	delete_script_parser.add_argument('nickname', type=str, help='Nickname of the script')


	# Create executor command
	executor_parser = subparsers.add_parser('executor', help='Manage executors')
	executor_subparsers = executor_parser.add_subparsers(dest='executor_command')

	# > clitemnestra executor create <tag> <command>
	create_executor_parser = executor_subparsers.add_parser('create', help='Create a new executor')
	create_executor_parser.add_argument('tag', type=str, help='Tag for the executor')
	create_executor_parser.add_argument('runner', type=str, help='Command for the executor')

	# > clitemnestra executor read <tag>
	read_executor_parser = executor_subparsers.add_parser('read', help='Read a executor')
	read_executor_parser.add_argument('tag', type=str, help='Tag of the executor')

	# > clitemnestra executor update <tag> <new_tag> <new_command>
	update_executor_parser = executor_subparsers.add_parser('update', help='Update a executor')
	update_executor_parser.add_argument('tag', type=str, help='Tag of the executor')
	update_executor_parser.add_argument('new_tag', type=str, help='New tag for the executor')
	update_executor_parser.add_argument('new_runner', type=str, help='New command for the executor')

	# > clitemnestra executor delete <tag>
	delete_executor_parser = executor_subparsers.add_parser('delete', help='Delete a executor')
	delete_executor_parser.add_argument('tag', type=str, help='Tag of the executor')

	return parser.parse_args(args)


if __name__ == "__main__":
	main()
