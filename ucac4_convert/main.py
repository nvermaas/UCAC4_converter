
import argparse

from ucac4_convert.converters import UCAC4_Converter

def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--command, -c", default="convert",help="convert, cone_search")
    parser.add_argument("--source",
                        default="binary:../z001",
                        help="source format:location. Source can be 'ascii','ascii_zonestats','binary'")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="format:location of the output. Format can be 'sqlite' or 'postgres'. The output is either a path or a database url")
    parser.add_argument("--host",
                        default="localhost",
                        help="database host")
    parser.add_argument("--user",
                        default="postgres",
                        help="postgres user")
    parser.add_argument("--password",
                        default="postgres",
                        help="postgres password")
    parser.add_argument("--port",
                        default="5432",
                        help="database host")
    parser.add_argument("--database",
                        default="postgres",
                        help="postgres database")
    parser.add_argument("--remove_database",
                        default=False,
                        help="First remove existing database (sqlite only).",
                        action="store_true")
    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 20 july 2022) ---")
    print("source : " + args.source)
    print("target : " + args.target)

    try:
        converter = UCAC4_Converter(args)
        count = converter.convert()

        print("imported "+ str(count) + " stars")
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main()


