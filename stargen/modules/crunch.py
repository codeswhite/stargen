
from pathlib import Path
import os
from subprocess import call

from .abs_module import Module

from termcolor import cprint, colored
from interutils import pr, cyan, is_package, choose, pause, ask

CHAR_FILE = Path('/usr/share/crunch/charset.lst')


def prompt_int(prompt: str) -> (int, None):
    try:
        return int(input(colored(prompt + ' >', 'yellow')))
    except Exception as e:
        pr('An exception caught!', 'X')
        return print(e)


def prompt_mask() -> (str, None):
    try:
        return input(colored('Mask special chars: \n\t@ will insert lower case characters\n\t, will insert upper case characters\n\t% will insert numbers\n\t^ will insert symbols\n\n> ', 'yellow'))
    except Exception as e:
        pr('An exception caught!', 'X')
        return print(e)


class Crunch(Module):
    def __init__(self, stargen):
        super().__init__(stargen, 'crun')

        # Identify existing crunches
        try:
            self.crunches = os.listdir(self.dest_dir)
        except FileNotFoundError:
            self.crunches = []

    def _gen(self, file_name: str, cmd: iter) -> (str, None):
        # Verify destination dir
        self.dest_dir.mkdir(exist_ok=True)
        ap: Path = self.dest_dir / file_name
        if ap.is_file():
            pr('Skipping, crunch already exist!')
            return file_name
        pr('Generating crunch: ' + cyan(file_name))
        cmd += ['-o', ap]
        call(cmd)
        if not ap.is_file():
            return
        return file_name

    def _crunch(self, crunch_method) -> None:
        try:
            # Crunch it
            cn = crunch_method()
            if not cn:
                return pr("Crunch was NOT generated!", 'X')
            self.crunches.append(cn)  # Save result
        except KeyboardInterrupt:
            print()
            pr('Interrupted!', '!')
            return

    def menu(self) -> tuple:
        return {
            # 'show': (self.show, 'Show crunches'),
            'crunch': (self.crunch, 'Generate a new wordlists via crunch\n\tOpt: "mask" -> Generate a wordlist based on a mask')
        }

    def show(self, args: tuple) -> None:
        pr(f'Destination directory: "{cyan(str(self.dest_dir))}"')
        if not self.crunches:
            return pr('No crunches downloaded yet!', '!')
        pr('Available crunches:')
        for p in self.crunches:
            cprint('  ' + p, 'yellow')
        pr(f'Crunches count: ' + cyan(len(self.crunches)))

    def crunch(self, args: tuple) -> None:
        if not is_package('crunch'):
            return pr('Package "crunch" not installed!', 'X')

        # Get args
        is_mask = args and args[0] == 'mask'

        # Mode switch: [Mask / Charset]
        if is_mask:
            mask = prompt_mask()
            if not mask:
                return pr('Invalid mask!', '!')

            file_name = f'mask_{ask("Enter save name:")}.dict'
            l = str(len(mask))
            return self._crunch(lambda: self._gen(file_name, ['crunch', l, l, '-t', mask]))

        # Get min and max seq len
        min_len = prompt_int('Enter minimum length')
        max_len = prompt_int('Enter maximum length')
        if not min_len or not max_len or \
                min_len < 1 or max_len < min_len:
            return pr('Invalid paramenters!', '!')

        # Ask for a charset to use
        with CHAR_FILE.open(encoding='utf-8') as char_file:
            sets = [n[:-1]
                    for n in char_file if '=' in n and 'sv' not in n]
        select = choose(sets, 'Choose charset:', default=26)  # Actually 27
        if select < 0:
            exit(-1)
        charset = sets[select].split(' ')[0]

        # Confirm
        if not pause(f'generate ({cyan(min_len)}-{cyan(max_len)}) length dict via "{cyan(charset)}" charset', cancel=True):
            return

        file_name = f'{charset}_{min_len}-{max_len}.dict'
        return self._crunch(lambda: self._gen(file_name, ['crunch', str(min_len), str(max_len), '-f', CHAR_FILE, charset]))
