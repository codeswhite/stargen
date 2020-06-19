from time import time

from interutils import pr


class IterationTimer:
    def __init__(self, total: int, init_interval: int = 1, max_interval: int = 15):
        assert total > 0
        assert init_interval > 0
        assert max_interval >= init_interval

        self.total = total
        self.interval = init_interval
        self.max_interval = max_interval
        self.current = self.last = 0
        self.lt = time()

    def tick(self) -> None:
        # Progress
        c = self.current = self.current + 1
        ts = time()

        if ts - self.lt > self.interval:
            # Show status
            delta = c - self.last
            if not delta:
                return pr('No progression!', '!')
            spd = int(delta / self.interval)
            prcnt = c / (self.total / 100)
            eta = int((self.total - c) / spd)
            pr('%.2f%% ' % prcnt +
               f'[{c}/{self.total}]\t@ {spd} ps\tETA: {eta} secs')

            # Checkpoint
            self.lt = ts
            self.last = c
            if self.interval <= self.max_interval:
                self.interval *= 2
