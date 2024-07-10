import pytest
from clitemnestra.parser import parse_args


# Parser Tests Plan:

# > clitemnestra
# x clitemnestra <errorarg>

# > clitemnestra list
# > clitemnestra list <tag>
# x clitemnestra list <tag> <errortag>

# x clitemnestra search
# > clitemnestra search <term>
# x clitemnestra search <term> <errorarg>

# > clitemnestra edit
# x clitemnestra edit <errorarg>

# > clitemnestra config
# x clitemnestra config <errorarg>

# x clitemnestra exec
# > clitemnestra exec <nickname>
# x clitemnestra exec <nickname> <errorarg>

# > clitemnestra script
# x clitemnestra script <errorarg>

# x clitemnestra script create
# x clitemnestra script create <nickname>
# x clitemnestra script create <nickname> <path>
# > clitemnestra script create <nickname> <path> <executor>
# x clitemnestra script create <nickname> <path> <executor> <errorarg>

# x clitemnestra script read
# > clitemnestra script read <nickname>
# x clitemnestra script read <nickname> <errorarg>

# x clitemnestra script update
# x clitemnestra script update <nickname>
# x clitemnestra script update <nickname> <new_nickname>
# x clitemnestra script update <nickname> <new_nickname> <new_path>
# > clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
# x clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor> <errorarg>

# x clitemnestra script delete
# > clitemnestra script delete <nickname>
# x clitemnestra script delete <nickname> <errorarg>

# > clitemnestra executor
# x clitemnestra executor <errorarg>

# x clitemnestra executor create
# x clitemnestra executor create <nickname>
# > clitemnestra executor create <nickname> <command>
# x clitemnestra executor create <nickname> <command> <errorarg>

# x clitemnestra executor read
# > clitemnestra executor read <nickname>
# x clitemnestra executor read <nickname> <errorarg>

# x clitemnestra executor update
# x clitemnestra executor update <nickname>
# x clitemnestra executor update <nickname> <new_nickname>
# > clitemnestra executor update <nickname> <new_nickname> <new_command>
# x clitemnestra executor update <nickname> <new_nickname> <new_command> <errorarg>

# x clitemnestra executor delete
# > clitemnestra executor delete <nickname>
# x clitemnestra executor delete <nickname> <errorarg>



# Test Cases:

# > clitemnestra
def test_parser_none():
	parser = parse_args([])
	assert parser.command == None

# x clitemnestra <errorarg>
def test_parser_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["errorarg"])

# > clitemnestra list
def test_parser_list():
	parser = parse_args(["list"])
	assert parser.command == 'list' and parser.tag == None

# > clitemnestra list <tag>
def test_parser_list_tag():
	parser = parse_args(["list", "tag"])
	assert parser.command == 'list' and parser.tag == 'tag'

# x clitemnestra list <tag> <errortag>
def test_parser_list_tag_errortag():
	with pytest.raises(SystemExit):
		parse_args(["list", "tag", "errortag"])

# x clitemnestra search
def test_parser_search():
	with pytest.raises(SystemExit):
		parse_args(["search"])

# > clitemnestra search <term>
def test_parser_search_term():
	parser = parse_args(["search", "term"])
	assert parser.command == 'search' and parser.term == 'term'

# x clitemnestra search <term> <errorarg>
def test_parser_search_term_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["search", "term", "errorarg"])

# > clitemnestra edit
def test_parser_edit():
	parser = parse_args(["edit"])
	assert parser.command == 'edit'

# x clitemnestra edit <errorarg>
def test_parser_edit_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["edit", "errorarg"])

# > clitemnestra config
def test_parser_config():
	parser = parse_args(["config"])
	assert parser.command == 'config'

# x clitemnestra config <errorarg>
def test_parser_config_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["config", "errorarg"])

# x clitemnestra exec
def test_parser_exec():
	with pytest.raises(SystemExit):
		parse_args(["exec"])

# > clitemnestra exec <nickname>
def test_parser_exec_nickname():
	parser = parse_args(["exec", "nickname"])
	assert parser.command == 'exec' and parser.nickname == 'nickname'

# x clitemnestra exec <nickname> <errorarg>
def test_parser_exec_nickname_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["exec", "nickname", "errorarg"])

# > clitemnestra script
def test_parser_script():
	parser = parse_args(["script"])
	assert parser.command == 'script'

# x clitemnestra script <errorarg>
def test_parser_script_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["script", "errorarg"])

# x clitemnestra script create
def test_parser_script_create():
	with pytest.raises(SystemExit):
		parse_args(["script", "create"])

# x clitemnestra script create <nickname>
def test_parser_script_create_nickname():
	with pytest.raises(SystemExit):
		parse_args(["script", "create", "nickname"])

# x clitemnestra script create <nickname> <path>
def test_parser_script_create_nickname_path():
	with pytest.raises(SystemExit):
		parse_args(["script", "create", "nickname", "path"])

# > clitemnestra script create <nickname> <path> <executor>
def test_parser_script_create_nickname_path_executor():
	parser = parse_args(["script", "create", "nickname", "path", "executor"])
	assert (
		parser.command == 'script' and
		parser.script_command == 'create' and
		parser.nickname == 'nickname' and
		parser.path == 'path' and
		parser.executor == 'executor'
	)

# x clitemnestra script create <nickname> <path> <executor> <errorarg>
def test_parser_script_create_nickname_path_executor_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["script", "create", "nickname", "path", "executor", "errorarg"])

# x clitemnestra script read
def test_parser_script_read():
	with pytest.raises(SystemExit):
		parse_args(["script", "read"])

