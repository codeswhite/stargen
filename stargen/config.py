import json
from pathlib import Path

from interutils import pr, cyan, DictConfig  # , cprint


class Config(DictConfig):
    def __init__(self, conf_path: Path, default_config: dict):
        super().__init__(conf_path, default_config)

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
