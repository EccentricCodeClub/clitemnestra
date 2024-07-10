import sys

from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.text import Text



def rich_list_search(matrix_scripts, matrix_executors, columns):
	# print("function: rich_list_search")

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
		for line in matrix_scripts:
			table_script.add_row(line[0], line[1], line[2], line[3])
	except Exception as e:
		print(e)
		sys.exit(1)

	try:
		for line in matrix_executors:
			table_executor.add_row(line[0], line[1], line[2])
	except Exception as e:
		print(e)
		sys.exit(1)

	if columns:
		console.print(Columns([table_script, table_executor]))
	else:
		console.print(table_script)
		console.print(table_executor)



def rich_config(matrix_config):
	# print("function: rich_config")

	console = Console()

	table_config = Table(title="Config File", show_lines=True, safe_box=True)
	table_config.add_column("Variable", style="dodger_blue1", no_wrap=True)
	table_config.add_column("Value", style="white")

	try:
		for line in matrix_config:
			if line[1] == False:
				table_config.add_row(line[0], "[bright_red]" + str(line[1]))
			elif line[1] == True:
				table_config.add_row(line[0], "[bright_green]" + str(line[1]))
			else:
				table_config.add_row(line[0], str(line[1]))
	except Exception as e:
		print(e)
		sys.exit(1)

	console.print(table_config)

