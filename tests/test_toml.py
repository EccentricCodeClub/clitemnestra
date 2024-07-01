import pytest
import clitemnestra.clitemnestra

# TOML Tests Plan:

# check_toml_integrity(file_path)
# x pass wrong path
# x pass RIGHT path, wrong syntax
# x pass RIGHT file, RIGHT syntax
# x pass RIGHT file, RIGHT syntax, toml scripts wrong keys
# x pass RIGHT file, RIGHT syntax, toml scripts RIGHT keys, executors wrong keys
# v pass RIGHT file, RIGHT syntax, toml scripts RIGHT keys, executors RIGHT keys

# write_toml(CONFIG_FILE_PATH, content)
# x pass wrong path
# x pass RIGHT path, wrong content syntax
# x pass RIGHT path, wrong content syntax
# x pass RIGHT file, RIGHT content syntax, toml scripts wrong keys
# x pass RIGHT file, RIGHT content syntax, toml scripts RIGHT keys, executors wrong keys
# v pass RIGHT file, RIGHT content syntax, toml scripts RIGHT keys, executors RIGHT keys

