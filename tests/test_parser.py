import pytest
import clitemnestra.clitemnestra

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
# x clitemnestra executor create <tag>
# > clitemnestra executor create <tag> <command>
# x clitemnestra executor create <tag> <command> <errorarg>

# x clitemnestra executor read
# > clitemnestra executor read <tag>
# x clitemnestra executor read <tag> <errorarg>

# x clitemnestra executor update
# x clitemnestra executor update <tag>
# x clitemnestra executor update <tag> <new_tag>
# > clitemnestra executor update <tag> <new_tag> <new_command>
# x clitemnestra executor update <tag> <new_tag> <new_command> <errorarg>

# x clitemnestra executor delete
# > clitemnestra executor delete <tag>
# x clitemnestra executor delete <tag> <errorarg>



# Test Cases:

# > clitemnestra
def test_parser_none():
	parser = clitemnestra.clitemnestra.parse_args([])
	assert parser.command is None

# x clitemnestra <errorarg>
def test_parser_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["errorarg"])

# > clitemnestra list
def test_parser_list():
	parser = clitemnestra.clitemnestra.parse_args(["list"])
	assert parser.command is 'list' and parser.tag is None

# > clitemnestra list <tag>
def test_parser_list_tag():
	parser = clitemnestra.clitemnestra.parse_args(["list", "tag"])
	assert parser.command is 'list' and parser.tag is 'tag'

# x clitemnestra list <tag> <errortag>
def test_parser_list_tag_errortag():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["list", "tag", "errortag"])

# x clitemnestra search
def test_parser_search():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["search"])

# > clitemnestra search <term>
def test_parser_search_term():
	parser = clitemnestra.clitemnestra.parse_args(["search", "term"])
	assert parser.command is 'search' and parser.term is 'term'

# x clitemnestra search <term> <errorarg>
def test_parser_search_term_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["search", "term", "errorarg"])

# > clitemnestra edit
def test_parser_edit():
	parser = clitemnestra.clitemnestra.parse_args(["edit"])
	assert parser.command is 'edit'

# x clitemnestra edit <errorarg>
def test_parser_edit_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["edit", "errorarg"])

# > clitemnestra config
def test_parser_config():
	parser = clitemnestra.clitemnestra.parse_args(["config"])
	assert parser.command is 'config'

# x clitemnestra config <errorarg>
def test_parser_config_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["config", "errorarg"])

# x clitemnestra exec
def test_parser_exec():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["exec"])

# > clitemnestra exec <nickname>
def test_parser_exec_nickname():
	parser = clitemnestra.clitemnestra.parse_args(["exec", "nickname"])
	assert parser.command is 'exec' and parser.nickname is 'nickname'

# x clitemnestra exec <nickname> <errorarg>
def test_parser_exec_nickname_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["exec", "nickname", "errorarg"])

# > clitemnestra script
def test_parser_script():
	parser = clitemnestra.clitemnestra.parse_args(["script"])
	assert parser.command is 'script'

# x clitemnestra script <errorarg>
def test_parser_script_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "errorarg"])

# x clitemnestra script create
def test_parser_script_create():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "create"])

# x clitemnestra script create <nickname>
def test_parser_script_create_nickname():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "create", "nickname"])

# x clitemnestra script create <nickname> <path>
def test_parser_script_create_nickname_path():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "create", "nickname", "path"])

# > clitemnestra script create <nickname> <path> <executor>
def test_parser_script_create_nickname_path_executor():
	parser = clitemnestra.clitemnestra.parse_args(["script", "create", "nickname", "path", "executor"])
	assert (
		parser.command is 'script' and
		parser.script_command is 'create' and
		parser.nickname is 'nickname' and
		parser.path is 'path' and
		parser.executor is 'executor'
	)

# x clitemnestra script create <nickname> <path> <executor> <errorarg>
def test_parser_script_create_nickname_path_executor_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "create", "nickname", "path", "executor", "errorarg"])

# x clitemnestra script read
def test_parser_script_read():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "read"])

# > clitemnestra script read <nickname>
def test_parser_script_read_nickname():
	parser = clitemnestra.clitemnestra.parse_args(["script", "read", "nickname"])
	assert (
		parser.command is 'script' and
		parser.script_command is 'read' and
		parser.nickname is 'nickname'
	)

# x clitemnestra script read <nickname> <errorarg>
def test_parser_script_read_nickname_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "read", "nickname", "errorarg"])

# x clitemnestra script update
def test_parser_script_update():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "update"])

# x clitemnestra script update <nickname>
def test_parser_script_update_nickname():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "update", "nickname"])

