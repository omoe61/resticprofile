'''
Display messages to the console
'''
import time
from colorama import Fore, init
from resticprofile import constants
from resticprofile.help import get_options_help


class Console:
    def __init__(self, quiet=False, verbose=False):
        '''
        Display messages to the console
        '''
        self.quiet = quiet
        self.verbose = verbose
        init(autoreset=True)

    def _msg(self, message):
        '''
        Low level display message
        '''
        print(time.asctime(), message)

    def debug(self, message):
        '''
        Display debug message to the console
        '''
        if self.verbose:
            self._msg(Fore.LIGHTGREEN_EX + message)

    def info(self, message):
        '''
        Display info message to the console
        '''
        if not self.quiet:
            self._msg(Fore.LIGHTYELLOW_EX + message)

    def warning(self, message):
        '''
        Display warning message to the console
        '''
        self._msg(Fore.LIGHTRED_EX + message)

    def error(self, message):
        '''
        Display error message to the console
        '''
        self._msg(Fore.LIGHTRED_EX + message)

    def usage(self, name):
        '''
        Display usage to the console
        '''
        print("\nUsage:")
        print(" " + name + "\n   " + "\n   ".join(get_options_help(constants.ARGUMENTS_DEFINITION)))
        print("   [restic command] [additional parameters to pass to restic]\n")
