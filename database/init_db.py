"""Database initialization for Chemistry AI.

Creates SQLite databases for:
- chemicals_reagents.db  (physical properties, densities, pKas, boiling points)
- reaction_rules.db      (transformation rules, name reactions, FG compatibility)
- spectra_reference.db   (indexed 1H/13C NMR, FT-IR, MS libraries)
- safety_hazards.db      (GHS hazards, incompatible pairs, regulatory watchlists)
- catalysts_solvents.db  (organocatalytic, transition-metal, green solvent properties)

Run: python -m database.init_db   (or python database/init_db.py)
"""

import os
import sqlite3

DB_DIR = os.path.dirname(os.path.abspath(__file__))


def _connect(name):
    return sqlite3.connect(os.path.join(DB_DIR, name))


def init_chemicals():
    conn = _connect("chemicals_reagents.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS chemicals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, formula TEXT, cas TEXT, mw REAL,
        density_g_mL REAL, bp_C REAL, mp_C REAL, pKa REAL, solubility TEXT)""")
    c.executemany("INSERT INTO chemicals(name,formula,cas,mw,density_g_mL,bp_C,mp_C,pKa) VALUES (?,?,?,?,?,?,?,?)",
                  [("water", "H2O", "7732-18-5", 18.015, 1.000, 100.0, 0.0, 15.7),
                   ("ethanol", "C2H6O", "64-17-5", 46.069, 0.789, 78.4, -114.1, 15.9),
                   ("acetic acid", "C2H4O2", "64-19-7", 60.052, 1.049, 118.1, 16.6, 4.76),
                   ("sulfuric acid", "H2SO4", "7664-93-9", 98.079, 1.830, 337.0, 10.0, -3.0),
                   ("sodium hydroxide", "NaOH", "1310-73-2", 40.000, 2.130, 1388.0, 318.0, None)])
    conn.commit()
    conn.close()


def init_reactions():
    conn = _connect("reaction_rules.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, category TEXT, reactants TEXT, products TEXT,
        functional_group TEXT, conditions TEXT)""")
    c.executemany("INSERT INTO reactions(name,category,reactants,products,functional_group,conditions) VALUES (?,?,?,?,?,?)",
                  [("Suzuki", "coupling", "aryl halide+boronic acid", "biaryl", "halide", "Pd(0), base, 80C"),
                   ("Grignard", "addition", "RMgX+carbonyl", "alcohol", "halide", "anhydrous THF, 0C"),
                   ("Fischer esterification", "condensation", "acid+alcohol", "ester", "carboxylic_acid", "H2SO4 cat., reflux"),
                   ("Diels-Alder", "cycloaddition", "diene+dienophile", "cyclohexene", "alkene", "heat"),
                   ("Wittig", "olefination", "aldehyde+ylide", "alkene", "aldehyde", "base, THF")])
    conn.commit()
    conn.close()


def init_spectra():
    conn = _connect("spectra_reference.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS spectra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        compound TEXT, technique TEXT, peak_data TEXT)""")
    c.executemany("INSERT INTO spectra(compound,technique,peak_data) VALUES (?,?,?)",
                  [("ethanol", "1H NMR", "1.19(t,3H);3.58(q,2H);2.6(s,1H)"),
                   ("acetone", "13C NMR", "30.6;206.7"),
                   ("benzene", "FT-IR", "3030;1479;673"),
                   ("aspirin", "MS", "180.0423[M]+;138;120;92")])
    conn.commit()
    conn.close()


def init_safety():
    conn = _connect("safety_hazards.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS hazards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical TEXT, ghs_pictograms TEXT, signal_word TEXT, h_statements TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS incompatible_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, reagent_a TEXT, reagent_b TEXT, hazard TEXT)""")
    c.executemany("INSERT INTO hazards(chemical,ghs_pictograms,signal_word,h_statements) VALUES (?,?,?,?)",
                  [("sulfuric acid", "GHS05", "Danger", "H314,H290"),
                   ("ethanol", "GHS02,GHS07", "Danger", "H225,H319"),
                   ("toluene", "GHS02,GHS07,GHS08", "Danger", "H225,H304,H315,H336")])
    c.executemany("INSERT INTO incompatible_pairs(reagent_a,reagent_b,hazard) VALUES (?,?,?)",
                  [("oxidizers", "flammables", "fire/explosion"),
                   ("cyanides", "acids", "HCN gas"),
                   ("hypochlorite", "ammonia", "chloramine gas")])
    conn.commit()
    conn.close()


def init_catalysts_solvents():
    conn = _connect("catalysts_solvents.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS catalysts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, typical_rxn TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS solvents (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, bp_C REAL, polarity TEXT, green_score INTEGER)""")
    c.executemany("INSERT INTO catalysts(name,category,typical_rxn) VALUES (?,?,?)",
                  [("Pd(PPh3)4", "transition-metal", "Suzuki coupling"),
                   ("Pd/C", "transition-metal", "hydrogenation"),
                   ("L-proline", "organocatalyst", "aldol"),
                   ("Grubbs II", "transition-metal", "olefin metathesis")])
    c.executemany("INSERT INTO solvents(name,bp_C,polarity,green_score) VALUES (?,?,?,?)",
                  [("water", 100.0, "high", 10),
                   ("ethanol", 78.4, "medium", 9),
                   ("ethyl acetate", 77.1, "medium", 7),
                   ("dichloromethane", 40.0, "low", 3),
                   ("hexanes", 69.0, "low", 4)])
    conn.commit()
    conn.close()


def init_all():
    init_chemicals()
    init_reactions()
    init_spectra()
    init_safety()
    init_catalysts_solvents()
    return {"status": "ok", "databases": [
        "chemicals_reagents.db", "reaction_rules.db", "spectra_reference.db",
        "safety_hazards.db", "catalysts_solvents.db"]}


if __name__ == "__main__":
    print(init_all())
