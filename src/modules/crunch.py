
from pathlib import Path
import os
from subprocess import call

from utils import pr, cyan, cprint, colored, is_package, choose, pause

from .abs_module import Module

CHAR_FILE = Path('/usr/share/crunch/charset.lst')


def prompt_int(prompt: str) -> (int, None):
    try:
        return int(input(colored(prompt + ' >', 'yellow')))
    except Exception as e:
        pr('An exception caught!', 'X')
        return print(e)


def gen_nums(charset: str, min_len: int, max_len: int, work_dir: Path) -> (Path, None):
    file_name = f'{charset}_{min_len}-{max_len}.dict'
    ap: Path = work_dir / file_name
    if ap.is_file():
        pr('Skipping, crunch already exist!')
        return file_name
    pr('Generating crunch: ' + cyan(file_name))
    pr(f'CMD: "crunch {min_len} {max_len} -f {CHAR_FILE} {charset} -o {ap}"', '~')
    call(['crunch', str(min_len), str(max_len),
          '-f', CHAR_FILE, charset, '-o', ap])

    if not ap.is_file():
        return None
    return file_name


class Crunch(Module):
    def __init__(self, stargen):
        super().__init__(stargen, 'crun')

        # Identify existing crunches
        try:
            self.crunches = os.listdir(self.dest_dir)
        except FileNotFoundError:
            self.crunches = []

    def __str__(self):
        return 'crunch'

    def menu(self) -> tuple:
        return str(self), {
            'show': (self.show, 'Show crunches'),
            'gen': (self.gen, 'Generate a new wordlists via crunch')
        }

    def show(self, args: tuple) -> None:
        pr(f'Destination directory: "{cyan(str(self.dest_dir))}"')
        if not self.crunches:
            return pr('No crunches downloaded yet!', '!')
        pr('Available crunches:')
        for p in self.crunches:
            cprint('  ' + p, 'yellow')
        pr(f'Crunches count: ' + cyan(len(self.crunches)))

    def gen(self, args: tuple) -> None:
        if not is_package('crunch'):
            return pr('Package "crunch" not installed!', 'X')

        # Get min and max seq len
        min_len = prompt_int('Enter minimum length')
        max_len = prompt_int('Enter maximum length')
        if not min_len or not max_len or \
                min_len < 1 or max_len < min_len:
            return pr('Invalid paramenters!', '!')

        # Get charset to use
        with CHAR_FILE.open(encoding='utf-8') as char_file:
            sets = [n[:-1] for n in char_file if '=' in n and 'sv' not in n]
        select = choose(sets, 'Choose charset:', default=26)  # Actually 27
        if select < 0:
            exit(-1)
        charset = sets[select].split(' ')[0]

        # Accept
        if not pause(f'generate ({cyan(min_len)}-{cyan(max_len)}) length dict via "{cyan(charset)}" charset', cancel=True):
            return

        # Verify destination dir
        self.dest_dir.mkdir(exist_ok=True)

        # Crunch it
        try:
            crunch_name = gen_nums(charset, min_len, max_len, self.dest_dir)
            if not crunch_name:
                return pr("Crunch was NOT generated!", 'X')
            self.crunches.append(crunch_name)  # Save result
        except:
            print()
            pr('Interrupted!', '!')
            return
