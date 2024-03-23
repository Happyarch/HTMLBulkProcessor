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
import curses

# Function to display file contents and line numbers


def display_file(window, html_string, start_line, end_line, start_col):
    # Display line numbers
    for i, line_num in enumerate(range(start_line, end_line), 1):
        window.addstr(i, 1, f"{line_num + 1} ")

    # Display file contents with horizontal scrolling
    max_cols = window.getmaxyx()[1] - 5
    for i, line in enumerate(html_string.splitlines()[start_line:end_line], 1):
        truncated_line = line.rstrip()[start_col:start_col+max_cols]
        window.addstr(i, 5, truncated_line)

# Function to draw the text box for user input


def draw_text_box(window, text_box_y, text_box_x, textbox_state, numeral_entry_textbox):
    textbox_messages = {
        0: "Lines to be removed, ranges are accepted e.g 1-5 (space separated): ",
        1: "Lines to partition across, see --help for more details (space separated): ",
        2: "Preview mode (press ENTER to continue):"
    }
    message = textbox_messages.get(
        textbox_state, "Invalid textbox_state value")
    window.addstr(text_box_y, text_box_x, f"{message}")
    window.addstr(text_box_y + 1, text_box_x, numeral_entry_textbox)

# Function to handle key presses


def handle_key(window, key, html_string, start_line, end_line, start_col, numeral_entry_textbox, textbox_state):
    # Handle key presses for navigation
    if key == curses.KEY_DOWN and end_line < len(html_string.splitlines()):
        start_line += 1
        end_line += 1
    elif key == curses.KEY_UP and start_line > 0:
        start_line -= 1
        end_line -= 1
    elif key == curses.KEY_RIGHT:
        start_col += 1
    elif key == curses.KEY_LEFT and start_col > 0:
        start_col -= 1

    # Handle backspace to delete characters from the entry textbox
    elif key == curses.KEY_BACKSPACE:
        numeral_entry_textbox = numeral_entry_textbox[:-1]

    # Handle key presses for entering numbers or spaces based on the textbox state
    elif textbox_state == 0 and (key == ord(' ') or key == ord('-') or (ord('0') <= key <= ord('9'))):
        numeral_entry_textbox += chr(key)
    elif textbox_state == 1 and (ord('0') <= key <= ord('9') or key == ord(' ')):
        numeral_entry_textbox += chr(key)

    # Handle invalid textbox states
    elif textbox_state not in [0, 1, 2]:  # Only 0, 1, and 2 are valid states
        print("Error: Invalid textbox state.")
        return None, None, None, numeral_entry_textbox, False

    # Handle Enter key to submit the entry textbox value
    elif key == curses.KEY_ENTER or key == 10:
        return None, None, None, numeral_entry_textbox, False

    return start_line, end_line, start_col, numeral_entry_textbox, True

# Main function to run the text-based user interface


def run_tui(textbox_state, line_operator_pipeline_stage):
    def run_curses_interface(stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        stdscr.clear()
        stdscr.refresh()

        html_string = line_operator_pipeline_stage

        # Adjusted to leave 3 lines at the bottom
        max_lines = stdscr.getmaxyx()[0] - 4
        start_line, end_line = 0, min(max_lines, len(html_string.splitlines()))
        start_col = 0
        text_box_y, text_box_x = stdscr.getmaxyx()[0] - 3, 1
        numeral_entry_textbox = ""

        while True:
            stdscr.clear()
            stdscr.border(0)

            display_file(stdscr, html_string, start_line, end_line, start_col)
            draw_text_box(stdscr, text_box_y, text_box_x,
                          textbox_state, numeral_entry_textbox)

            stdscr.refresh()

            key = stdscr.getch()
            result = handle_key(stdscr, key, html_string, start_line,
                                end_line, start_col, numeral_entry_textbox, textbox_state)
            if result is None:
                break
            else:
                start_line, end_line, start_col, numeral_entry_textbox, continue_loop = result
                if not continue_loop:
                    break

        # Return the final value of numeral_entry_textbox
        return numeral_entry_textbox

    # Run the interface and return the final value of numeral_entry_textbox
    return curses.wrapper(run_curses_interface)
