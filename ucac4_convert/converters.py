import os, sys
import struct

from ucac4_convert.database_helper import \
    create_sqlite_database,\
    create_postgres_database, \
    add_star_to_sqlite, \
    add_star_to_postgres, \
    add_zone_to_database, \
    create_database_schema, \
    create_table_schema, \
    zone_stats

progressbar_length = 100

def convert_zonestats_from_ascii_to_sqlite(source_location, target_location):
    """
    Convert the index file with statistics per zone to a sqlite database
    https://cdsarc.cds.unistra.fr/ftp/I/322A/UCAC4/u4i/zone_stats

    Statistics number of stars in UCAC4 zones.

     zn     = zone number
     nsz    = number of stars in zone
     nss    = accumulated sum of stars this and prev.zones
     nopmz  = numb. of stars in zone without proper motion
     no2mz  = numb. of stars in zone without 2MASS match
     max_dec= largest declination of zone

     zn       nsz       nss     nopmz     no2mz   max_dec
    -----------------------------------------------------
      1       206       206         5         3    -89.80
      2       660       866         8        17    -89.60
      3      1143      2009        16        42    -89.40
      4      1613      3622        21        72    -89.20
      ...
    """

    def _parse_ascii_line(line):

        zone_nr = int(line[0:3])
        nr_of_stars = int(line[5:13])
        accumulated_sum = int(line[15:23])
        max_dec = float(line[47:53])

        # save the zone
        zone = (zone_nr, nr_of_stars, accumulated_sum, max_dec)

        return zone

    count = 0

    # create a database connection
    conn = create_sqlite_database(target_location, zone_stats)

    with open(source_location, "r") as f:
        lines = f.readlines()

        # skip the lines with header and documentation
        for line in lines[11:]:
            if not "-----" in line:
                zone = _parse_ascii_line(line)

                add_zone_to_database(conn, zone)
                count = count + 1

    # close the database connection
    if conn:
        conn.close()

    return count



def convert_from_ascii_to_database(source_location, target_location):

    def _parse_ascii_line(line):
        # https://irsa.ipac.caltech.edu/data/UCAC4/readme_u4.txt
        zone = 1
        ucac4_id = line[0:10]
        mpos1 = int(line[129:138])
        ucac2 = line[139:149]

        ot = int(line[84:85])

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

        ra = float(line[11:22])
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
            f_mag = round(float(line[63:69]) * 1000)
        except:
            f_mag = None

        try:
            a_mag = round(float(line[70:76]) * 1000)
        except:
            a_mag = None

        try:
            j_mag = round(float(line[174:180]) * 1000)
        except:
            j_mag = None

        try:
            h_mag = round(float(line[189:195]) * 1000)
        except:
            h_mag = None

        try:
            k_mag = round(float(line[204:210]) * 1000)
        except:
            k_mag = None

        try:
            b_mag = round(float(line[219:225]) * 1000)
        except:
            b_mag = None

        try:
            v_mag = round(float(line[230:236]) * 1000)  # visual magnitude
        except:
            v_mag = None

        try:
            g_mag = round(float(line[241:247]) * 1000)
        except:
            g_mag = None

        try:
            r_mag = round(float(line[252:258]) * 1000)
        except:
            r_mag = None

        try:
            i_mag = round(float(line[263:269]) * 1000)
        except:
            i_mag = None

        # save the star
        star = (zone, mpos1, ucac2, ot, ra, dec, j_mag, h_mag, k_mag, b_mag, v_mag, g_mag, r_mag, i_mag)

        # star = (ucac4_id,ot,ra,dec,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag )
        return star

    count = 0

    # create a database connection
    conn = create_sqlite_database(target_location, create_table_schema)

    with open(source_location, "r") as f:
        # with codecs.open(source_location, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        number_of_stars = len(lines) - 1
        progress_factor = round(number_of_stars / progressbar_length)

        # skip the first line with the header
        for line in lines[1:]:
            star = _parse_ascii_line(line)

            add_star_to_database(conn, star)
            count = count + 1

            if (count % progress_factor) == 0:
                sys.stdout.write(".")

    # close the database connection
    if conn:
        conn.close()

    return count