# > clitemnestra script read <nickname>
def test_parser_script_read_nickname():
	parser = parse_args(["script", "read", "nickname"])
	assert (
		parser.command == 'script' and
		parser.script_command == 'read' and
		parser.nickname == 'nickname'
	)

# x clitemnestra script read <nickname> <errorarg>
def test_parser_script_read_nickname_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["script", "read", "nickname", "errorarg"])

# x clitemnestra script update
def test_parser_script_update():
	with pytest.raises(SystemExit):
		parse_args(["script", "update"])

# x clitemnestra script update <nickname>
def test_parser_script_update_nickname():
	with pytest.raises(SystemExit):
		parse_args(["script", "update", "nickname"])

# x clitemnestra script update <nickname> <new_nickname>
def test_parser_script_update_nickname_new_nickname():
	with pytest.raises(SystemExit):
		parse_args(["script", "update", "nickname", "new_nickname"])

# x clitemnestra script update <nickname> <new_nickname> <new_path>
def test_parser_script_update_nickname_new_nickname_new_path():
	with pytest.raises(SystemExit):
		parse_args(["script", "update", "nickname", "new_nickname", "new_path"])

# > clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
def test_parser_script_update_nickname_new_nickname_new_path_new_executor():
	parser = parse_args(["script", "update", "nickname", "new_nickname", "new_path", "new_executor"])
	assert (
		parser.command == 'script' and
		parser.script_command == 'update' and
		parser.nickname == 'nickname' and
		parser.new_nickname == 'new_nickname' and
		parser.new_path == 'new_path' and
		parser.new_executor == 'new_executor'
	)

# x clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor> <errorarg>
def test_parser_script_update_nickname_new_nickname_new_path_new_executor_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["script", "update", "nickname", "new_nickname", "new_path", "new_executor", "errorarg"])

# x clitemnestra script delete
def test_parser_script_delete():
	with pytest.raises(SystemExit):
		parse_args(["script", "delete"])

# > clitemnestra script delete <nickname>
def test_parser_script_delete_nickname():
	parser = parse_args(["script", "delete", "nickname"])
	assert (
		parser.command == 'script' and
		parser.script_command == 'delete' and
		parser.nickname == 'nickname'
	)

# x clitemnestra script delete <nickname> <errorarg>
def test_parser_script_delete_nickname_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["script", "delete", "nickname", "errorarg"])

# > clitemnestra executor
def test_parser_executor():
	parser = parse_args(["executor"])
	assert parser.command == 'executor'

# x clitemnestra executor <errorarg>
def test_parser_executor_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["executor", "errorarg"])

# x clitemnestra executor create
def test_parser_executor_create():
	with pytest.raises(SystemExit):
		parse_args(["executor", "create"])

# x clitemnestra executor create <nickname>
def test_parser_executor_create_nickname():
	with pytest.raises(SystemExit):
		parse_args(["executor", "create", "nickname"])

# > clitemnestra executor create <nickname> <command>
def test_parser_executor_create_nickname_command():
	parser = parse_args(["executor", "create", "nickname", "command"])
	assert (
		parser.command == 'executor' and
		parser.executor_command == 'create' and
		parser.nickname == 'nickname' and
		parser.runner == 'command'
	)

# x clitemnestra executor create <nickname> <command> <errorarg>
def test_parser_executor_create_nickname_command_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["executor", "create", "nickname", "command", "errorarg"])

# x clitemnestra executor read
def test_parser_executor_read():
	with pytest.raises(SystemExit):
		parse_args(["executor", "read"])

# > clitemnestra executor read <nickname>
def test_parser_executor_read_nickname():
	parser = parse_args(["executor", "read", "nickname"])
	assert (
		parser.command == 'executor' and
		parser.executor_command == 'read' and
		parser.nickname == 'nickname'
	)

# x clitemnestra executor read <nickname> <errorarg>
def test_parser_executor_read_nickname_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["executor", "read", "nickname", "errorarg"])

# x clitemnestra executor update
def test_parser_executor_update():
	with pytest.raises(SystemExit):
		parse_args(["executor", "update"])

# x clitemnestra executor update <nickname>
def test_parser_executor_update_nickname():
	with pytest.raises(SystemExit):
		parse_args(["executor", "update", "nickname"])

# x clitemnestra executor update <nickname> <new_nickname>
def test_parser_executor_update_nickname_new_nickname():
	with pytest.raises(SystemExit):
		parse_args(["executor", "update", "nickname", "new_nickname"])

# > clitemnestra executor update <nickname> <new_nickname> <new_command>
def test_parser_executor_update_nickname_new_nickname_new_command():
	parser = parse_args(["executor", "update", "nickname", "new_nickname", "new_command"])
	assert (
		parser.command == 'executor' and
		parser.executor_command == 'update' and
		parser.nickname == 'nickname' and
		parser.new_nickname == 'new_nickname' and
		parser.new_runner == 'new_command'
	)

# x clitemnestra executor update <nickname> <new_nickname> <new_command> <errorarg>
def test_parser_executor_update_nickname_new_nickname_new_command_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["executor", "update", "nickname", "new_nickname", "new_command", "errorarg"])

# x clitemnestra executor delete
def test_parser_executor_delete():
	with pytest.raises(SystemExit):
		parse_args(["executor", "delete"])

# > clitemnestra executor delete <nickname>
def test_parser_executor_delete_nickname():
	parser = parse_args(["executor", "delete", "nickname"])
	assert (
		parser.command == 'executor' and
		parser.executor_command == 'delete' and
		parser.nickname == 'nickname'
	)

# x clitemnestra executor delete <nickname> <errorarg>
def test_parser_executor_delete_nickname_errorarg():
	with pytest.raises(SystemExit):
		parse_args(["executor", "delete", "nickname", "errorarg"])

# Done.