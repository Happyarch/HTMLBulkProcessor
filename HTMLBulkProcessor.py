# HTMLBulkProcessor
# Copyright (C) 2024  Matthew L. Frazier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import argparse
import platform
from HTMLCleaner import html_cleaner
from HTMLLineRemover import remove_lines
from HTMLPartitioner import line_partitioner
from HTMLProcessorTUI import run_tui
# Checking for Windows to activate Windows bodges.
is_windows = (platform.system() == 'Windows')
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process some files.')

# Add an argument for the input file path
parser.add_argument('input_file', help='Path to the input file')

# Parse the command-line arguments
args = parser.parse_args()

# Use the input file specified by the user
with open(args.input_file, 'r') as file:
    # Read the HTML content from the input file
    html_content = file.read()

# Clean the HTML content
cleaned_text = html_cleaner(html_content)

# Get user input for line removal
numeral_entry_textbox = run_tui(0, is_windows, cleaned_text)

# Remove specified lines
removed_lines = remove_lines(cleaned_text, numeral_entry_textbox)

# Get user input for line partitioning
numeral_entry_textbox = run_tui(1, is_windows, removed_lines)

# Partition the lines based on user input
line_partitioner(removed_lines, numeral_entry_textbox, args.input_file)

# Clear the screen
os.system('clear' if not is_windows else 'cls')

# Print a goodbye message
print("Goodbye!")
