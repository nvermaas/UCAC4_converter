
import argparse

from ucac4_convert.converters import UCAC4_Converter

def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--command, -c", default="convert",help="convert, cone_search")
    parser.add_argument("--source",
                        default="binary:../z001",
                        help="source format:path. Source can be 'ascii','ascii_zonestats','binary'")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="format:location of the output. Format can be 'sqlite' or 'postgres'. The output is either a path or a database url")

    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 20 july 2022) ---")
    print("source : " + args.source)
    print("target : " + args.target)

    try:
        converter = UCAC4_Converter(args)
        count = converter.convert()

        print(count)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main()


