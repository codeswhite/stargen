from argparse import ArgumentParser, Namespace

from .stargen import Stargen


def parse_args() -> Namespace:
    parser = ArgumentParser('Stargen', description="")

    parser.add_argument('-c', '--config', help='Specify path to config file')

    return parser.parse_args()


def main():
    Stargen(parse_args())


if __name__ == "__main__":
    main()
