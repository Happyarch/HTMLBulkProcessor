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
def parse_lines_to_remove(lines_to_remove):
    # Parse the lines to remove and sort them
    return sorted(lines_to_remove.split(), key=lambda x: (int(x.split('-')[0]), int(x.split('-')[-1] if '-' in x else x)))


def remove_lines(input_string, lines_to_remove):
    # Function to process a range of lines for removal
    def process_range(start, end):
        # Remove lines in the specified range
        for i in range(start, end + 1):
            # Check for duplicate removals
            if i in lines_to_remove_set and i not in lines_to_remove_duplicates:
                lines_to_remove_duplicates.add(i)
            lines_to_remove_set.add(i)
        del lines[start - 1:end]

    # Split the input string into lines
    lines = input_string.split('\n')
    # Initialize sets to keep track of lines to remove and duplicates
    lines_to_remove_set = set()
    lines_to_remove_duplicates = set()

    # Iterate over lines to remove, in reverse order for correct removal
    for line_to_remove in parse_lines_to_remove(lines_to_remove)[::-1]:
        if '-' in line_to_remove:
            # Process a range of lines
            start, end = map(int, line_to_remove.split('-'))
            if start > end:
                start, end = end, start  # Swap start and end if start > end
            process_range(start, end)
        else:
            # Process a single line
            line_num = int(line_to_remove)
            if line_num in lines_to_remove_set and line_num not in lines_to_remove_duplicates:
                lines_to_remove_duplicates.add(line_num)
            lines_to_remove_set.add(line_num)
            del lines[line_num - 1]

    if lines_to_remove_duplicates:
        # Raise an error if there are duplicate removals
        raise ValueError(
            f"Lines {', '.join(map(str, lines_to_remove_duplicates))} are included in the set of lines to be removed multiple times.")

    # Join the remaining lines and return the modified string
    return '\n'.join(lines)
