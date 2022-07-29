
import argparse
import math
from ucac4_convert.converters import UCAC4_Converter

def cone_to_box(ra, dec, radius):
    # ra_min, ra_max, dec_min, dec_max
    dec_min = dec - radius
    dec_max = dec + radius
    dec_factor = 1 / math.cos(math.radians(dec))

    ra_min = ra - (radius * dec_factor)
    ra_max = ra + (radius * dec_factor)


    box = [ra_min,ra_max,dec_min,dec_max]
    return box

def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--operation",
                        default="convert",help="convert, cone_search")
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
    parser.add_argument("--rabbit_host",
                        default="192.168.178.37",
                        help="RabbitMQ host")
    parser.add_argument("--rabbit_port",
                        default="5672",
                        help="RabbitMQ port")
    parser.add_argument("--rabbit_user",
                        default="nvermaas",
                        help="RabbitMQ user")
    parser.add_argument("--rabbit_password",
                        default=None,
                        help="RabbitMQ password")
    parser.add_argument("--remove_database",
                        default=False,
                        help="First remove existing database (sqlite only).",
                        action="store_true")
    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 27 july 2022) ---")
    print("source : " + args.source)
    print("target : " + args.target)

    if args.operation == 'cone':
        box = cone_to_box(10,50,10)
        print(box)
    else:
        try:
            converter = UCAC4_Converter(args)
            count = converter.convert()

            print("imported "+ str(count) + " stars")
        except Exception as error:
            print(error)

if __name__ == '__main__':
    main()


