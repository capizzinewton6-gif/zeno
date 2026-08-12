"""Database query helpers for Chemistry AI."""

import os
import sqlite3

DB_DIR = os.path.dirname(os.path.abspath(__file__))


def query(db_name, sql, params=()):
    """Run a SQL query against a database file and return rows."""
    path = os.path.join(DB_DIR, db_name)
    if not os.path.exists(path):
        return {"error": f"{db_name} not initialized. Run database.init_all()."}
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        return rows
    finally:
        conn.close()


def search_chemical(name):
    return query("chemicals_reagents.db",
                 "SELECT * FROM chemicals WHERE name LIKE ?", ("%" + name + "%",))

def search_reaction(name):
    return query("reaction_rules.db",
                 "SELECT * FROM reactions WHERE name LIKE ?", ("%" + name + "%",))

def search_spectrum(compound):
    return query("spectra_reference.db",
                 "SELECT * FROM spectra WHERE compound LIKE ?", ("%" + compound + "%",))

def search_hazard(chemical):
    return query("safety_hazards.db",
                 "SELECT * FROM hazards WHERE chemical LIKE ?", ("%" + chemical + "%",))

def list_solvents():
    return query("catalysts_solvents.db", "SELECT * FROM solvents")
