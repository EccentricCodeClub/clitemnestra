import pytest
from unittest.mock import mock_open, patch
from tomlkit import dumps

from clitemnestra.toml import check_syntax
from clitemnestra.toml import check_valid_keys
from clitemnestra.toml import check_toml_integrity
from clitemnestra.toml import read_toml
from clitemnestra.toml import write_toml

# TOML Tests Plan:

# check_toml_integrity(file_path):
# x check_toml_integrity pass error path
# x check_toml_integrity pass RIGHT path, error syntax
# x check_toml_integrity pass RIGHT path, RIGHT syntax, error keys
# v check_toml_integrity pass RIGHT path, RIGHT syntax, RIGHT keys

# read_toml(file_path):
# x read_toml error path
# v read_toml RIGHT path

# check_syntax(doc):
# v check_syntax empty syntax
# x check_syntax error syntax
# v check_syntax RIGHT syntax

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

# write_toml(CONFIG_FILE, content):
# x write_toml pass error path
# x write_toml pass RIGHT path, error keys
# v write_toml pass RIGHT path, RIGHT keys



# Test Cases:

# x check_toml_integrity pass error path
def test_check_toml_integrity_error_path():
	with pytest.raises(SystemExit):
		check_toml_integrity('invalid_path/file.toml')

# x check_toml_integrity pass RIGHT path, error syntax
def test_check_toml_integrity_right_path_error_syntax():
	with patch('clitemnestra.toml.read_toml') as m:
		m.return_value = 'error syntax'
		with pytest.raises(SystemExit):
			check_toml_integrity('right_path/file.toml')

# x check_toml_integrity pass RIGHT path, RIGHT syntax, error keys
def test_check_toml_integrity_right_path_right_syntax_error_keys():
	with patch('clitemnestra.toml.read_toml') as m:
		m.return_value = """
			# test toml text

			[config]
			editor = "fakeeditor"	# Fake Comment
			list_columns = true		# Fake Comment
			colorize = true			# Fake Comment
			debug = false			# Fake Comment

			[[scripts]]
			invalid_key = "error"
			invalid_key = "/path/to/script"

			[[executor]]
			name = "fakeexecutor"
			command = "exec"
			tags = []
		"""
		with pytest.raises(SystemExit):
			check_toml_integrity('right_path/file.toml')

# v check_toml_integrity pass RIGHT path, RIGHT syntax, RIGHT keys
def test_check_toml_integrity_right_path_right_syntax_right_keys():
	with patch('clitemnestra.toml.read_toml') as m:
		m.return_value = """
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
		"""
		check_toml_integrity('right_path/file.toml')

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

# v check_valid_keys empty scripts_keys, empty executor_keys
def test_check_valid_keys_empty_keys():
	check_valid_keys(
		{
			'scripts': [],
			'executor': []
		}
	)

# x check_valid_keys error scripts_keys, empty executor_keys
def test_check_valid_keys_error_scripts_keys():
	with pytest.raises(SystemExit):
		check_valid_keys(
			{
				'scripts': [{
					'invalid_key': 'error'
				}],
				'executor': []
			}
		)

# v check_valid_keys RIGHT scripts_keys, empty executor_keys
def test_check_valid_keys_right_scripts_keys():
	check_valid_keys(
		{
			'scripts': [{
				'name': 'valid_name',
				'path': 'valid_path',
				'executor': 'valid_executor',
				'tags': ['valid_tag1', 'valid_tag2']
			}],
			'executor': []
		}
	)

# x check_valid_keys empty scripts_keys, error executor_keys
def test_check_valid_keys_error_executor_keys():
	with pytest.raises(SystemExit):
		check_valid_keys(
			{
				'scripts': [],
				'executor': [{
					'invalid_key': 'error'
				}]
			}
		)

# x check_valid_keys error scripts_keys, error executor_keys
def test_check_valid_keys_error_scripts_executor_keys():
	with pytest.raises(SystemExit):
		check_valid_keys(
			{
				'scripts': [{
					'invalid_key': 'error'
				}],
				'executor': [{
					'invalid_key': 'error'
				}]
			}
		)

# x check_valid_keys RIGHT scripts_keys, error executor_keys
def test_check_valid_keys_right_scripts_error_executor_keys():
	with pytest.raises(SystemExit):
		check_valid_keys(
			{
				'scripts': [{
					'name': 'valid_name',
					'path': 'valid_path',
					'executor': 'valid_executor',
					'tags': ['valid_tag1', 'valid_tag2']
				}],
				'executor': [{
					'invalid_key': 'error'
				}]
			}
		)

# v check_valid_keys empty scripts_keys, RIGHT executor_keys
def test_check_valid_keys_empty_scripts_right_executor():
	check_valid_keys(
		{
			'scripts': [],
			'executor': [{
				'name': 'valid_name',
				'command': 'valid_command',
				'tags': ['valid_tag1', 'valid_tag2']
			}]
		}
	)

# x check_valid_keys error scripts_keys, RIGHT executor_keys
def test_check_valid_keys_error_scripts_right_executor():
	with pytest.raises(SystemExit):
		check_valid_keys(
			{
				'scripts': [{
					'invalid_key': 'error'
				}],
				'executor': [{
					'name': 'valid_name',
					'command': 'valid_command',
					'tags': ['valid_tag1', 'valid_tag2']
				}]
			}
		)

# v check_valid_keys RIGHT scripts_keys, RIGHT executor_keys
def test_check_valid_keys_right_scripts_right_executor():
	check_valid_keys(
		{
			'scripts': [{
				'name': 'valid_name',
				'path': 'valid_path',
				'executor': 'valid_executor',
				'tags': ['valid_tag1', 'valid_tag2']
			}],
			'executor': [{
				'name': 'valid_name',
				'command': 'valid_command',
				'tags': ['valid_tag1', 'valid_tag2']
			}]
		}
	)

# x write_toml pass error path
def test_write_toml_error_path():
	with pytest.raises(SystemExit):
		write_toml('invalid_path/file.toml', {})

# x write_toml pass RIGHT path, error keys
def test_write_toml_right_file_right_content_error_keys():
	data = {
		'scripts': [{
			'invalid_key': 'error'
		}],
		'executor': [{
			'invalid_key': 'error'
		}]
	}
	mock = mock_open()

	with pytest.raises(SystemExit):
		with patch('builtins.open', mock):
			write_toml('filename.toml', data)

# v write_toml pass RIGHT path, RIGHT keys
def test_write_toml_right_file_right_content_right_keys():
	data = {
		'config': { 'editor': "fakeeditor", 'list_columns': True, 'colorize': True, 'debug': False},
		'scripts': [ { 'name': "fakenameone", 'path': "/path/to/script", 'executor': "fakeexecutor", 'tags': ["fake1"]}],
		'executor': [ { 'name': "fakeexecutor", 'command': "exec", 'tags': [] }]
	}
	mock = mock_open()

	with patch('builtins.open', mock):
		write_toml('filename.toml', data)

		mock.assert_called_once_with('filename.toml', 'w')
		handle = mock()
		handle.write.assert_called_once_with(dumps(data))

# Done.