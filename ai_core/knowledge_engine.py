"""Knowledge engine — chemical ontology and reaction transformation knowledge graph."""

import logging

logger = logging.getLogger(__name__)


class KnowledgeEngine:
    """A lightweight chemical ontology and reaction transformation graph."""

    def __init__(self):
        self.functional_groups = {
            "alcohol": {"smarts": "[#6][OX2H]"},
            "alkene": {"smarts": "[#6]=[#6]"},
            "alkyne": {"smarts": "[#6]#[#6]"},
            "aldehyde": {"smarts": "[CX3H1](=O)"},
            "ketone": {"smarts": "[#6][CX3](=O)[#6]"},
            "carboxylic_acid": {"smarts": "[CX3](=O)[OX2H1]"},
            "ester": {"smarts": "[#6][CX3](=O)[OX2H0]"},
            "amine": {"smarts": "[NX3;H2,H1,H0]"},
            "amide": {"smarts": "[CX3](=O)[NX3]"},
            "nitrile": {"smarts": "[CX2]#[NX1]"},
            "halide": {"smarts": "[#6][F,Cl,Br,I]"},
            "nitro": {"smarts": "[$([NX3](=O)=O)]"},
        }

        self.name_reactions = {
            "Suzuki": {"category": "coupling", "functional_group": "halide", "product_fg": "biaryl"},
            "Grignard": {"category": "addition", "functional_group": "halide", "product_fg": "alcohol"},
            "Friedel-Crafts": {"category": "acylation/alkylation", "functional_group": "halide", "product_fg": "aromatic"},
            "Diels-Alder": {"category": "cycloaddition", "functional_group": "alkene", "product_fg": "cyclohexene"},
            "Wittig": {"category": "olefination", "functional_group": "aldehyde/ketone", "product_fg": "alkene"},
            "Haber-Bosch": {"category": "industrial", "functional_group": None, "product_fg": "ammonia"},
            "Esterification (Fischer)": {"category": "condensation", "functional_group": "carboxylic_acid", "product_fg": "ester"},
            "Hydrogenation": {"category": "reduction", "functional_group": "alkene/alkyne", "product_fg": "alkane"},
        }

        self.element_data = {
            "H": {"z": 1, "mass": 1.008},
            "C": {"z": 6, "mass": 12.011},
            "N": {"z": 7, "mass": 14.007},
            "O": {"z": 8, "mass": 15.999},
            "F": {"z": 9, "mass": 18.998},
            "Na": {"z": 11, "mass": 22.990},
            "Cl": {"z": 17, "mass": 35.45},
            "Br": {"z": 35, "mass": 79.904},
            "I": {"z": 53, "mass": 126.904},
            "P": {"z": 15, "mass": 30.974},
            "S": {"z": 16, "mass": 32.06},
        }

    def lookup_functional_group(self, name):
        return self.functional_groups.get(name)

    def lookup_reaction(self, name):
        return self.name_reactions.get(name)

    def list_reactions(self):
        return list(self.name_reactions.keys())

    def list_functional_groups(self):
        return list(self.functional_groups.keys())

    def element(self, symbol):
        return self.element_data.get(symbol)
