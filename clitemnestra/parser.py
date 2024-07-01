import argparse
import sys

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
