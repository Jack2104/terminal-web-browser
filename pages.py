import config
import os
import pages
import requests
import sys

from abc import ABC, abstractmethod


class BasePage(ABC):
    def __init__(self):
        self.sublinks = []

    @classmethod
    def display(cls, add_to_history=True):
        """
        Renders the page contents and omnibar.

        Arguments:
            add_to_local_history {bool} -- determines if the page will be
            added to local_history
        """
        # Windows and Unix clear the screen in different ways
        os.system('cls' if os.name == 'nt' else 'clear')

        print(cls.get_contents())
        print()
        print()
        print()

        is_current = config.local_history_view_idex != len(
            config.local_history)

        try:
            is_self = config.local_history[config.local_history_view_idex] != cls
        except IndexError:
            # config.local_history is empty (happens on first run or when history is cleared)
            is_self = False

        if add_to_history and is_current and not is_self:
            config.history.append(cls)
            config.local_history = config.local_history[:config.local_history_view_idex]
            config.local_history.append(cls)

        # Create an infinite loop so that input is prompted infinitely
        is_invalid = False
        has_shown_commands = False

        while True:
            sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K")

            omni_prompt = "(invalid) > " if is_invalid else "> "
            omni_query = input(omni_prompt)

            if omni_query.isspace() or omni_query == "":
                is_invalid = True
                continue

            oq_split = omni_query.split()
            command_count = len(oq_split)
            first_command = oq_split[0]

            if first_command in ["-h", "--home"] and command_count == 1:
                new_page = pages.HomePage()
            elif first_command in ["-l", "--link"] and command_count == 2 and oq_split[1].isnumeric() and sublinks:
                sublink_index = oq_split[1] - 1
                new_page = pages.WebPage(sublinks[sublink_index])
            elif first_command in ["-c", "--commands"] and command_count == 1:
                if not has_shown_commands:
                    # Moves up one line, thendeletes the input field
                    sys.stdout.write("\x1b[1A")
                    sys.stdout.write("\x1b[2K")
                    is_invalid = False
                    has_shown_commands = True

                    # print()
                    print(config.commands)
                    continue
                else:
                    continue
            elif omni_query.startswith("http") and command_count == 1:
                new_page = WebPage(omni_query)
            elif omni_query[0] != "-":
                new_page = ResultsPage(omni_query)
            else:
                is_invalid = True
                continue

    @abstractmethod
    def get_contents(self):
        pass


class HomePage(BasePage):
    def get_contents():
        # TODO: read this text from a text file
        home_text = """
  ______          _       __    ______    ____ 
 /_  __/         | |     / /   / ____/   / __ )
  / /    ______  | | /| / /   / __/     / __  |
 / /    /_____/  | |/ |/ /   / /___    / /_/ / 
/_/              |__/|__/   /_____/   /_____/  
A simple terminal browser

Begin browsing by searching below
Type -c or --commands for some help
For more information, type -a or --about"""
        twidth = os.get_terminal_size()[0]
        home_text = "\n".join(line.center(twidth)
                              for line in home_text.split("\n"))
        return home_text


class ResultsPage(BasePage):
    def __init__(self, search_terms):
        self.search_terms = search_terms

    def get_contents(self):
        pass


class WebPage(BasePage):
    def __init__(self, url):
        self.url = url


class HistoryPage(BasePage):
    def get_contents():
        pass
