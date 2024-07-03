import pytest
from unittest.mock import mock_open, patch

from clitemnestra.toml import check_syntax
from clitemnestra.toml import check_valid_keys
from clitemnestra.toml import check_toml_integrity
from clitemnestra.toml import read_toml
from clitemnestra.toml import write_toml

# TOML Tests Plan:

# read_toml(file_path):
# x read_toml error path
# v read_toml RIGHT path

# check_syntax(doc):
# v check_syntax empty syntax
# x check_syntax error syntax
# v check_syntax RIGHT syntax

# ^^^^ Done / TO DO vvvv

# check_valid_keys(content):
# v check_valid_keys empty scripts_keys, empty executor_keys
# x check_valid_keys error scripts_keys, empty executor_keys
# v check_valid_keys RIGHT scripts_keys, empty executor_keys
# x check_valid_keys empty scripts_keys, error executor_keys
# x check_valid_keys error scripts_keys, error executor_keys
# x check_valid_keys RIGHT scripts_keys, error executor_keys
# v check_valid_keys empty scripts_keys, RIGHT executor_keys
# x check_valid_keys error scripts_keys, RIGHT executor_keys
# v check_valid_keys RIGHT scripts_keys, RIGHT executor_keys

# check_toml_integrity(file_path):
# x pass error path
# x pass RIGHT path, error syntax
# x pass RIGHT file, RIGHT syntax
# x pass RIGHT file, RIGHT syntax, toml scripts error keys
# x pass RIGHT file, RIGHT syntax, toml scripts RIGHT keys, executors error keys
# v pass RIGHT file, RIGHT syntax, toml scripts RIGHT keys, executors RIGHT keys

# write_toml(CONFIG_FILE_PATH, content):
# x pass error path
# x pass RIGHT path, error content syntax
# x pass RIGHT path, error content syntax
# x pass RIGHT file, RIGHT content syntax, toml scripts error keys
# x pass RIGHT file, RIGHT content syntax, toml scripts RIGHT keys, executors error keys
# v pass RIGHT file, RIGHT content syntax, toml scripts RIGHT keys, executors RIGHT keys



# x read_toml error path
def test_read_toml_error_path():
	with pytest.raises(SystemExit):
		read_toml('invalid_path/file.toml')

# v read_toml RIGHT path
def test_read_toml_right_path():
	# using mock file
	with patch('builtins.open', mock_open(read_data='content')) as m:
		assert read_toml('right_path/file.toml') == 'content'
		m.assert_called_once_with('right_path/file.toml', 'r')

# v check_syntax empty syntax
def test_check_syntax_empty_syntax():
	assert check_syntax('') == {}

# x check_syntax error syntax
def test_check_syntax_error_syntax():
	with pytest.raises(SystemExit):
		check_syntax('error syntax')

# v check_syntax RIGHT syntax
def test_check_syntax_right_syntax():
	assert check_syntax("""
		# test toml text

		[config]
		editor = "fakeeditor"	# Fake Comment
		list_columns = true		# Fake Comment
		colorize = true			# Fake Comment
		debug = false			# Fake Comment

		[[scripts]]
		name = "fakenameone"
		path = "/path/to/script"
		executor = "fakeexecutor"
		tags = ["fake1"]

		[[executor]]
		name = "fakeexecutor"
		command = "exec"
		tags = []

		""") == {
			'config': { 'editor': "fakeeditor", 'list_columns': True, 'colorize': True, 'debug': False},
			'scripts': [ { 'name': "fakenameone", 'path': "/path/to/script", 'executor': "fakeexecutor", 'tags': ["fake1"]}],
			'executor': [ { 'name': "fakeexecutor", 'command': "exec", 'tags': [] }]
		}




