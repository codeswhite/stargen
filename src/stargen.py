
from pathlib import Path
from argparse import Namespace
from random import choice

from utils import pr, cyan, cprint, banner

from src.generic_loop import generic_loop
from src.modules import *


def clear() -> None:
    print(chr(27) + "[2J")


class Stargen:
    DEFAULT_CONFIG_PATH = Path.cwd() / 'config.json'
    DEFAULT_CONFIG_SETUP = {
        'workspace': str(Path.cwd().joinpath('dicts').resolve()),
        'comb': {
            'subdir': 'comb',
            'len_min': 5,
            'len_max': 12,
            'complex_min': 0,
            'complex_max': 100,
        },
        'crunch': {
            'subdir': 'crunch'
        },
        'down': {
            'subdir': 'down',
            'dict_url': 'http://ftp.funet.fi/pub/unix/security/passwd/crack/dictionaries/'
        }
    }

    def __init__(self, args: Namespace):
        # Initialize modules
        self.config = Config(
            args.config if args.config else Stargen.DEFAULT_CONFIG_PATH,
            Stargen.DEFAULT_CONFIG_SETUP)
        self.keywords = Keyword()
        self.crunch = Crunch(self)
        self.downloads = Download(self)
        self.combinations = Combination(self)
        
        # Welcoming message
        cprint(banner('Stargen'), choice(('red', 'green', 'blue')))
        pr(f'Enter "{cyan("help")}" to see list of available commands,\n' +
               '    enter blank to exit from current menu')

        # Enter main menu
        try:
            generic_loop('stargen', {
                # 'conf': self.config.menu(),
                'kwd': self.keywords.menu(),
                'crun': self.crunch.menu(),
                'down': self.downloads.menu(),
                'comb': self.combinations.menu()
                # 'craft': (self.craft, 'Craft a wordlist from the current setup')
            })
        except (KeyboardInterrupt, EOFError):
            print()
            pr('\nInterrupted!', '!')
        finally:
            self.config.save()

    # def craft(self, *args):
    #     pass
