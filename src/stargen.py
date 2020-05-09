
from pathlib import Path
from argparse import Namespace
from random import choice

from utils import pr, cyan, cprint, banner, generic_menu_loop

from src.modules import *


class Stargen:
    DEFAULT_CONFIG_PATH = Path.cwd() / 'config.json'
    DEFAULT_CONFIG_SETUP = {
        'workspace': str(Path.cwd().joinpath('dicts').resolve()),
        'modules': {
            'kwd': {
                'list_treshold': 50
            },
            'down': {
                'dict_url': 'http://ftp.funet.fi/pub/unix/security/passwd/crack/dictionaries/'
            },
            'crunch': {
            },
            'comb': {
                'len_min': 5,
                'len_max': 12,
                'complex_min': 0,
                'complex_max': 100,
            }
        }
    }

    def __init__(self, args: Namespace):
        # Initialize modules
        self.config = Config(
            args.config if args.config else Stargen.DEFAULT_CONFIG_PATH,
            Stargen.DEFAULT_CONFIG_SETUP)
        self.keywords = Keyword(self)
        self.crunch = Crunch(self)
        self.downloads = Download(self)
        self.combinations = Combination(self)

        # Welcoming message
        cprint(banner('Stargen'), choice(('red', 'green', 'blue')))
        pr(f'Enter "{cyan("help")}" to see list of available commands,\n' +
           '    enter blank to exit from current menu', '?')

        # Enter main menu
        try:
            generic_menu_loop('stargen', {
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
