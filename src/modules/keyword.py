from utils import pr, cyan, cprint, pause


class Keyword(set):
    def __init__(self):
        super().__init__()

    def menu(self) -> tuple:
        return 'keywords', {
            'show': (self.show, 'List all keywords'),
            'expand': (self.expand, 'Expand current keywords'),
            'add': (self._add, 'Add keyword(s)'),
            'rem': (self.rem, 'Remove keyword(s)'),
            'clear': (self._clear, 'Clear all keywords')
        }

    def show(self, args: tuple) -> None:
        if not self:
            return pr('No keywords registered yet!', '!')
        for v in self:
            cprint('  ' + v, "yellow")
        pr(f'Keywords count: ' + cyan(len(self)))

    def expand(self, args) -> None:
        if pause(cyan('capitalize') + 'keywords', cancel=True):
            for k in self:
                self.add(k.capitalize())
        # TODO 1337, mOcKiNg and more

        # Show current status
        self.show()

    def _add(self, args: tuple) -> None:
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

    def _clear(self, args) -> None:
        self.clear()
        pr('Set cleared!')
