import argparse
import sqlite3
from sqlite3 import Error

ucac4_table = """
CREATE TABLE IF NOT EXISTS ucac4 (
	ucac4_id integer PRIMARY KEY,
	ot text NOT NULL,
	ra float NOT NULL,
	dec float NOT NULL,
    f_mag float,
    a_mag float,
    j_mag float,
    h_mag float,
    k_mag float,
    b_mag float,
    v_mag float,
    g_mag float,
    r_mag float,
    i_mag float
);
"""

def create_sqlite_database(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(ucac4_table)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return conn


def add_star_to_sqlite(conn, star):
    sql = ''' INSERT INTO ucac4(ucac4_id,ot,ra,dec,f_mag,a_mag,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, star)
    conn.commit()


def parse_line(line):
    # https://irsa.ipac.caltech.edu/data/UCAC4/readme_u4.txt
    record = {}

    record['ucac4_id'] = line[0:10]
    record['ot'] = line[84:85]

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

    record['ra']  = line[11:22]
    record['dec'] = line[23:33]

    # 3e) Additional photometry
    # -------------------------
    # The UCAC4 observational data are supplemented with 5-band photometry (B,V,
    # g,r,i) from the APASS project (Henden, private comm.) as well as with IR
    # photometry (J,H,K_s) from the Two Micron All Sky Survey, 2MASS (Skrutskie
    # et al. 2006).  In addition, magnitudes errors and some flags are provided.
    # For more details see http://www.aavso.org/apass  and
    # http://www.ipac.caltech.edu/2mass/releases/allsky/ .

    record['f_mag'] = line[63:69]
    record['a_mag'] = line[70:76]
    record['j_mag'] = line[174:180]
    record['h_mag'] = line[189:195]
    record['k_mag'] = line[204:210]
    record['b_mag'] = line[219:225]
    record['v_mag'] = line[230:236] # visual magnitude
    record['g_mag'] = line[241:247]
    record['r_mag'] = line[252:258]
    record['i_mag'] = line[263:269]

    return record



def convert_to_postgres(source_file, location):
    result = 0
    return result


def do_conversion(args):

    # determine the requested conversion based on the prefix in the 'target' parameter
    target_format = args.target.split(':')[0]
    target_location = args.target.split(':')[1]

    if target_format == 'sqlite':
        conn = create_sqlite_database(target_location)

    elif target_format == 'postgres':
        pass
    else:
        result = -1
        print('unknown target format: '+target_format)

    # open the source_file
    with open(args.source_file, "r") as f:
        # skip the header
        line = f.readline()
        count = 0

        while line != '':  # The EOF char is an empty string
            # 451-133336|359.2517683+00.1305667  15  16   22 2001.15 2001.45|13.301 13.273 0.06 | 0  0|  8   8   2|   +10.1     -2.7  1.9  2.3|102165057 181-173041             |1098500800 12.162 0.02:05 11.827 0.02:05 11.764 0.02:05|13.971:.02 13.327:.05 13.649:.02 13.164:.06 13.050:.04|00.000000010|  0   0
            line = f.readline()

            count = count + 1
            star = parse_line(line)


            if target_format == 'sqlite':
                # add record
                add_star_to_sqlite(conn, star)

    return result


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


