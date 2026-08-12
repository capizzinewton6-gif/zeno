"""File manager — manage MOL, SDF, CIF, JCAMP-DX, and FID files."""

import os
import json
import time


class FileManager:
    """Handle chemical data file formats."""

    def __init__(self, base_dir="chemical_files"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save_mol(self, name, smiles_or_molblock):
        path = os.path.join(self.base_dir, f"{name}.mol")
        with open(path, "w") as f:
            f.write(smiles_or_molblock)
        return {"saved": path, "format": "mol"}

    def save_sdf(self, name, records):
        """records: list of molblock strings."""
        path = os.path.join(self.base_dir, f"{name}.sdf")
        with open(path, "w") as f:
            for rec in records:
                f.write(rec + "\n$$$$\n")
        return {"saved": path, "format": "sdf", "n_records": len(records)}

    def save_jcamp(self, name, x, y, xunit="ppm", yunit="intensity", title=""):
        """Write a minimal JCAMP-DX file."""
        path = os.path.join(self.base_dir, f"{name}.jdx")
        lines = [
            f"##TITLE={title or name}",
            "##JCAMP-DX=5.01",
            f"##XUNITS={xunit}",
            f"##YUNITS={yunit}",
            "##NPOINTS=" + str(len(x)),
            "##XYDATA=(XY..XY)",
        ]
        for xi, yi in zip(x, y):
            lines.append(f"{xi} {yi}")
        lines.append("##END=")
        with open(path, "w") as f:
            f.write("\n".join(lines))
        return {"saved": path, "format": "jcamp-dx"}

    def save_cif(self, name, cell_params, atoms):
        """Minimal CIF writer. cell_params: (a,b,c,alpha,beta,gamma). atoms: list of (label,x,y,z)."""
        path = os.path.join(self.base_dir, f"{name}.cif")
        a, b, c, al, be, ga = cell_params
        lines = [
            f"data_{name}",
            f"_cell_length_a {a}", f"_cell_length_b {b}", f"_cell_length_c {c}",
            f"_cell_angle_alpha {al}", f"_cell_angle_beta {be}", f"_cell_angle_gamma {ga}",
            "_symmetry_space_group_name_H-M 'P 1'",
            "loop_",
            "_atom_site_label _atom_site_fract_x _atom_site_fract_y _atom_site_fract_z",
        ]
        for lbl, x, y, z in atoms:
            lines.append(f"{lbl} {x} {y} {z}")
        with open(path, "w") as f:
            f.write("\n".join(lines))
        return {"saved": path, "format": "cif"}

    def list_files(self):
        return [f for f in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, f))]

    def read_file(self, name):
        path = os.path.join(self.base_dir, name)
        if not os.path.exists(path):
            return {"error": "not found"}
        with open(path) as f:
            return {"content": f.read(), "format": os.path.splitext(name)[1].lstrip(".")}
