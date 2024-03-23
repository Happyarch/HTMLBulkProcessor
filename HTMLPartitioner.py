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


def get_output_path_from_config():
    config_file = 'HTMLBulkProcessor.config'
    if not os.path.exists(config_file) or os.stat(config_file).st_size == 0:
        # If the config file doesn't exist or is empty, use the current working directory
        return os.getcwd()

    output_path = None
    with open(config_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue  # Skip comments

            key, value = line.strip().split(',')
            if key.strip() == 'output_path':
                output_path = value.strip()
                break

    if output_path is None:
        # Output path not found, use the current working directory
        return os.getcwd()

    if not os.path.isabs(output_path):
        raise ValueError(
            "Output path in config file must be an absolute path.")

    return output_path


def line_partitioner(input_string, line_numbers, input_file):
    # Convert line_numbers to a list of integers
    line_numbers = list(map(int, line_numbers.split()))

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Get the output path from the config file
    output_path = get_output_path_from_config()

    # Create the output folder
    output_folder = os.path.join(output_path, file_name)
    os.makedirs(output_folder, exist_ok=True)

    lines = input_string.split('\n')
    # Add a dummy line at the beginning to simplify indexing
    lines.insert(0, '')

    for i in range(1, len(line_numbers)):
        start_line = line_numbers[i-1]
        end_line = line_numbers[i]

        # Create the output file name with integer prefix
        output_file = os.path.join(output_folder, f"{i}_{file_name}.txt")

        # Check if the output file already exists
        if os.path.exists(output_file):
            raise FileExistsError(
                f"Output file '{output_file}' already exists.")

        # Write the segment to the output file
        with open(output_file, 'w') as out_f:
            out_f.writelines(lines[start_line:end_line])

    # Process the last line number
    last_start_line = line_numbers[-1]
    last_output_file = os.path.join(
        output_folder, f"{len(line_numbers)}_{file_name}.txt")

    # Check if the last output file already exists
    if os.path.exists(last_output_file):
        raise FileExistsError(
            f"Output file '{last_output_file}' already exists.")

    with open(last_output_file, 'w') as out_f:
        out_f.writelines(lines[last_start_line:])
