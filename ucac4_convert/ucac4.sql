-- ucac4 table
CREATE TABLE IF NOT EXISTS ucac4 (
	ucac4_id integer PRIMARY KEY,
	object_type text NOT NULL,
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