from pathlib import Path
from typing import Callable
from time import time
from shutil import copy, move
from tempfile import mkstemp

from .abs_module import Module

from termcolor import cprint, colored
from interutils import pr, cyan, pause, choose_file, file_volume, IterationTimer, count_lines, ask


def mockify(text: str, start_first: bool) -> str:
    r = ''
    for i in range(len(text)):
        c = text[i]
        if i % 2 == int(start_first):
            c = c.swapcase()
        r += c
    return r


def leetify(text: str):
    result = text.translate(str.maketrans('AaSsIiEeOoTtBb', '@@551133007788'))
    return result


class Keyword(Module):
    def __init__(self, stargen):
        super().__init__(stargen, 'kwd')
        self.current: Path = None

    def _modifier_wrapper(self, tmp_path: Path, name: str, impact: str, ask: bool, modifier: Callable[[int], None]) -> None:
        count = count_lines(tmp_path)
        if ask and not pause(f'{cyan(name)} keywords (impact: {impact} => {eval(f"{count}{impact}")})', cancel=True):
            return
        modifier(tmp_path, count)
        new_count = count_lines(tmp_path)
        pr(f'{name} added {cyan(new_count - count)} new keywords, total: {cyan(new_count)}')

    def _get_wordlist_path(self):
        if self.current:
            return self.current
        pr('Please choose a wordlist')
        return choose_file(self.workspace)

    def _gen_wordlist(self, wordlist: Path):
        if wordlist:
            f = wordlist
        else:
            f = self._get_wordlist_path()
            if not f:
                return
        for l in f.read_text(encoding='utf8').splitlines():
            yield l

    def menu(self) -> tuple:
        return {
            'use': (self.use, 'Specify which wordlist to use for operations'),
            'show': (self.print_all, 'List all keywords and show count\n\tOpt: "total" -> Print sum total'),
            'expand': (self.expand, 'Expand keywords\n\tOpt: "all" -> Execute all modifications'),
            'add': (self.add, 'Add keyword(s)'),
            # 'rem': (self.rem, 'Remove keyword(s)'),
            'clear': (self.clear, 'Clear all keywords'),
            'duplicate': (self.duplicate, 'Duplicate the wordlist\n\tReq: "name" -> Duplicated wordlist file name'),
            'isin': (self.isin, 'Check if string(s) among keywords')
        }

    def use(self, args: tuple) -> None:
        if self.current:
            if not pause(f'Switching from {cyan(self.current)} to new wordlist', cancel=True):
                return
        f = choose_file(self.workspace)
        if not f:
            return

        sb, lc, txt = file_volume(f)
        pr(txt)

        # if sb > 1*1024**3:  # 1 GB
        #     pr(f'File is too larget to be loaded into RAM!', '!')
        #     return
        self.current = f
        pr(f'Now using {cyan(self.current)} wordlist!')

    def print_all(self, args: tuple) -> None:
        f = self._get_wordlist_path()
        if not f:
            return

        lc = count_lines(f)
        if not lc:
            return pr('Wordlist is empty!', '!')

        # Get arguments
        total = False
        if args:
            total = args[0] == 'total'

        # Print relevant info
        if not total:
            if lc > self.config['list_treshold']:
                if not pause(f'show all {cyan(lc)} keywords', cancel=True):
                    return
            for v in self._gen_wordlist(f):
                cprint('  ' + v, "yellow")
        pr(f'Total keywords count: ' + cyan(lc))

    def expand(self, args: tuple) -> None:
        f = self._get_wordlist_path()
        if not f:
            return

        lc = count_lines(f)
        if not self:
            return pr('Wordlist is empty!', '!')

        # Get new wordlist name
        try:
            print('Enter name for new expanded wordlist:')
            save_path = input(colored('>', 'yellow'))
            if not save_path:
                return
            save_path = self.workspace.joinpath('expand_' + str(save_path))
            if save_path.is_file():
                pr(f'File {cyan(save_path)} already exists, overwrite?', '!')
                if not pause(cancel=True):
                    return
        except KeyboardInterrupt:
            return

        # Get arguments
        auto_all = False
        if args:
            auto_all = args[0] == 'all'

        _, tmp_path = mkstemp('stargen')
        tmp_path = Path(tmp_path)

        # Copy initial content
        tmp_path.write_bytes(f.read_bytes())

        def _capitalize(tmp_p: Path, count: int) -> None:
            with tmp_p.open('a', encoding='utf8') as file:
                for k in self._gen_wordlist(f):
                    file.write(k.capitalize() + '\n')
        self._modifier_wrapper(tmp_path, 'Capitalize', '*2',
                               not auto_all, _capitalize)

        def _leetify(tmp_p: Path, count: int) -> None:
            with tmp_p.open('a', encoding='utf8') as file:
                for k in self._gen_wordlist(f):
                    file.write(leetify(k) + '\n')
        self._modifier_wrapper(tmp_path, '13371fy', '*2',
                               not auto_all, _leetify)

        def _mockify(tmp_p: Path, count: int) -> None:
            with tmp_p.open('a', encoding='utf8') as file:
                for k in self._gen_wordlist(f):
                    file.write(mockify(k, True) + '\n')
                    file.write(mockify(k, False) + '\n')
        self._modifier_wrapper(tmp_path, 'MoCkIfY', '*3',
                               not auto_all, _mockify)

        def _intermix(tmp_p: Path, count: int) -> None:
            itmr = IterationTimer(count ** 2)
            with tmp_p.open('a', encoding='utf8') as file:
                for a in self._gen_wordlist(f):
                    for b in self._gen_wordlist(f):
                        file.write(a + b + '\n')
                        file.write(b + a + '\n')
                        itmr.tick()
        self._modifier_wrapper(tmp_path, 'Intermix', '**2',
                               not auto_all, _intermix)

        # Save as
        pr(f'Saving as: {cyan(save_path)}')
        move(tmp_path, save_path)
        new_lc = count_lines(save_path)

        # Show current status
        print()
        a = []
        if new_lc > self.config['list_treshold']:
            a += ['total']
        self.print_all(a)

    def add(self, args: tuple) -> None:
        if not args:
            return pr('Usage: add <keyword...>', '*')

        f = self._get_wordlist_path()
        if not f:
            return

        for a in args:
            if a in self._gen_wordlist(f):
                pr(f'Skipping duplicate "{cyan(a)}"', '*')
                continue
            pr(f'Adding "{a}"')
            with f.open('a') as file:
                file.write(a)

    def clear(self, args: tuple) -> None:
        if not pause('truncatete wordlist', cancel=True):
            return

        f = self._get_wordlist_path()
        if not f:
            return

        with f.open('w') as file:
            file.truncate()
        pr('Wordlist truncateted!')

    def duplicate(self, args: tuple) -> None:
        if not args:
            return pr('Usage: duplicate <copy_name>', '*')

        f = self._get_wordlist_path()
        if not f:
            return

        dst = Path(args[0])
        if dst.is_file():
            pr(f'File {cyan(dst)} already exists, overwrite?', '!')
            if not pause(cancel=True):
                return
        copy(f, dst)
        pr(f'Copied to {cyan(dst)}!')

    def isin(self, args: tuple) -> None:
        if not args:
            return pr('Usage: isin <keyword...>', '*')

        f = self._get_wordlist_path()
        if not f:
            return

        for a in args:
            if a in self._gen_wordlist(f):
                pr(f'Found a match for {cyan(a)}')
            else:
                pr(f'No match for {cyan(a)}', '!')
