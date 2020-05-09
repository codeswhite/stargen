from time import time

from utils import pr


class IterationTimer:
    def __init__(self, tlc: int, init_interval: int = 1, max_interval: int = 15):
        assert tlc > 0
        assert init_interval > 0
        assert max_interval >= init_interval

        self.tlc = tlc
        self.interval = init_interval
        self.max_interval = max_interval
        self.i = self.lp = 0
        self.lt = time()

    def tick(self) -> None:
        # Progress
        self.i += 1
        i = self.i
        ts = time()

        if ts - self.lt > self.interval:
            # Checkpoint
            self.lt = ts
            self.lp = i
            if self.interval <= self.max_interval:
                self.interval *= 2

            # Show status
            delta = i - self.lp
            if not delta:
                return pr('No progression!', '!')
            spd = int(delta / self.interval)
            prcnt = i / (self.tlc / 100)
            eta = int((self.tlc - i) / spd)
            pr('%.2f%% ' % prcnt +
               f'[{i}/{self.tlc}]\t@ {spd} ps\tETA: {eta} secs')
