import os, sys
import argparse

progressbar_length = 100

from ucac4_convert.sqlite_helper import create_sqlite_database, add_star_to_sqlite

def parse_line(line):
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


def do_conversion(args):

    # determine the requested conversion based on the prefix in the 'target' parameter
    target_format = args.target.split(':')[0]
    target_location = args.target.split(':')[1]

    try:

        if target_format == 'sqlite':
            conn = create_sqlite_database(target_location)

        elif target_format == 'postgres':
            pass
        else:
            count = -1
            raise Exception('Unknown target format: '+target_format)

        # open the source_file
        with open(args.source_file, "r") as f:
            lines = f.readlines()
            number_of_stars = len(lines)-1
            progress_factor = number_of_stars / progressbar_length

            count = 0

            # skip the first line with the header
            for line in lines[1:]:
                star = parse_line(line)

                if target_format == 'sqlite':
                    add_star_to_sqlite(conn, star)
                    count = count + 1

                    if (count % progress_factor) == 0:
                        sys.stdout.write(".")

    except Exception as error:
        print(error)

    finally:
        # close the database if needed
        if target_format == 'sqlite':
            if conn:
                conn.close()
    return count


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument("--source_file",
                        default="UCAC4_sample.txt",
                        help="ASCII file in UCAC4 format")
    parser.add_argument("--target",
                        default="mysqlite:UCAC4_sample.sqlite3",
                        help="format:location of the output. Format can be 'sqlite' or 'postgres'. The output is either a path or a database url")

    args = args = parser.parse_args()

    print("--- UCAC4 Converter (version 2 july 2022) ---")
    print("source_file: " + args.source_file)
    print("target     : " + args.target)

    result = do_conversion(args)
    print(result)

if __name__ == '__main__':
    main()


