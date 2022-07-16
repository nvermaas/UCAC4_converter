import os
import sqlite3
from sqlite3 import Error

ucac4_table = """
CREATE TABLE IF NOT EXISTS ucac4 (
	ucac4_id text PRIMARY KEY,
	ot integer NOT NULL,
	ra float NOT NULL,
	dec float NOT NULL,
    f_mag integer,
    a_mag integer,
    j_mag integer,
    h_mag integer,
    k_mag integer,
    b_mag integer,
    v_mag integer,
    g_mag integer,
    r_mag integer,
    i_mag integer
);
"""

def create_sqlite_database(db_file):
    """ create a database connection to a SQLite database """

    # remove existing file
    try:
        os.remove(db_file)
    except OSError:
        pass

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(ucac4_table)

    except Error as e:
        print(e)
        if conn:
            conn.close()

    return conn


def add_star_to_sqlite(conn, star):
    sql = ''' INSERT INTO ucac4(ucac4_id,ot,ra,dec,f_mag,a_mag,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, star)
    conn.commit()