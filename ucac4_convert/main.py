
import argparse

from ucac4_convert.converters import convert_from_ascii_to_sqlite, convert_from_binary_to_sqlite, \
    convert_zonestats_from_ascii_to_sqlite

def do_conversion(args):

    # determine the requested conversion based on the prefix in the 'source' and 'target' parameters
    source_format = args.source.split(':')[0]
    source_location = args.source.split(':')[1]

    target_format = args.target.split(':')[0]
    target_location = args.target.split(':')[1]

    count = 0

    if target_format == 'sqlite':

        if source_format == 'ascii_zonestats':
            count = convert_zonestats_from_ascii_to_sqlite(source_location, target_location)

        elif source_format == 'ascii':
            count = convert_from_ascii_to_sqlite(source_location, target_location)

        elif source_format == 'binary':
            count = convert_from_binary_to_sqlite(source_location, target_location)

    return count


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--command, -c", default="zone",help="zone = convert a single zone file (default), zone_stats = convert a zone_stats file")
    parser.add_argument("--source",
                        default="ascii:UCAC4_sample.txt",
                        help="ASCII file in UCAC4 format")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="format:location of the output. Format can be 'sqlite' or 'postgres'. The output is either a path or a database url")

    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 20 july 2022) ---")
    print("source : " + args.source)
    print("target : " + args.target)

    try:
        result = do_conversion(args)
        print(result)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main()


