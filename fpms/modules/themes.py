# -*- coding: utf-8 -*-
#
"""
themes.py - display themes
"""

from enum import Enum
from fpms.modules.env_utils import EnvUtils

env_util = EnvUtils()
PLATFORM = env_util.get_platform()

class BlackAndWhiteTheme(Enum):
    display_background            = "black"
    text_color                    = "white"
    text_secondary_color          = "white"
    text_tertiary_color           = "white"
    text_highlighted_color        = "white"
    status_bar_foreground         = "black"
    status_bar_background         = "white"
    status_bar_battery_low        = "white"
    status_bar_battery_full       = "white"
    system_bar_foreground         = "black"
    system_bar_background         = "white"
    page_title_background         = "white"
    page_title_foreground         = "black"
    page_item_foreground          = "white"
    page_item_background          = "black"
    page_nav_item_foreground      = "white"
    page_nav_indicator_foreground = "white"
    page_selected_item_foreground = "black"
    page_selected_item_background = "white"
    page_table_title_foreground   = "black"
    page_table_title_background   = "white"
    page_table_row_foreground     = "white"
    page_table_row_background     = "black"
    page_table_row_separator      = "white"
    simple_table_title_foreground = "black"
    simple_table_title_background = "white"
    simple_table_row_foreground   = "white"
    simple_table_row_background   = "black"
    alert_info_title_foreground   = "black"
    alert_info_title_background   = "white"
    alert_error_title_foreground  = "black"
    alert_error_title_background  = "white"
    alert_message_foreground      = "white"
    alert_popup_foreground        = "white"
    alert_popup_background        = "black"

class LightTheme(Enum):
    display_background            = "#e4e2e0"
    text_color                    = "#323a45"
    text_secondary_color          = "#5b616b"
    text_tertiary_color           = "#4773aa"
    text_highlighted_color        = "#0071bc"
    status_bar_foreground         = "white"
    status_bar_background         = "#0071bc"
    status_bar_battery_low        = "#fdb81e"
    status_bar_battery_full       = "#94bfa2"
    system_bar_foreground         = "white"
    system_bar_background         = "#5b616b"
    page_title_foreground         = "white"
    page_title_background         = "#205493"
    page_item_foreground          = "#323a45"
    page_item_background          = "#e4e2e0"
    page_nav_item_foreground      = "#205493"
    page_nav_indicator_foreground = "#205493"
    page_selected_item_foreground = "#323a45"
    page_selected_item_background = "#f9c642"
    page_table_title_foreground   = "#323a45"
    page_table_title_background   = "#f9c642"
    page_table_row_foreground     = "#323a45"
    page_table_row_background     = "#e4e2e0"
    page_table_row_separator      = "gray"
    simple_table_title_foreground = "#323a45"
    simple_table_title_background = "#f9c642"
    simple_table_row_foreground   = "#323a45"
    simple_table_row_background   = "#e4e2e0"
    alert_info_title_foreground   = "white"
    alert_info_title_background   = "#2e8540"
    alert_error_title_foreground  = "white"
    alert_error_title_background  = "#cd2026"
    alert_message_foreground      = "#323a45"
    alert_popup_foreground        = "white"
    alert_popup_background        = "#323a45"

class DarkTheme(Enum):
    display_background            = "black"
    text_color                    = "white"
    text_secondary_color          = "#aeb0b5"
    text_tertiary_color           = "#4773aa"
    text_highlighted_color        = "#f9c642"
    status_bar_foreground         = "white"
    status_bar_background         = "#0071bc"
    status_bar_battery_low        = "#fdb81e"
    status_bar_battery_full       = "#94bfa2"
    system_bar_foreground         = "#aeb0b5"
    system_bar_background         = "#323a45"
    page_title_foreground         = "white"
    page_title_background         = "#205493"
    page_item_foreground          = "white"
    page_item_background          = "black"
    page_nav_item_foreground      = "#939499"
    page_nav_indicator_foreground = "#4773aa"
    page_selected_item_foreground = "black"
    page_selected_item_background = "#f9c642"
    page_table_title_foreground   = "black"
    page_table_title_background   = "#f9c642"
    page_table_row_foreground     = "white"
    page_table_row_background     = "black"
    page_table_row_separator      = "#205493"
    simple_table_title_foreground = "black"
    simple_table_title_background = "#f9c642"
    simple_table_row_foreground   = "white"
    simple_table_row_background   = "black"
    alert_info_title_foreground   = "white"
    alert_info_title_background   = "#2e8540"
    alert_error_title_foreground  = "white"
    alert_error_title_background  = "#cd2026"
    alert_message_foreground      = "white"
    alert_popup_foreground        = "white"
    alert_popup_background        = "#5b616b"

if PLATFORM == "pro":
    THEME = DarkTheme
else:
    THEME = BlackAndWhiteTheme
