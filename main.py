import sys

import commands
from parser import get_main_parser


def main():
    parser = get_main_parser()
    args = parser.parse_args()
    print(args)

    if not args.cmd:
        parser.parse_args(['--help'])
        sys.exit(0)

    if args.cmd:
        getattr(commands, args.cmd.replace('-', '_'))(args)


if __name__ == '__main__':
    main()
