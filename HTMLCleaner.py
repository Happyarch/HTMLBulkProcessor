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
from bs4 import BeautifulSoup
import re

# Strips content of HTML symbols


def remove_html_tags_with_bs(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Get the text without HTML tags
    text_only = soup.get_text()

    return text_only

# Strips content of other undesireable characters


def html_cleaner(html_content):

    # Process the HTML content
    preprocessed_data = remove_html_tags_with_bs(html_content)

    nbsp_processing = re.sub(
        r'(&nbsp;|&#160;|&#xA0;|\u00A0)', ' ', preprocessed_data)
    newline_processing = re.sub(r'\n{2,}', '\n', nbsp_processing)

    # Store the modified data in a variable
    cleaned_text = newline_processing

    return cleaned_text
