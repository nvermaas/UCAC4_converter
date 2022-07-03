import os
import sqlite3
from sqlite3 import Error

ucac4_table = """
CREATE TABLE IF NOT EXISTS ucac4 (
	ucac4_id text PRIMARY KEY,
	ot integer NOT NULL,
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

    # remove existing file
    os.remove(db_file)

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