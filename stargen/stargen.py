
from pathlib import Path
from argparse import Namespace
from random import choice

from stargen import modules

from termcolor import cprint, colored
from interutils import pr, cyan, banner, choose_file, pause, DictConfig


class Stargen:
    DEFAULT_CONFIG_PATH = Path.home().joinpath('.config', 'stargen.json')
    DEFAULT_CONFIG_SETUP = {
        'workspace': str(Path.home().joinpath('dicts').resolve()),
        'prompt': '[ stargen ]> ',
        'modules': {
            'kwd': {
                'list_treshold': 50
            },
            'down': {
                'dict_url': 'http://ftp.funet.fi/pub/unix/security/passwd/crack/dictionaries/'
            },
            'crun': {
            },
            'comb': {
                'max_created_file_size': 5 * 1024**3,  # 5 GB
                'len_min': 5,
                'len_max': 12,
                'complex_min': 0,
                'complex_max': 100,
            }
        }
    }

    def __init__(self, args: Namespace):
        # Load config
        self.config = DictConfig(
            args.config if args.config else Stargen.DEFAULT_CONFIG_PATH,
            Stargen.DEFAULT_CONFIG_SETUP)

        # Create workspace dir
        self.workspace = Path(self.config['workspace'])
        Path(self.workspace).mkdir(exist_ok=True)

        # Initialize modules
        self.modules = (
            modules.Keyword(self),
            modules.Crunch(self),
            modules.Download(self),
            modules.Combination(self)
        )
        # Initialize menu
        menu = {}
        for mod in self.modules:
            mod: modules.Module
            menu.update(mod.menu())

        # Welcoming message & enter main menu
        cprint(banner('Stargen'), choice(('red', 'green', 'blue')))
        pr(f'Enter "{cyan("help")}" to see list of available commands,\n' +
           '    [Ctrl + C] to exit', '?')
        while 1:
            try:
                # Get user input
                inp = input(
                    colored(self.config['prompt'], 'red', attrs=['bold']))

                if not inp:
                    continue

                # Help the user
                if 'help' in inp:
                    for k, v in menu.items():
                        print(f'  {cyan(k)} -> {colored(v[1], "yellow")}')
                    continue

                # Get command
                pts = inp.split(' ')
                cmd = pts[0]
                if cmd not in menu:
                    pr(f'No such command! try "{cyan("help")}".', '!')
                    continue

                # Call menu entry
                menu.get(cmd)[0](tuple([i for i in pts[1:] if i]))
                print()
            except (KeyboardInterrupt, EOFError):
                print()
                dirt = self.modules[0].dirty
                kwds = set(self.modules[0])
                if not kwds:
                    break
                if dirt and pause('return and save keywords', cancel=True):
                    continue
                break
        self.config.save()
