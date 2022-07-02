import argparse
import os


def do_conversion(args):
    # check whether the source exists
    if args.source_file:
        pass

    # determine the requested conversion


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument("--source_file",
                        default="UCAC4_sample.txt",
                        help="ASCII file in UCAC4 format")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="single cardboard file to convert")

    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 2 july 2022) ---")
    print("source_file: " + args.source_file)
    print("target     : " + args.target)

    do_conversion(args)

if __name__ == '__main__':
    main()


