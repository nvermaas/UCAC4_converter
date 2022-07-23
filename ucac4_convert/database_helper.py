import os
import sqlite3
import psycopg2
from sqlite3 import Error

zone_stats = """
CREATE TABLE IF NOT EXISTS zones (
	zone integer PRIMARY KEY,
	nr_of_stars integer,
	accumulated_sum integer,
	max_dec float NOT NULL
);
"""

create_database_schema = """
CREATE DATABASE replace-with-database
"""

create_table_schema = """
CREATE TABLE replace-with-zone (
	zone integer NOT NULL,
	mpos1 integer PRIMARY KEY,
	ucac2 text,
	ot integer NOT NULL,
	ra float NOT NULL,
	dec float NOT NULL,
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

def open_sqlite_database(db_file, schema, remove_database):
    """ create a database connection to a SQLite database """

    if remove_database:
        try:
            os.remove(db_file)
        except OSError:
            pass

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            cursor.execute(schema)
        except Error as e:
            # database already exists, continue
            # print(e)
            pass

    except Error as e:
        print(e)
        if conn:
            conn.close()

    return conn


def open_postgres_database(args, database_name, schema):
    """ create a database connection to a Postgres database """


    conn = None
    try:
        # establishing the connection
        conn = psycopg2.connect(
            database=args.database,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )
        conn.autocommit = True

        # Creating a database
        cursor = conn.cursor()

        # first try to drop the database, to ensure that it doesn't exist before creating
        #try:
        #    cursor.execute("DROP DATABASE "+database_name)
        #except psycopg2.Error as e:
        #    # database already exists, continue
        #    print(e)

        try:
            cursor.execute("CREATE DATABASE "+database_name)
        except psycopg2.Error as e:
            # database already exists, continue
            # print(e)
            pass

        conn.close()

        # connect to the just created database
        # establishing the connection

        conn = psycopg2.connect(
            database=database_name,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )

        cursor = conn.cursor()
        conn.autocommit = True

        # create the table
        try:
            cursor.execute(schema)
        except psycopg2.Error as e:
            # table already exists, continue
            # print(e)
            pass

    except psycopg2.Error as e:
        print(e)
        if conn:
            conn.close()

    conn.commit()
    return conn


def add_zone_to_database(conn, zone):
    sql = ''' INSERT INTO zones(zone,nr_of_stars,accumulated_sum,max_dec)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, zone)
    conn.commit()


def add_star_to_sqlite(conn, table_name, star):
    base_sql = ''' INSERT INTO replace-with-zone(zone,mpos1,ucac2,ot,ra,dec,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    sql = base_sql.replace("replace-with-zone",table_name)
    cur = conn.cursor()
    try:
        cur.execute(sql, star)
        conn.commit()
    except Error as e:
        #print(e)
        print(str(star[1]) + ' already exists... continue')


def add_star_to_postgres(conn, table_name, star):
    base_sql = ''' INSERT INTO replace-with-zone(zone,mpos1,ucac2,ot,ra,dec,j_mag,h_mag,k_mag,b_mag,v_mag,g_mag,r_mag,i_mag)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
    sql = base_sql.replace("replace-with-zone",table_name)
    cur = conn.cursor()
    try:
        cur.execute(sql, star)
        conn.commit()
    except:
        print(str(star[1]) + ' already exists... continue')