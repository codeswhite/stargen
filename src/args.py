from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace:
    parser = ArgumentParser('Stargen', description="")
    
    parser.add_argument('-c', '--config', help='Specify path to config file')
    
    return parser.parse_args()