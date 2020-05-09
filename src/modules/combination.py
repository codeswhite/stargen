from pathlib import PurePath, Path
from utils import pr, cyan, choose, pause
from os import listdir
from subprocess import check_output
from time import time, strftime, gmtime


def human_size(size_in_bytes: int):
    unit = 0
    while size_in_bytes >= 1024:
        unit += 1
        size_in_bytes /= 1024
    return str(round(size_in_bytes)) + ('', 'KB', 'MB', 'GB', 'TB')[unit]


def count_lines(file_path: Path) -> int:
    # TODO Crossplatform
    return int(check_output(('/usr/bin/wc', '-l', str(file_path.resolve()))).decode().split(' ')[0])


def avail_space(workspace: Path) -> int:
    # TODO Crossplatform
    return 1024 * int(check_output(('/usr/bin/df', '--sync', '--output=avail', str(workspace.resolve()))).decode().split('\n')[1])


def choose_file(root_dir: PurePath) -> (PurePath, None):
    def _format(root_dir: PurePath, entry: str):
        f = root_dir / entry
        if f.is_dir():
            return entry
        return f'{entry}\t({human_size(f.stat().st_size)}, {count_lines(f)})'
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


class Combination:
    def __init__(self, stargen):
        super().__init__()
        self.stargen = stargen
        self.config = stargen.config['comb']
        self.dest_dir = Path(
            stargen.config['workspace']) / self.config['subdir']

    def menu(self) -> tuple:
        return 'combination', {
            # 'show': (sel, '')
            'mix': (self.mix, 'Mix two dicts'),
            'craft': (self.craft, 'Craft a dict from keywords and another dict')
        }

    def mix(self, args) -> None:
        workspace = Path(self.stargen.config['workspace'])

        pr('Select first dictionary:')
        f1 = choose_file(workspace)
        if not f1:
            return
        f1sb = f1.stat().st_size
        f1lc = count_lines(f1)
        pr(f'  {cyan(f1.name)} ({human_size(f1sb)}, {f1lc})')

        pr('Select secund dictionary:')
        f2 = choose_file(workspace)
        if not f2:
            return
        f2sb = f2.stat().st_size
        f2lc = count_lines(f2)
        pr(f'  {cyan(f2.name)} ({human_size(f2sb)}, {f2lc})')

        # Show disk impact
        availb = avail_space(workspace)
        pr(f'Available space in workspace: ' + cyan(human_size(availb)))
        allocb = f1sb * f2sb * 2
        twcl = f1lc * f2lc * 2
        pr(f'Mixing will allocate {cyan(human_size(allocb))} for {cyan("{:,}".format(twcl))} lines')
        if allocb > availb:
            return pr('Not enough space on the workspace disk for such a mix!', '!')

        if not pause(cancel=True):
            return

        # Verify destination directory
        self.dest_dir.mkdir(exist_ok=True)

        out_path: Path = self.dest_dir / f'{f1.stem}_{f2.stem}'
        pr(f'Mixing dictionaries into "{cyan(out_path.name)}"')

        with out_path.open('w', encoding='utf-8') as out_file:
            i = lp = 0
            lt = time()
            interval = 1
            max_interval = 15

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

                            # Write
                            out_file.write(f'{l1}{l2}\n{l2}{l1}\n')

                            i += 1
                            ts = time()
                            if ts - lt > interval:
                                spd = int((i - lp) / interval)
                                prcnt = i / (twcl / 100)
                                eta = int((twcl - i) / spd)
                                pr('%.2f%% ' % prcnt +
                                   f'[{i}/{twcl}]\t@ {spd} ps\tETA: {eta} secs')
                                lt = ts
                                lp = i
                                if interval <= max_interval:
                                    interval *= 2
        pr('List written into: ' + cyan(out_path.name))

        ebs = 57000
        ebt = ((twcl * 2) / ebs)
        ebt = strftime('%H:%M:%S', gmtime(ebt))
        pr(f'Estimated WPA2 time: {cyan(ebt)} minutes (assuming est.line/sec={ebs})')

    def craft(self, args) -> None:
        pass #TODO
