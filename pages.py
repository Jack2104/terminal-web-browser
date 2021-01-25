import config
import os

from abc import ABC, abstractmethod


class BasePage(ABC):
    def __init__(self):
        self.sublinks = []

    @classmethod
    def display(cls, add_to_local_history=True):
        """
        Renders the page contents and omnibar.

        Arguments:
            add_to_local_history {bool} -- determines if the page will be
            added to local_history
        """
        # Windows and Unix clear the screen in different ways
        os.system('cls' if os.name == 'nt' else 'clear')

        print(cls.get_contents())

        # Create an infinite loop so that input is prompted infinitely
        is_invalid = False
        has_shown_commands = False

        while True:
            omni_prompt = "(invalid) > " if is_invalid else "> "
            omni_query = input(omni_prompt)

            oq_split = omni_query.split()
            command_count = len(oq_split)
            first_command = omni_query_split[0]

            if first_command in ["-h", "--home"] and command_count == 1:
                # Go home
                pass
            elif first_command in ["-l", "--link"] and command_count == 2 and oq_split[1].isnumeric():
                # Follow link
                pass
            elif first_command in ["-c", "--commands"] and command_count == 1:
                if not has_shown_commands:
                    # move cursor above omnibar
                    print(config.commands)
                    continue
                else:
                    continue
            elif omni_query.startswith("http") and command_count == 1:
                # Go to url
                pass
            elif not omni_query.isspace() and not omni_query == "":
                # Search omniquery
                pass
            else:
                is_invalid == True

            if is_invalid:
                continue

    @abstractmethod
    def get_contents(self):
        pass


class HomePage(BasePage):
    pass


class ResultsPage(BasePage):
    pass


class WebPage(BasePage):
    pass


class HistoryPage(BasePage):
    pass
