#################################
# Create a simpe table object
#################################
import fpms.modules.wlanpi_oled as oled
from textwrap import wrap

from fpms.modules.pages.display import *
from fpms.modules.pages.utils import *
from fpms.modules.themes import THEME
from fpms.modules.constants import (
    STATUS_BAR_HEIGHT,
    SMART_FONT,
    FONT11,
    MAX_TABLE_LINES,
)

class SimpleTable(object):

    def __init__(self, g_vars):

        # grab a screeb obj
        self.display_obj = Display(g_vars)
        self.draw = g_vars['draw']
        self.string_formatter = StringFormatter()

    def display_simple_table(self, g_vars, item_list, title='', justify=True):
        '''
        This function takes a list and paints each entry as a line on a
        page. It also displays appropriate up/down scroll buttons if the
        entries passed exceed a page length (one line at a time)
        '''

        g_vars['drawing_in_progress'] = True
        g_vars['display_state'] = 'page'

        # Clear display prior to painting new item
        self.display_obj.clear_display(g_vars)

        y = 0
        x = 0
        padding = 2
        font_offset = 2
        font_type = SMART_FONT
        font_size = 11
        item_length_max = 21
        table_display_max = MAX_TABLE_LINES + 1

        # write title if present
        if title != '':
            g_vars['draw'].rectangle((x, y, PAGE_WIDTH, STATUS_BAR_HEIGHT), fill=THEME.simple_table_title_background.value)
            g_vars['draw'].text((x + padding, y + font_offset), title.center(item_length_max,
                                                               " "),  font=font_type, fill=THEME.simple_table_title_foreground.value)
            font_offset += font_size + padding + padding
            table_display_max -= 1

        previous_table_list_length = g_vars['table_list_length']
        g_vars['table_list_length'] = len(item_list)

        # if table length changes, reset current scroll selection
        # e.g. when showing lldp table info and eth cable
        # pulled so list size changes
        if g_vars['table_list_length'] != previous_table_list_length:
            g_vars['current_scroll_selection'] = 0

        # if we're going to scroll of the end of the list, adjust pointer
        if g_vars['current_scroll_selection'] + table_display_max > g_vars['table_list_length']:
            g_vars['current_scroll_selection'] -= 1

        # modify list to display if scrolling required
        if g_vars['table_list_length'] > table_display_max:

            table_bottom_entry = g_vars['current_scroll_selection'] + table_display_max
            item_list = item_list[g_vars['current_scroll_selection']: table_bottom_entry]

        for item in item_list:

            if len(item) > item_length_max:
                item = item[0:item_length_max]

            if justify:
                item = self.string_formatter.justify(item, width=item_length_max)

            self.draw.text((x + padding, y + font_offset), item,
                            font=font_type, fill=THEME.simple_table_row_foreground.value)

            font_offset += font_size

        oled.drawImage(g_vars['image'])

        g_vars['display_state'] = 'page'
        g_vars['drawing_in_progress'] = False

        return