# x clitemnestra script update <nickname> <new_nickname>
def test_parser_script_update_nickname_new_nickname():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "update", "nickname", "new_nickname"])

# x clitemnestra script update <nickname> <new_nickname> <new_path>
def test_parser_script_update_nickname_new_nickname_new_path():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "update", "nickname", "new_nickname", "new_path"])

# > clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor>
def test_parser_script_update_nickname_new_nickname_new_path_new_executor():
	parser = clitemnestra.clitemnestra.parse_args(["script", "update", "nickname", "new_nickname", "new_path", "new_executor"])
	assert (
		parser.command is 'script' and
		parser.script_command is 'update' and
		parser.nickname is 'nickname' and
		parser.new_nickname is 'new_nickname' and
		parser.new_path is 'new_path' and
		parser.new_executor is 'new_executor'
	)

# x clitemnestra script update <nickname> <new_nickname> <new_path> <new_executor> <errorarg>
def test_parser_script_update_nickname_new_nickname_new_path_new_executor_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "update", "nickname", "new_nickname", "new_path", "new_executor", "errorarg"])

# x clitemnestra script delete
def test_parser_script_delete():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "delete"])

# > clitemnestra script delete <nickname>
def test_parser_script_delete_nickname():
	parser = clitemnestra.clitemnestra.parse_args(["script", "delete", "nickname"])
	assert (
		parser.command is 'script' and
		parser.script_command is 'delete' and
		parser.nickname is 'nickname'
	)

# x clitemnestra script delete <nickname> <errorarg>
def test_parser_script_delete_nickname_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["script", "delete", "nickname", "errorarg"])

# > clitemnestra executor
def test_parser_executor():
	parser = clitemnestra.clitemnestra.parse_args(["executor"])
	assert parser.command is 'executor'

# x clitemnestra executor <errorarg>
def test_parser_executor_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "errorarg"])

# x clitemnestra executor create
def test_parser_executor_create():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "create"])

# x clitemnestra executor create <tag>
def test_parser_executor_create_tag():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "create", "tag"])

# > clitemnestra executor create <tag> <command>
def test_parser_executor_create_tag_command():
	parser = clitemnestra.clitemnestra.parse_args(["executor", "create", "tag", "command"])
	assert (
		parser.command is 'executor' and
		parser.executor_command is 'create' and
		parser.tag is 'tag' and
		parser.runner is 'command'
	)

# x clitemnestra executor create <tag> <command> <errorarg>
def test_parser_executor_create_tag_command_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "create", "tag", "command", "errorarg"])

# x clitemnestra executor read
def test_parser_executor_read():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "read"])

# > clitemnestra executor read <tag>
def test_parser_executor_read_tag():
	parser = clitemnestra.clitemnestra.parse_args(["executor", "read", "tag"])
	assert (
		parser.command is 'executor' and
		parser.executor_command is 'read' and
		parser.tag is 'tag'
	)

# x clitemnestra executor read <tag> <errorarg>
def test_parser_executor_read_tag_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "read", "tag", "errorarg"])

# x clitemnestra executor update
def test_parser_executor_update():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "update"])

# x clitemnestra executor update <tag>
def test_parser_executor_update_tag():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "update", "tag"])

# x clitemnestra executor update <tag> <new_tag>
def test_parser_executor_update_tag_new_tag():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "update", "tag", "new_tag"])

# > clitemnestra executor update <tag> <new_tag> <new_command>
def test_parser_executor_update_tag_new_tag_new_command():
	parser = clitemnestra.clitemnestra.parse_args(["executor", "update", "tag", "new_tag", "new_command"])
	assert (
		parser.command is 'executor' and
		parser.executor_command is 'update' and
		parser.tag is 'tag' and
		parser.new_tag is 'new_tag' and
		parser.new_runner is 'new_command'
	)

# x clitemnestra executor update <tag> <new_tag> <new_command> <errorarg>
def test_parser_executor_update_tag_new_tag_new_command_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "update", "tag", "new_tag", "new_command", "errorarg"])

# x clitemnestra executor delete
def test_parser_executor_delete():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "delete"])

# > clitemnestra executor delete <tag>
def test_parser_executor_delete_tag():
	parser = clitemnestra.clitemnestra.parse_args(["executor", "delete", "tag"])
	assert (
		parser.command is 'executor' and
		parser.executor_command is 'delete' and
		parser.tag is 'tag'
	)

# x clitemnestra executor delete <tag> <errorarg>
def test_parser_executor_delete_tag_errorarg():
	with pytest.raises(SystemExit):
		clitemnestra.clitemnestra.parse_args(["executor", "delete", "tag", "errorarg"])

# Done.