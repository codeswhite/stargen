from pathlib import Path
from typing import Callable
from time import time

from .abs_module import Module

from termcolor import cprint
from interutils import pr, cyan, pause, choose_file, file_volume, human_bytes, IterationTimer


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


class Keyword(Module, set):
    def __init__(self, stargen):
        self.dirty = False
        super().__init__(stargen, 'kwd')

    def add(self, value):
        if value not in self:
            self.dirty = True
        super().add(value)

    def _modifier_wrapper(self, name: str, impact: str, ask: bool, modifier: Callable[[int], None]) -> None:
        count = len(self)
        if ask and not pause(f'{cyan(name)} keywords (impact: {impact} => {eval(f"{count}{impact}")})', cancel=True):
            return
        modifier(count)
        new_count = len(self)
        pr(f'{name} added {cyan(new_count - count)} new keywords, total: {cyan(new_count)}')

    def menu(self) -> tuple:
        return {
            'load': (self.load, 'Load keywords from wordlist on the disk'),
            'show': (self.print_all, 'List all keywords and show count\n\tOpt: "total" -> Print sum total'),
            'expand': (self.expand, 'Expand keywords\n\tOpt: "all" -> Execute all modifications'),
            'add': (self.add, 'Add keyword(s)'),
            'rem': (self.rem, 'Remove keyword(s)'),
            'clear': (self.clear, 'Clear all keywords'),
            'isin': (self.isin, 'Check if string(s) among keywords')
        }

    def load(self, args: tuple) -> None:
        if self:
            pr(f'Already have {cyan(len(self))} keywords')
            if not pause(cancel=True):
                return
        f = choose_file(self.workspace)
        if not f:
            return

        sb, lc, txt = file_volume(f)
        pr(txt)

        if sb > 1*1024**3:  # 1 GB
            pr(f'File is too larget to be loaded into RAM!', '!')
            return
        pr('Loading keywords...')
        self.update(f.read_text(encoding='utf-8').split('\n'))
        pr('Done!')

    def print_all(self, args: tuple) -> None:
        if not self:
            return pr('No keywords registered yet!', '!')

        # Get arguments
        total = False
        if len(args) > 0:
            total = args[0] == 'total'

        # Print relevant info
        if not total:
            if len(self) > self.config['list_treshold']:
                if not pause(f'show all {cyan(len(self))} keywords', cancel=True):
                    return
            for v in self:
                cprint('  ' + v, "yellow")
        pr(f'Total keywords count: ' + cyan(len(self)))

    def expand(self, args: tuple) -> None:
        if not self:
            return pr('No keywords registered yet!', '!')

        auto_all = False
        if len(args) > 0:
            auto_all = args[0] == 'all'

        def _capitalize(count: int) -> None:
            for k in tuple(self):
                self.add(k.capitalize())
        self._modifier_wrapper('Capitalize', '*2', not auto_all, _capitalize)

        def _leetify(count: int) -> None:
            for k in tuple(self):
                self.add(leetify(k))
        self._modifier_wrapper('13371fy', '*2', not auto_all, _leetify)

        def _mockify(count: int) -> None:
            for k in tuple(self):
                self.add(mockify(k, True))
                self.add(mockify(k, False))
        self._modifier_wrapper('MoCkIfY', '*3', not auto_all, _mockify)

        def _intermix(count: int) -> None:
            itmr = IterationTimer(count ** 2)
            snapshot = tuple(self)
            for a in snapshot:
                for b in snapshot:
                    self.add(a + b)
                    self.add(b + a)
                    itmr.tick()
        self._modifier_wrapper('Intermix', '**2', not auto_all, _intermix)

        # Show current status
        print()
        a = []
        if len(self) > self.config['list_treshold']:
            a += ['total']
        self.print_all(a)

    def dump(self, args: tuple) -> None:
        if not self:
            return pr('No keywords registered yet!', '!')

        save_name = args[0] if args else str(int(time()))
        out_file = self.dest_dir.joinpath('kwd_' + save_name)

        out_file.write_text('\n'.join(self), encoding='utf-8')
        pr('Dumped into ' + cyan(str(out_file)))
        self.dirty = False

    def add(self, args: tuple) -> None:
        if not args:
            return pr('Usage: add <keyword...>', '*')
        for a in args:
            if a in self:
                pr(f'Skipping duplicate "{cyan(a)}"', '*')
                continue
            pr(f'Adding "{a}"')
            self.add(a)

    def rem(self, args: tuple) -> None:
        if not args:
            return pr('Usage: rem <keyword...>', '*')
        for a in args:
            if a not in self:
                pr(f'Keyword "{cyan(a)}" not found!', '!')
                continue
            pr(f'Removing "{cyan(a)}"')
            self.remove(a)

    def clear(self, args: tuple) -> None:
        if not pause('clear keywords', cancel=True):
            return
        self.clear()
        pr('Set cleared!')

    def isin(self, args: tuple) -> None:
        if not args:
            return pr('Usage: add <keyword...>', '*')
        for a in args:
            if a in self:
                pr(f'Found a match for {cyan(a)}')
            else:
                pr(f'No match for {cyan(a)}', '!')
