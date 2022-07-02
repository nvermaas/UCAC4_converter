import argparse
import os


def do_conversion(args):
    # check whether the source exists
    if args.source_file:
        pass


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument("--source_file",
                        default=None,
                        help="single cardboard file to convert")
    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 2 july 2022) ---")
    print(args)

    do_conversion(args)

if __name__ == '__main__':
    main()


