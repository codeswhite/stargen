from pathlib import Path
from abc import ABCMeta, abstractmethod

class Module(metaclass=ABCMeta):
    def __init__(self, stargen, short_n: str):
        super().__init__()
        self.short_n = short_n
        self.stargen = stargen

        self.config = stargen.config['modules'][short_n]
        self.workspace = Path(stargen.config['workspace'])
        self.dest_dir = self.workspace / self.config['subdir']

    @abstractmethod
    def menu(self) -> dict:
        raise NotImplementedError