def convert_from_binary_to_database(args, source_location, target_location, target_format):
    """
            col byte item   fmt unit       explanation                            notes
        ---------------------------------------------------------------------------
         1  1- 3 ra     I*4 mas        right ascension at  epoch J2000.0 (ICRS) (1)
         2  5- 8 spd    I*4 mas        south pole distance epoch J2000.0 (ICRS) (1)
         3  9-10 magm   I*2 millimag   UCAC fit model magnitude                 (2)
         4 11-12 maga   I*2 millimag   UCAC aperture  magnitude                 (2)
         5 13    sigmag I*1 1/100 mag  error of UCAC magnitude                  (3)
         6 14    objt   I*1            object type                              (4)
         7 15    cdf    I*1            combined double star flag                (5)
                 15 bytes
         8 16    sigra  I*1 mas        s.e. at central epoch in RA (*cos Dec)   (6)
         9 17    sigdc  I*1 mas        s.e. at central epoch in Dec             (6)
        10 18    na1    I*1            total # of CCD images of this star
        11 19    nu1    I*1            # of CCD images used for this star       (7)
        12 20    cu1    I*1            # catalogs (epochs) used for proper motions
                  5 bytes
        13 21-22 cepra  I*2 0.01 yr    central epoch for mean RA, minus 1900
        14 23-24 cepdc  I*2 0.01 yr    central epoch for mean Dec,minus 1900
        15 25-26 pmrac  I*2 0.1 mas/yr proper motion in RA*cos(Dec)             (8)
        16 27-28 pmdc   I*2 0.1 mas/yr proper motion in Dec
        17 29    sigpmr I*1 0.1 mas/yr s.e. of pmRA * cos Dec                   (9)
        18 30    sigpmd I*1 0.1 mas/yr s.e. of pmDec                            (9)
                 10 bytes
        19 31-34 pts_key I*4           2MASS unique star identifier            (10)
        20 35-36 j_m    I*2 millimag   2MASS J  magnitude
        21 37-38 h_m    I*2 millimag   2MASS H  magnitude
        22 39-40 k_m    I*2 millimag   2MASS K_s magnitude
        23 41    icqflg I*1            2MASS cc_flg*10 + ph_qual flag for J    (11)
        24 42     (2)   I*1            2MASS cc_flg*10 + ph_qual flag for H    (11)
        25 43     (3)   I*1            2MASS cc_flg*10 + ph_qual flag for K_s  (11)
        26 44    e2mpho I*1 1/100 mag  error 2MASS J   magnitude               (12)
        27 45     (2)   I*1 1/100 mag  error 2MASS H   magnitude               (12)
        28 46     (3)   I*1 1/100 mag  error 2MASS K_s magnitude               (12)
                 16 bytes
        29 47-48 apasm  I*2 millimag   B magnitude from APASS                  (13)
        30 49-50  (2)   I*2 millimag   V magnitude from APASS                  (13)
        31 51-52  (3)   I*2 millimag   g magnitude from APASS                  (13)
        32 53-54  (4)   I*2 millimag   r magnitude from APASS                  (13)
        33 55-56  (5)   I*2 millimag   i magnitude from APASS                  (13)
        34 57    apase  I*1 1/100 mag  error of B magnitude from APASS         (14)
        35 58     (2)   I*1 1/100 mag  error of V magnitude from APASS         (14)
        36 59     (3)   I*1 1/100 mag  error of g magnitude from APASS         (14)
        37 60     (4)   I*1 1/100 mag  error of r magnitude from APASS         (14)
        38 61     (5)   I*1 1/100 mag  error of i magnitude from APASS         (14)
        39 62    gcflg  I*1            Yale SPM g-flag*10  c-flag              (15)
                 16 bytes
        40 63-66 icf(1) I*4            FK6-Hipparcos-Tycho source flag         (16)
        41       icf(2) ..             AC2000       catalog match flag         (17)
        42       icf(3) ..             AGK2 Bonn    catalog match flag         (17)
        43       icf(4) ..             AKG2 Hamburg catalog match flag         (17)
        44       icf(5) ..             Zone Astrog. catalog match flag         (17)
        45       icf(6) ..             Black Birch  catalog match flag         (17)
        46       icf(7) ..             Lick Astrog. catalog match flag         (17)
        47       icf(8) ..             NPM  Lick    catalog match flag         (17)
        48       icf(9) ..             SPM  YSJ1    catalog match flag         (17)
                  4 bytes
        49 67    leda   I*1            LEDA galaxy match flag                  (18)
        50 68    x2m    I*1            2MASS extend.source flag                (19)
        51 69-72 rnm    I*4            unique star identification number       (20)
        52 73-74 zn2    I*2            zone number of UCAC2 (0 = no match)     (21)
        53 75-78 rn2    I*4            running record number along UCAC2 zone  (21)
                 12 bytes
        ---------------------------------------------------------------------------
                 78 = total number of bytes per star record

    """
    zone = int(source_location[-3:])
    count = 0

    # create a database connection
    conn = None

    # construct the correct database schema for this zone

    table_name = "z"+target_location[-3:]

    if target_format == 'sqlite':
        # target_location: ../z001.sqlite3
        schema = create_table_schema.replace("replace-with-zone", table_name)
        conn = create_sqlite_database(target_location, schema)

    elif target_format == 'postgres':
        # target_location: ucac4.z002
        db_table_names = target_location.split('.')
        database_name = db_table_names[0]
        table_name = db_table_names[1]
        schema = create_table_schema.replace("replace-with-zone", table_name)
        conn = create_postgres_database(args, database_name, schema)

    # this assumes a naming convention of binary files like z001,z002,z???
    # and the record size of 78 bytes per star
    number_of_stars = round(os.path.getsize(source_location) / 78)

    with open(source_location, "rb") as f:
        progress_factor = round(number_of_stars / progressbar_length)
        pointer = 0

        while count < number_of_stars:

            # ra,dec
            size = 8
            f.seek(pointer)
            bytes = f.read(size)

            # https://docs.python.org/3/library/struct.html
            ra_mas, spd_mas = struct.unpack('<II', bytes)  # expected: 4117825, 292970

            # convert from milliarcseconds and distance from the south pole
            ra = ra_mas / 3600000
            dec = -90 + (spd_mas / 3600000)

            # advance pointer, and skip 5 bytes
            pointer = pointer + size + 5

            # object_type
            size = 1
            f.seek(pointer)
            bytes = f.read(size)
            try:
                ot = struct.unpack('<B', bytes)[0]
            except:
                ot = 0

            # advance pointer, and skip 20 bytes
            pointer = pointer + size + 20

            # j,h,k magnitude
            size = 6
            f.seek(pointer)
            bytes = f.read(size)

            # https://docs.python.org/3/library/struct.html
            j_mag, h_mag, k_mag = struct.unpack('<hhh', bytes)
            j_mag = None if j_mag == 20000 else j_mag
            h_mag = None if h_mag == 20000 else h_mag
            k_mag = None if k_mag == 20000 else k_mag

            # advance pointer, and skip 6 bytes
            pointer = pointer + size + 6

            # b,v,g,r,i magnitude
            size = 10
            f.seek(pointer)
            bytes = f.read(size)

            # https://docs.python.org/3/library/struct.html
            b_mag, v_mag, g_mag, r_mag, i_mag = struct.unpack('<hhhhh', bytes)
            b_mag = None if b_mag == 20000 else b_mag
            v_mag = None if v_mag == 20000 else v_mag
            g_mag = None if g_mag == 20000 else g_mag
            r_mag = None if r_mag == 20000 else r_mag
            i_mag = None if i_mag == 20000 else i_mag

            # advance pointer, and skip 12 bytes
            pointer = pointer + size + 12

            # id
            size = 10
            f.seek(pointer)
            bytes = f.read(size)

            # https://docs.python.org/3/library/struct.html
            mpos1, zone2, rec = struct.unpack('<IhI', bytes)

            ucac2 = str(zone2).zfill(3) + '-' + str(rec).zfill(6)
            ucac2 = None if ucac2 == "000-000000" else ucac2

            # advance pointer
            pointer = pointer + size

            # save the star
            star = (zone, mpos1, ucac2, ot, ra, dec, j_mag, h_mag, k_mag, b_mag, v_mag, g_mag, r_mag, i_mag)

            if target_format == 'sqlite':
                add_star_to_sqlite(conn, table_name, star)
            elif target_format == 'postgres':
                add_star_to_postgres(conn, table_name, star)

            count = count + 1

            if (count % progress_factor) == 0:
                sys.stdout.write(".")

    # close the database connection
    if conn:
        conn.close()

    return count


class UCAC4_Converter:

    def __init__(self, args):
        """
        Constructor.
        :param args: the dict of parameters to the application
        """
        self.args = args
        self.source_format = args.source.split(':')[0]
        self.source_location = args.source.split(':')[1]

        self.target_format = args.target.split(':')[0]
        self.target_location = args.target.split(':')[1]


    def convert(self):

        if self.target_format == 'sqlite':

            if self.source_format == 'ascii_zonestats':
                count = convert_zonestats_from_ascii_to_sqlite(self.source_location, self.target_location)

            elif self.source_format == 'ascii':
                count = convert_from_ascii_to_database(self.source_location, self.target_location)

            elif self.source_format == 'binary':
                count = convert_from_binary_to_database(self.args, self.source_location, self.target_location, self.target_format)

        if self.target_format == 'postgres':

            if self.source_format == 'binary':
                count = convert_from_binary_to_database(self.args, self.source_location, self.target_location, self.target_format)
