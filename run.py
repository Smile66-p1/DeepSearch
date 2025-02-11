import argparse

from deepsearch import deepsearch

__version__ = "0.1.0"
github = "https://github.com/Smile66-p1/deepsearch"


def main():
    parser = argparse.ArgumentParser(description="OnionSearch help text")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    subparsers.add_parser("list", help="All search resources")

    subparsers.add_parser("checkresources", help="Checking a resource for operability")

    parser_search = subparsers.add_parser("search", help="Command of search")
    parser_search.add_argument(
        "searchtext", type=str, help="The text or word to search in the bucket"
    )
    parser_search.add_argument(
        "--threads", type=int, default=4, help="Number of search threads"
    )
    parser_search.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Check links received from resources",
    )

    args = parser.parse_args()

    # print(
    #     "░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓██████▓▒░ ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░\n"
    # )
    # print("Developed by Smile")++++++
    print(f"Version {__version__}")
    # print(f"Github: {github}\n")

    if args.command == "list":
        resources = deepsearch.getSearchResources()
        for resource in resources:
            print(resource["name"])
            print(f"-URL {resource['URL']}")
            print(f"-Status {resource['status']}")
            print(f"-Last checked on {resource['last_check']}\n")
    elif args.command == "search":
        deepsearch.search(**args.__dict__)
    elif args.command == "checkresources":
        deepsearch.checkresources()


if __name__ == "__main__":
    main()
