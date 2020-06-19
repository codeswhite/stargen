from pathlib import PurePath, Path
from subprocess import check_output
from time import time, strftime, gmtime
from typing import Optional, Callable
from shutil import disk_usage

from interutils import pr, cyan, choose, pause, human_bytes, count_lines, choose_file, file_volume, IterationTimer
from .abs_module import Module


def show_disk_impact(workspace: Path, tsb: int, tlc: int) -> bool:
    pr(f'Mixing will allocate {cyan(human_bytes(tsb))} for {cyan("{:,}".format(tlc))} lines')

    free = disk_usage(workspace.resolve()).free
    pr(f"Available space on workspace's disk: " + cyan(human_bytes(free)))
    if tsb > free:
        pr('Not enough space on the workspace disk for such creation!', '!')
        return False
    return True


def show_ebt(algos: dict, tlc: int):
    assert tlc > 0

    for algo, elps in algos.items():
        ebt = ((tlc * 2) / elps)
        ebt = strftime('%H:%M:%S', gmtime(ebt))
        pr(f'Estimated {cyan(algo)} time: {cyan(ebt)} (assuming elps={elps})')


class Combination(Module):
    def __init__(self, stargen):
        super().__init__(stargen, 'comb')

    def menu(self) -> tuple:
        return {
            'intermix': (self.mix, 'Mix two wordlists'),
            'concat': (self.concat, 'Concatenate two wordlists')
        }

    def ask_two_wl(self, _total_calc=Callable[[int, int], int], _write_action=Callable[[Path, Path, Path, IterationTimer], None]):
        pr('Select first wordlist:')
        f1 = choose_file(self.workspace)
        if not f1:
            return
        f1sb, f1lc, f1txt = file_volume(f1)
        pr(f'  {f1txt}')

        pr('Select secund wordlist:')
        f2 = choose_file(self.workspace)
        if not f2:
            return
        f2sb, f2lc, f2txt = file_volume(f2)
        pr(f'  {f2txt}')

        # Calculate impact impact
        tsb = _total_calc(f1sb, f2sb)
        tlc = _total_calc(f1lc, f2lc)
        if tsb > self.config['max_created_file_size']:
            return pr('Calculation resulted in an oversized file, aborting!', '!')
        if not show_disk_impact(self.workspace, tsb, tlc) or not pause(cancel=True):
            return

        out_path: Path = self.dest_dir / f'{f1.stem}_{f2.stem}'
        with out_path.open('w', encoding='utf-8') as out_file:
            itmr = IterationTimer(tlc, init_interval=1, max_interval=15)
            _write_action(f1, f2, out_file, itmr)

        # Finalize
        pr('Wordlist written into: ' + cyan(out_path.name))
        show_ebt({  # TODO Move to config
            'WPA2': 57000
        }, tlc)

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
                            itmr.tick()  # O(n^2)

        if self.ask_two_wl((lambda a, b: int(a * b * 2)), mix_action) is None:
            return  # Currently redundant - might be of use later

    def concat(self, args: tuple) -> None:
        def concat_action(f1: Path, f2: Path, out_file: Path, itmr: IterationTimer) -> None:
            with f1.open(encoding='utf-8') as f1d:
                for l1 in f1d:
                    if '# ' in l1 or '##' in l1:
                        continue

                    out_file.write(l1)
                    itmr.tick()  # O(n)

            with f2.open(encoding='utf-8') as f2d:
                for l2 in f2d:
                    if '# ' in l2 or '##' in l2:
                        continue

                    out_file.write(l2)
                    itmr.tick()  # O(n)

        if self.ask_two_wl((lambda a, b: a + b), concat_action) is None:
            return  # Currently redundant - might be of use later
