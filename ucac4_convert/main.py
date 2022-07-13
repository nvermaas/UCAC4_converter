import os, sys
import argparse
import codecs

progressbar_length = 100

from ucac4_convert.sqlite_helper import create_sqlite_database, add_star_to_sqlite

def parse_ascii_line(line):
    # https://irsa.ipac.caltech.edu/data/UCAC4/readme_u4.txt

    ucac4_id = line[0:10]
    ot       = int(line[84:85])

    # 0 = good, clean star (from MPOS), no known problem
    # 1 = largest flag of any image = near overexposed star (from MPOS)
    # 2 = largest flag of any image = possible streak object (from MPOS)
    # 3 = high proper motion (HPM) star, match with external PM file (MPOS)
    # 4 = actually use external HPM data instead of UCAC4 observ.data (accuracy of positions varies between catalogs)
    # 5 = poor proper motion solution, report only CCD epoch position
    # 6 = substitute poor astrometric results by FK6/Hip/Tycho-2 data
    # 7 = added supplement star (no CCD data) from FK6/Hip/Tycho-2 data, and 2 stars added from high proper motion surveys
    # 8 = high proper motion solution in UCAC4, star not matched with PPMXL
    # 9 = high proper motion solution in UCAC4, discrepant PM to PPMXL (see documentation

    ra  = float(line[11:22])
    dec = float(line[23:33])

    # 3e) Additional photometry
    # -------------------------
    # The UCAC4 observational data are supplemented with 5-band photometry (B,V,
    # g,r,i) from the APASS project (Henden, private comm.) as well as with IR
    # photometry (J,H,K_s) from the Two Micron All Sky Survey, 2MASS (Skrutskie
    # et al. 2006).  In addition, magnitudes errors and some flags are provided.
    # For more details see http://www.aavso.org/apass  and
    # http://www.ipac.caltech.edu/2mass/releases/allsky/ .

    try:
        f_mag= float(line[63:69])
    except:
        f_mag = None

    try:
        a_mag = float(line[70:76])
    except:
        a_mag = None

    try:
        j_mag = float(line[174:180])
    except:
        j_mag = None

    try:
        h_mag = float(line[189:195])
    except:
        h_mag = None

    try:
        k_mag = float(line[204:210])
    except:
        k_mag = None

    try:
        b_mag = float(line[219:225])
    except:
        b_mag = None

    try:
        v_mag = float(line[230:236]) # visual magnitude
    except:
        v_mag = None

    try:
        g_mag = float(line[241:247])
    except:
        g_mag = None

    try:
        r_mag = float(line[252:258])
    except:
        r_mag = None

    try:
        i_mag = float(line[263:269])
    except:
        i_mag = None

    star = (ucac4_id, ot, ra, dec, f_mag, a_mag,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag )
    return star


def convert_from_ascii_to_sqlite(source_location, target_location):
    count = 0

    # create a database connection
    conn = create_sqlite_database(target_location)

    with open(source_location, "r") as f:
        # with codecs.open(source_location, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        number_of_stars = len(lines) - 1
        progress_factor = number_of_stars / progressbar_length

        # skip the first line with the header
        for line in lines[1:]:
            star = parse_ascii_line(line)

            add_star_to_sqlite(conn, star)
            count = count + 1

            if (count % progress_factor) == 0:
                sys.stdout.write(".")

    # close the database connection
    if conn:
        conn.close()

    return count


def convert_from_binary_to_sqlite(source_location, target_location):
    count = 0

    # create a database connection
    conn = create_sqlite_database(target_location)

    with open(source_location, "r") as f:
        # with codecs.open(source_location, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        number_of_stars = len(lines) - 1
        progress_factor = number_of_stars / progressbar_length

        # skip the first line with the header
        for line in lines[1:]:
            star = parse_ascii_line(line)

            add_star_to_sqlite(conn, star)
            count = count + 1

            if (count % progress_factor) == 0:
                sys.stdout.write(".")

    # close the database connection
    if conn:
        conn.close()

    return count


def do_conversion(args):

    # determine the requested conversion based on the prefix in the 'source' and 'target' parameters
    source_format = args.source.split(':')[0]
    source_location = args.source.split(':')[1]

    target_format = args.target.split(':')[0]
    target_location = args.target.split(':')[1]

    count = 0

    if target_format == 'sqlite':

        if source_format == 'ascii':
            count = convert_from_ascii_to_sqlite(source_location, target_location)

        if source_format == 'binary':
            count = convert_from_binary_to_sqlite(source_location, target_location)

    return count


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument("--source",
                        default="ascii:UCAC4_sample.txt",
                        help="ASCII file in UCAC4 format")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="format:location of the output. Format can be 'sqlite' or 'postgres'. The output is either a path or a database url")

    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 2 july 2022) ---")
    print("source : " + args.source)
    print("target : " + args.target)

    try:
        result = do_conversion(args)
        print(result)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main()


