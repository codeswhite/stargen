import json
from pathlib import Path

from utils import pr, cyan  # , cprint


class Config(dict):
    def __init__(self, path: Path, default_setup: dict):
        super().__init__({})
        self.path = path
        if path.is_file():
            # Load
            self.update(json.loads(self.path.read_text()))
        else:
            # Initialize and save
            pr(f'Config not found, generating fresh in: "{cyan(path)}"', '!')
            for k, v in default_setup['modules'].items():
                v.update({'subdir': k})
            self.update(default_setup)
            self.save()

    def save(self):
        self.path.write_text(json.dumps(self))

    # def menu(self) -> tuple:
    #     return 'configuration', {
    #         'show': (self.show, 'Show whole config'),
    #         'get': (self._get, 'Get value'),
    #         'set': (self._set, 'Set value'),
    #     }

    # def _get(self, args):
    #     if not args:
    #         return pr('Usage: get <key...>', '!')
    #     for k in args:
    #         cprint(f'  {k}={self[k]}', 'yellow')

    # def _set(self, args):
    #     if len(args) != 2:
    #         return pr('Usage: set <key> <value>', '!')
    #     k, v = args
    #     if k not in self:
    #         return pr(f'No such key: "{cyan(k)}"', '!')
    #     pr(f'Setting "{cyan(k)}" to "{cyan(v)}"')
    #     self[k] = v

    # def show(self, args):
    #     def _print_dict(ident, d):
    #         ident += 2
    #         for k, v in d.items():
    #             if type(v) is dict:
    #                 cprint(f'{" " * ident}{k}:', 'yellow')
    #                 _print_dict(ident, v)
    #                 continue
    #             cprint(f'{" " * ident}{k}={v}', 'yellow')
    #     if not self:
    #         return pr('Nothing to show!', '!')
    #     _print_dict(0, self)
