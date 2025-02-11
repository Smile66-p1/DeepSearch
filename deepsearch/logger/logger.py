from colorama import Fore, init

init(autoreset=True)

COLORS = {"green": Fore.GREEN, "yellow": Fore.YELLOW, "red": Fore.RED}


def log(print_data: tuple[tuple], end: str = "\n"):
    for element in print_data:
        print(COLORS[element[1]] + element[0], end="")
    print(end=end)
