import os
import random

from rich.console import Console
from rich.table import Table
from rich.text import Text

def info():
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

