from utils import pr, cyan, colored


def generic_loop(directory: str, menu: dict) -> None:
    while 1:
        inp = input(colored(f'.{directory}->', 'red', attrs=['bold']))
        if not inp:
            break
        if 'help' in inp:
            for c in menu:
                v = menu[c]
                desc = v[1] if type(
                    v[1]) is str else f'Enter {v[0].capitalize()} menu'
                print(f'  {cyan(c)} -> {colored(desc, "yellow")}')
            continue

        pts = inp.split(' ')
        if pts[0] not in menu:
            pr('No such command! try "help".', '!')
            continue

        command = menu.get(pts[0])
        func = command[0]
        if callable(func):
            func(tuple([i for i in pts[1:] if i]))
        else:
            generic_loop(f'{directory}.{func}', command[1])
        print()
