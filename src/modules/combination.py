from pathlib import PurePath, Path
from utils import pr, cyan, choose, pause
from os import listdir
from subprocess import check_output
from time import time, strftime, gmtime
from typing import Optional, Callable

from ..iteration_timer import IterationTimer


def human_bytes(size_in_bytes: int) -> str:
    unit = 0
    while size_in_bytes >= 1024:
        unit += 1
        size_in_bytes /= 1024
    return str(round(size_in_bytes)) + ('', 'KB', 'MB', 'GB', 'TB')[unit]


def count_lines(file_path: Path) -> int:
    # TODO Crossplatformize
    return int(check_output(('/usr/bin/wc', '-l', str(file_path.resolve()))).decode().split(' ')[0])


def choose_file(root_dir: PurePath) -> Optional[PurePath]:
    def _format(root_dir: PurePath, entry: str) -> str:
        f = root_dir / entry
        if f.is_dir():
            return entry
        return f'{entry}\t({human_bytes(f.stat().st_size)}, {count_lines(f)})'
    listing = listdir(root_dir)
    if not listing:
        return pr('Empty directory!', '!')
    while 1:
        c = choose([_format(root_dir, i) for i in listing], default=-1)
        if c < 0:
            return
        f = root_dir / listing[c]
        if f.is_dir():
            f = choose_file(root_dir / f)
            if not f:
                continue
        return f


def print_file_volume(path: Path, show: bool = True) -> tuple:
    sb = path.stat().st_size
    lc = count_lines(path)
    if show:
        pr(f'  {cyan(path.name)} ({human_bytes(sb)}, {lc})')
    return sb, lc


def show_disk_impact(workspace: Path, tsb: int, tlc: int) -> bool:
    def avail_space(workspace: Path, show: bool = True) -> int:
        # TODO Crossplatformize
        b = check_output(
            ('/usr/bin/df', '--sync', '--output=avail', str(workspace.resolve())))
        b = 1024 * int(b.decode().split('\n')[1])
        if show:
            pr(f'Available space in workspace: ' + cyan(human_bytes(b)))
        return b

    pr(f'Mixing will allocate {cyan(human_bytes(tsb))} for {cyan("{:,}".format(tlc))} lines')
    if tsb > avail_space(workspace):
        pr('Not enough space on the workspace disk for such creation!', '!')
        return False
    return True


def show_ebt(algos: dict, tlc: int):
    assert tlc > 0

    for algo, elps in algos.items():
        ebt = ((tlc * 2) / elps)
        ebt = strftime('%H:%M:%S', gmtime(ebt))
        pr(f'Estimated {cyan(algo)} time: {cyan(ebt)} (assuming elps={elps})')


def ask_two_wl(workspace: Path, subdir: Path, _total_calc=Callable[[int, int], int], _write_action=Callable[[Path, Path, Path, IterationTimer], None]):
    pr('Select first wordlist:')
    f1 = choose_file(workspace)
    if not f1:
        return
    f1sb, f1lc = print_file_volume(f1)

    pr('Select secund wordlist:')
    f2 = choose_file(workspace)
    if not f2:
        return
    f2sb, f2lc = print_file_volume(f2)

    # Show disk impact
    tsb = _total_calc(f1sb, f2sb)
    tlc = _total_calc(f1lc, f2lc)
    if not show_disk_impact(workspace, tsb, tlc):
        return

    if not pause(cancel=True):
        return

    # Verify destination directory
    dest_dir = workspace / subdir
    dest_dir.mkdir(exist_ok=True)

    out_path: Path = dest_dir / f'{f1.stem}_{f2.stem}'
    with out_path.open('w', encoding='utf-8') as out_file:
        itmr = IterationTimer(tlc, init_interval=1, max_interval=15)
        _write_action(f1, f2, out_file, itmr)

    # Finalize
    pr('Wordlist written into: ' + cyan(out_path.name))
    show_ebt({  # TODO Move to config
        'WPA2': 57000
    }, tlc)


class Combination:
    def __init__(self, stargen):
        super().__init__()
        self.stargen = stargen
        self.config = stargen.config['modules']['comb']
        self.workspace = Path(self.stargen.config['workspace'])

    def menu(self) -> tuple:
        return 'combination', {
            'mix': (self.mix, 'Mix two wordlists'),
            'concat': (self.concat, 'Concatenate two wordlists')
        }

    def mix(self, args: tuple) -> None:
        def mix_action(f1: Path, f2: Path, out_file: Path, itmr: IterationTimer) -> None:
            with f1.open(encoding='utf-8') as f1d:
                for l1 in f1d:
                    if '# ' in l1 or '##' in l1:
                        continue
                    l1 = l1.strip()

                    with f2.open(encoding='utf-8') as f2d:
                        for l2 in f2d:
                            if '# ' in l2 or '##' in l2:
                                continue
                            l2 = l2.strip()

                            out_file.write(f'{l1}{l2}\n{l2}{l1}\n')
                            itmr.tick()

        if ask_two_wl(self.workspace, self.config['subdir'],
                      (lambda a, b: a ** b * 2), mix_action) is None:
            return  # Currently redundant - might be of use later

    def concat(self, args: tuple) -> None:
        def concat_action(f1: Path, f2: Path, out_file: Path, itmr: IterationTimer) -> None:
            with f1.open(encoding='utf-8') as f1d:
                for l1 in f1d:
                    if '# ' in l1 or '##' in l1:
                        continue

                    out_file.write(l1)
                    itmr.tick()

            with f2.open(encoding='utf-8') as f2d:
                for l2 in f2d:
                    if '# ' in l2 or '##' in l2:
                        continue

                    out_file.write(l2)
                    itmr.tick()

        if ask_two_wl(self.workspace, self.config['subdir'],
                      (lambda a, b: a + b), concat_action) is None:
            return  # Currently redundant - might be of use later
