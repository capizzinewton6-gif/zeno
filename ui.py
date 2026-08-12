"""Text-GUI user interface and interaction for Biology AI.

This module builds a tkinter desktop GUI that exposes the full agent suite,
capability modules, calculations, simulations, and biosafety screening. All
simulations are run on the user interface (rendered as plots/tables in the UI).
"""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BiologyUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Biology AI - Autonomous Laboratory Assistant")
        self.root.geometry("1280x820")
        self.root.minsize(960, 600)

        # Lazy-load agents in a background thread so the GUI appears instantly
        self.agents: dict = {}
        self._load_thread = threading.Thread(target=self._load_agents, daemon=True)
        self._load_thread.start()

        self._build_layout()

    # ------------------------------------------------------------------ build
    def _build_layout(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self._tab_chat = ttk.Frame(self.notebook)
        self._tab_tools = ttk.Frame(self.notebook)
        self._tab_genetics = ttk.Frame(self.notebook)
        self._tab_calc = ttk.Frame(self.notebook)
        self._tab_sim = ttk.Frame(self.notebook)
        self._tab_biosafety = ttk.Frame(self.notebook)
        self._tab_status = ttk.Frame(self.notebook)

        self.notebook.add(self._tab_chat, text="🧬 AI Assistant")
        self.notebook.add(self._tab_tools, text="🧪 Bio Tools")
        self.notebook.add(self._tab_genetics, text="🧻 Genetic Engineering")
        self.notebook.add(self._tab_calc, text="🧮 Calculations")
        self.notebook.add(self._tab_sim, text="📊 Simulations")
        self.notebook.add(self._tab_biosafety, text="🛡️ Biosafety")
        self.notebook.add(self._tab_status, text="ℹ️ Status")

        self._build_chat_tab()
        self._build_tools_tab()
        self._build_genetics_tab()
        self._build_calc_tab()
        self._build_sim_tab()
        self._build_biosafety_tab()
        self._build_status_tab()

    # ------------------------------------------------------------------ chat
    def _build_chat_tab(self):
        frame = self._tab_chat
        top = ttk.LabelFrame(frame, text="Ask the Biology AI")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Prompt:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.chat_input = tk.Text(top, height=4, width=100)
        self.chat_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        top.columnconfigure(1, weight=1)

        btns = ttk.Frame(top)
        btns.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(btns, text="Ask (route)", command=self._on_ask_route).pack(side="left", padx=2)
        ttk.Button(btns, text="Free-form reason", command=self._on_ask_reason).pack(side="left", padx=2)
        ttk.Button(btns, text="Clear", command=lambda: self.chat_output.delete("1.0", "end")).pack(side="left", padx=2)

        ttk.Label(top, text="Tip: routing selects a domain module; free-form uses the Gemini engine directly.").grid(
            row=2, column=1, padx=5, pady=2, sticky="w")

        output_frame = ttk.LabelFrame(frame, text="Response")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat_output = scrolledtext.ScrolledText(output_frame, wrap="word", font=("Consolas", 10))
        self.chat_output.pack(fill="both", expand=True, padx=5, pady=5)

    def _on_ask_route(self):
        q = self.chat_input.get("1.0", "end").strip()
        if not q:
            return
        self._append_chat(">> routed query:\n" + q + "\n")
        self._run_async(lambda: self._route(q))

    def _on_ask_reason(self):
        q = self.chat_input.get("1.0", "end").strip()
        if not q:
            return
        self._append_chat(">> free-form reasoning:\n" + q + "\n")
        self._run_async(lambda: self._reason(q))

    def _route(self, q):
        try:
            agent = self.agents.get("biology") or self._wait_agent("biology")
            result = agent.route(q)
        except Exception as e:
            result = f"[ERROR] {e}"
        self._append_chat("Biology Agent:\n" + str(result) + "\n" + "-" * 60 + "\n")

    def _reason(self, q):
        try:
            ai = self._get_ai()
            result = ai.reason(q)
        except Exception as e:
            result = f"[ERROR] {e}"
        self._append_chat("AI Engine:\n" + str(result) + "\n" + "-" * 60 + "\n")

    # ------------------------------------------------------------------ tools
    def _build_tools_tab(self):
        frame = self._tab_tools
        self._build_sequence_panel(frame)

    def _build_sequence_panel(self, frame):
        top = ttk.LabelFrame(frame, text="Sequence Analysis (molecular biology)")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Sequence:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.seq_input = tk.Text(top, height=3, width=80)
        self.seq_input.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Second seq (for alignment):").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.seq_input2 = tk.Text(top, height=2, width=80)
        self.seq_input2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

        btns = ttk.Frame(top)
        btns.grid(row=2, column=1, columnspan=3, sticky="w", pady=5)
        ttk.Button(btns, text="GC%", command=self._tool_gc).pack(side="left", padx=2)
        ttk.Button(btns, text="Translate", command=self._tool_translate).pack(side="left", padx=2)
        ttk.Button(btns, text="Reverse complement", command=self._tool_revcomp).pack(side="left", padx=2)
        ttk.Button(btns, text="Global align", command=self._tool_align_global).pack(side="left", padx=2)
        ttk.Button(btns, text="Local align", command=self._tool_align_local).pack(side="left", padx=2)
        ttk.Button(btns, text="Restriction map", command=self._tool_restriction).pack(side="left", padx=2)

        out_frame = ttk.LabelFrame(frame, text="Result")
        out_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.tools_output = scrolledtext.ScrolledText(out_frame, wrap="word", font=("Consolas", 10))
        self.tools_output.pack(fill="both", expand=True, padx=5, pady=5)

    def _tool_gc(self):
        seq = self._get_seq()
        if not seq:
            return
        from biology.molecular import MolecularModule
        self._set_tools_output(f"GC content: {MolecularModule.gc_content(seq):.2f}%\n"
                                f"Length: {len(seq)} bp")

    def _tool_translate(self):
        seq = self._get_seq()
        if not seq:
            return
        from biology.molecular import MolecularModule
        prot, stops = MolecularModule.translate(seq)
        self._set_tools_output(f"Protein ({len(prot)} aa):\n{prot}\n\nStop codons: {stops}")

    def _tool_revcomp(self):
        seq = self._get_seq()
        if not seq:
            return
        from biology.molecular import MolecularModule
        self._set_tools_output(f"Reverse complement:\n{MolecularModule.reverse_complement(seq)}")

    def _tool_align_global(self):
        s1, s2 = self._get_two_seqs()
        if not (s1 and s2):
            return
        from calculations.sequence_alignment import needleman_wunsch
        score, a1, a2 = needleman_wunsch(s1, s2)
        self._set_tools_output(f"Needleman-Wunsch (global) score: {score}\n\n{s1} -> {a1}\n{s2} -> {a2}")

    def _tool_align_local(self):
        s1, s2 = self._get_two_seqs()
        if not (s1 and s2):
            return
        from calculations.sequence_alignment import smith_waterman
        score, a1, a2 = smith_waterman(s1, s2)
        self._set_tools_output(f"Smith-Waterman (local) score: {score}\n\n{s1} -> {a1}\n{s2} -> {a2}")

    def _tool_restriction(self):
        seq = self._get_seq()
        if not seq:
            return
        from genetic_engineering.plasmid_builder import PlasmidBuilder
        self._set_tools_output(json.dumps(PlasmidBuilder().map_sites(seq), indent=2))

    # -------------------------------------------------------------- genetics
    def _build_genetics_tab(self):
        frame = self._tab_genetics
        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True, padx=5, pady=5)

        self._build_crispr_tab(nb)
        self._build_primer_tab(nb)
        self._build_plasmid_tab(nb)
        self._build_codon_tab(nb)

    def _build_crispr_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="CRISPR gRNA")
        ttk.Label(f, text="Target sequence:").pack(anchor="w", padx=10, pady=(10, 0))
        self.crispr_input = tk.Text(f, height=4, width=100)
        self.crispr_input.pack(fill="x", padx=10, pady=5)
        ttk.Label(f, text="PAM:").pack(anchor="w", padx=10)
        self.crispr_pam = tk.StringVar(value="NGG")
        ttk.Entry(f, textvariable=self.crispr_pam, width=10).pack(anchor="w", padx=10)
        ttk.Label(f, text="Cas:").pack(anchor="w", padx=10)
        self.crispr_cas = tk.StringVar(value="SpCas9")
        ttk.Entry(f, textvariable=self.crispr_cas, width=15).pack(anchor="w", padx=10)
        ttk.Button(f, text="Design gRNA", command=self._design_crispr).pack(anchor="w", padx=10, pady=10)
        self.crispr_out = scrolledtext.ScrolledText(f, height=12, font=("Consolas", 10))
        self.crispr_out.pack(fill="both", expand=True, padx=10, pady=5)

    def _design_crispr(self):
        seq = self.crispr_input.get("1.0", "end").strip().replace(" ", "").upper()
        if not seq:
            return
        from genetic_engineering.crispr_designer import CRISPRDesigner
        result = CRISPRDesigner().design_grna(seq, self.crispr_pam.get(), self.crispr_cas.get())
        self.crispr_out.delete("1.0", "end")
        self.crispr_out.insert("end", json.dumps(result, indent=2, default=str))

    def _build_primer_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="PCR Primers")
        ttk.Label(f, text="Template sequence:").pack(anchor="w", padx=10, pady=(10, 0))
        self.primer_input = tk.Text(f, height=4, width=100)
        self.primer_input.pack(fill="x", padx=10, pady=5)
        row = ttk.Frame(f); row.pack(fill="x", padx=10)
        ttk.Label(row, text="Product size (bp):").pack(side="left")
        self.primer_size = tk.IntVar(value=500)
        ttk.Entry(row, textvariable=self.primer_size, width=8).pack(side="left", padx=5)
        ttk.Button(f, text="Design primers", command=self._design_primers).pack(anchor="w", padx=10, pady=10)
        self.primer_out = scrolledtext.ScrolledText(f, height=12, font=("Consolas", 10))
        self.primer_out.pack(fill="both", expand=True, padx=10, pady=5)

    def _design_primers(self):
        seq = self.primer_input.get("1.0", "end").strip().replace(" ", "").upper()
        if not seq:
            return
        from genetic_engineering.primer_designer import PrimerDesigner
        result = PrimerDesigner().design_primers(seq, self.primer_size.get())
        self.primer_out.delete("1.0", "end")
        self.primer_out.insert("end", json.dumps(result, indent=2, default=str))

    def _build_plasmid_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Plasmid Builder")
        ttk.Label(f, text="Insert sequence:").pack(anchor="w", padx=10, pady=(10, 0))
        self.plasmid_input = tk.Text(f, height=4, width=100)
        self.plasmid_input.pack(fill="x", padx=10, pady=5)
        row = ttk.Frame(f); row.pack(fill="x", padx=10)
        ttk.Label(row, text="Vector:").pack(side="left")
        self.plasmid_vector = tk.StringVar(value="pUC19")
        ttk.Combobox(row, textvariable=self.plasmid_vector,
                     values=["pUC19", "pBR322", "pET28a", "pcDNA3.1"]).pack(side="left", padx=5)
        ttk.Label(row, text="Enzyme:").pack(side="left", padx=(10, 0))
        self.plasmid_enzyme = tk.StringVar(value="BamHI")
        ttk.Combobox(row, textvariable=self.plasmid_enzyme, width=10,
                     values=["EcoRI", "BamHI", "HindIII", "XhoI", "NotI", "NdeI", "XbaI", "KpnI", "SacI", "BglII"]).pack(side="left", padx=5)
        ttk.Button(f, text="Build construct", command=self._build_plasmid).pack(anchor="w", padx=10, pady=10)
        self.plasmid_out = scrolledtext.ScrolledText(f, height=12, font=("Consolas", 10))
        self.plasmid_out.pack(fill="both", expand=True, padx=10, pady=5)

    def _build_plasmid(self):
        seq = self.plasmid_input.get("1.0", "end").strip().replace(" ", "").upper()
        if not seq:
            return
        from genetic_engineering.plasmid_builder import PlasmidBuilder
        result = PlasmidBuilder().build(seq, self.plasmid_vector.get(), self.plasmid_enzyme.get())
        self.plasmid_out.delete("1.0", "end")
        self.plasmid_out.insert("end", json.dumps(result, indent=2, default=str))

    def _build_codon_tab(self, nb):
        f = ttk.Frame(nb)
        nb.add(f, text="Codon Optimization")
        ttk.Label(f, text="Protein sequence:").pack(anchor="w", padx=10, pady=(10, 0))
        self.codon_input = tk.Text(f, height=4, width=100)
        self.codon_input.pack(fill="x", padx=10, pady=5)
        row = ttk.Frame(f); row.pack(fill="x", padx=10)
        ttk.Label(row, text="Host:").pack(side="left")
        self.codon_host = tk.StringVar(value="escherichia coli")
        ttk.Combobox(row, textvariable=self.codon_host,
                     values=["escherichia coli", "saccharomyces cerevisiae", "homo sapiens"]).pack(side="left", padx=5)
        ttk.Button(f, text="Optimize", command=self._optimize_codons).pack(anchor="w", padx=10, pady=10)
        self.codon_out = scrolledtext.ScrolledText(f, height=12, font=("Consolas", 10))
        self.codon_out.pack(fill="both", expand=True, padx=10, pady=5)

    def _optimize_codons(self):
        prot = self.codon_input.get("1.0", "end").strip().upper()
        if not prot:
            return
        from genetic_engineering.codon_optimizer import CodonOptimizer
        result = CodonOptimizer().optimize(prot, self.codon_host.get())
        self.codon_out.delete("1.0", "end")
        self.codon_out.insert("end", json.dumps(result, indent=2, default=str))

    # -------------------------------------------------------------- calc
    def _build_calc_tab(self):
        frame = self._tab_calc
        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True, padx=5, pady=5)

        self._build_enzyme_calc(nb)
        self._build_growth_calc(nb)
        self._build_hwe_calc(nb)
        self._build_tm_calc(nb)
        self._build_unit_calc(nb)
        self._build_qpcr_calc(nb)

    def _build_enzyme_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Enzyme Kinetics")
        grid = ttk.Frame(f); grid.pack(anchor="w", padx=10, pady=10)
        self._label_entry_grid(grid, [
            ("[S] (mM)", "mm_s", "5"),
            ("Vmax (mM/s)", "mm_vmax", "10"),
            ("Km (mM)", "mm_km", "2"),
        ])
        ttk.Button(f, text="Calculate v", command=self._calc_mm).pack(pady=10)
        self.mm_out = ttk.Label(f, text="v = ?")
        self.mm_out.pack()

    def _calc_mm(self):
        from calculations.enzyme_kinetics import michaelis_menten
        v = michaelis_menten(float(self.vars["mm_s"].get()),
                             float(self.vars["mm_vmax"].get()),
                             float(self.vars["mm_km"].get()))
        self.mm_out.config(text=f"v = {v:.4f} mM/s")

    def _build_growth_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Cell Growth")
        grid = ttk.Frame(f); grid.pack(anchor="w", padx=10, pady=10)
        self._label_entry_grid(grid, [
            ("N0", "cg_n0", "1e6"),
            ("Nt", "cg_nt", "1e7"),
            ("t (h)", "cg_t", "5"),
            ("Dilution factor", "cg_dil", "10"),
            ("Steps", "cg_steps", "5"),
        ])
        btns = ttk.Frame(f); btns.pack(anchor="w", padx=10)
        ttk.Button(btns, text="Doubling time", command=self._calc_doubling).pack(side="left", pady=5)
        ttk.Button(btns, text="Serial dilution", command=self._calc_dilution).pack(side="left", padx=5, pady=5)
        self.cg_out = ttk.Label(f, text="")
        self.cg_out.pack()

    def _calc_doubling(self):
        from calculations.cell_growth_calc import doubling_time
        dt = doubling_time(float(self.vars["cg_n0"].get()),
                            float(self.vars["cg_nt"].get()),
                            float(self.vars["cg_t"].get()))
        self.cg_out.config(text=f"Doubling time = {dt:.3f} h")

    def _calc_dilution(self):
        from calculations.cell_growth_calc import serial_dilution
        series = serial_dilution(1.0, float(self.vars["cg_dil"].get()),
                                  int(self.vars["cg_steps"].get()))
        self.cg_out.config(text=f"Concentrations: {[round(s, 6) for s in series]}")

    def _build_hwe_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Population Genetics")
        grid = ttk.Frame(f); grid.pack(anchor="w", padx=10, pady=10)
        self._label_entry_grid(grid, [
            ("AA count", "hwe_aa", "100"),
            ("Aa count", "hwe_ab", "200"),
            ("aa count", "hwe_bb", "100"),
        ])
        ttk.Button(f, text="Hardy-Weinberg", command=self._calc_hwe).pack(pady=10)
        self.hwe_out = ttk.Label(f, text="")
        self.hwe_out.pack()

    def _calc_hwe(self):
        from calculations.population_genetics import hardy_weinberg_expected, chi_square_hwe
        obs = [int(self.vars["hwe_aa"].get()), int(self.vars["hwe_ab"].get()), int(self.vars["hwe_bb"].get())]
        exp = hardy_weinberg_expected(obs)
        chi = chi_square_hwe(obs)
        self.hwe_out.config(text=f"Expected: {[round(e, 1) for e in exp]} | chi2 = {chi:.3f}")

    def _build_tm_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Melting Temp (Tm)")
        ttk.Label(f, text="Oligo sequence:").pack(anchor="w", padx=10, pady=(10, 0))
        self.tm_input = tk.Text(f, height=2, width=60)
        self.tm_input.pack(fill="x", padx=10, pady=5)
        ttk.Button(f, text="Calculate Tm", command=self._calc_tm).pack(pady=10)
        self.tm_out = ttk.Label(f, text="")
        self.tm_out.pack()

    def _calc_tm(self):
        seq = self.tm_input.get("1.0", "end").strip().upper()
        if not seq:
            return
        from calculations.thermodynamic_calc import tm_wallace, tm_gc_content
        w = tm_wallace(seq)
        g = tm_gc_content(seq)
        self.tm_out.config(text=f"Wallace Tm = {w}°C | Salt-adjusted Tm = {g:.2f}°C")

    def _build_unit_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Unit Conversions")
        grid = ttk.Frame(f); grid.pack(anchor="w", padx=10, pady=10)
        self._label_entry_grid(grid, [
            ("Molarity (M)", "uc_m", "0.001"),
            ("MW (g/mol)", "uc_mw", "50000"),
            ("bp", "uc_bp", "1000"),
        ])
        btns = ttk.Frame(f); btns.pack(anchor="w", padx=10)
        ttk.Button(btns, text="M->mg/ml", command=self._calc_unit_m).pack(side="left", pady=5)
        ttk.Button(btns, text="bp->Daltons", command=self._calc_unit_bp).pack(side="left", padx=5, pady=5)
        self.uc_out = ttk.Label(f, text="")
        self.uc_out.pack()

    def _calc_unit_m(self):
        from calculations.unit_converter import molar_to_mg_ml
        v = molar_to_mg_ml(float(self.vars["uc_m"].get()), float(self.vars["uc_mw"].get()))
        self.uc_out.config(text=f"{v:.3f} mg/mL")

    def _calc_unit_bp(self):
        from calculations.unit_converter import bp_to_daltons
        v = bp_to_daltons(int(self.vars["uc_bp"].get()))
        self.uc_out.config(text=f"{v:.0f} Da")

    def _build_qpcr_calc(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="qPCR (2^-ddCt)")
        grid = ttk.Frame(f); grid.pack(anchor="w", padx=10, pady=10)
        self._label_entry_grid(grid, [
            ("Target Ct (sample)", "qpcr_ts", "20"),
            ("Reference Ct (sample)", "qpcr_rs", "15"),
            ("Target Ct (control)", "qpcr_tc", "22"),
            ("Reference Ct (control)", "qpcr_rc", "15"),
        ])
        ttk.Button(f, text="Fold change", command=self._calc_qpcr).pack(pady=10)
        self.qpcr_out = ttk.Label(f, text="")
        self.qpcr_out.pack()

    def _calc_qpcr(self):
        from calculations.gene_expression_calc import fold_change_ddct
        fc = fold_change_ddct(float(self.vars["qpcr_ts"].get()), float(self.vars["qpcr_rs"].get()),
                              float(self.vars["qpcr_tc"].get()), float(self.vars["qpcr_rc"].get()))
        self.qpcr_out.config(text=f"Fold change = {fc:.4f}")

    # -------------------------------------------------------------- sims
    def _build_sim_tab(self):
        frame = self._tab_sim
        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True, padx=5, pady=5)

        self._build_lv_sim(nb)
        self._build_sir_sim(nb)
        self._build_evo_sim(nb)
        self._build_logistic_sim(nb)

        # placeholder figure frame shared
        self.sim_fig_frame = ttk.Frame(frame)
        self.sim_fig_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _sim_params(self, f, fields):
        self.vars = getattr(self, "vars", {})
        for i, (label, key, default) in enumerate(fields):
            ttk.Label(f, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
            var = tk.StringVar(value=default)
            ttk.Entry(f, textvariable=var, width=12).grid(row=i, column=1, padx=5, pady=3)
            self.vars[key] = var
        return self.vars

    def _build_lv_sim(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Lotka-Volterra")
        params = ttk.Frame(f); params.pack(anchor="w", padx=10, pady=10)
        self._sim_params(params, [
            ("Prey initial", "lv_prey", "40"),
            ("Predator initial", "lv_pred", "9"),
            ("alpha", "lv_alpha", "0.1"),
            ("beta", "lv_beta", "0.02"),
            ("delta", "lv_delta", "0.01"),
            ("gamma", "lv_gamma", "0.1"),
            ("Days", "lv_days", "200"),
        ])
        ttk.Button(f, text="Run & plot", command=self._run_lv).pack(padx=10)

    def _run_lv(self):
        from simulation.population_simulator import LotkaVolterraSimulator
        v = self.vars
        r = LotkaVolterraSimulator().run(
            prey0=float(v["lv_prey"].get()), predator0=float(v["lv_pred"].get()),
            alpha=float(v["lv_alpha"].get()), beta=float(v["lv_beta"].get()),
            delta=float(v["lv_delta"].get()), gamma=float(v["lv_gamma"].get()),
            days=int(v["lv_days"].get()),
        )
        self._plot_sim(r["time"], [("prey", r["prey"]), ("predator", r["predator"])],
                       "Lotka-Volterra Predator-Prey", "Time (days)", "Population")

    def _build_sir_sim(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="SIR Epidemic")
        params = ttk.Frame(f); params.pack(anchor="w", padx=10, pady=10)
        self._sim_params(params, [
            ("Population", "sir_pop", "10000"),
            ("Initial infected", "sir_i0", "1"),
            ("beta", "sir_beta", "0.3"),
            ("gamma", "sir_gamma", "0.1"),
            ("Days", "sir_days", "160"),
        ])
        ttk.Button(f, text="Run & plot", command=self._run_sir).pack(padx=10)

    def _run_sir(self):
        from simulation.viral_transmission import SIRModel
        v = self.vars
        r = SIRModel().run(population=int(v["sir_pop"].get()), i0=int(v["sir_i0"].get()),
                           beta=float(v["sir_beta"].get()), gamma=float(v["sir_gamma"].get()),
                           days=int(v["sir_days"].get()))
        self._plot_sim(r["day"], [("S", r["S"]), ("I", r["I"]), ("R", r["R"])],
                       f"SIR Epidemic (R0={r['r0']})", "Day", "Population")

    def _build_evo_sim(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Evolution / Drift")
        params = ttk.Frame(f); params.pack(anchor="w", padx=10, pady=10)
        self._sim_params(params, [
            ("Population", "evo_pop", "1000"),
            ("Generations", "evo_gen", "100"),
            ("Fitness advantage", "evo_fit", "0.05"),
            ("Initial allele freq", "evo_p0", "0.01"),
        ])
        ttk.Button(f, text="Run & plot", command=self._run_evo).pack(padx=10)

    def _run_evo(self):
        from simulation.evolution_simulator import EvolutionSimulator
        v = self.vars
        r = EvolutionSimulator().run(population=int(v["evo_pop"].get()),
                                     generations=int(v["evo_gen"].get()),
                                     fitness_advantage=float(v["evo_fit"].get()),
                                     p0=float(v["evo_p0"].get()))
        self._plot_sim(r["generation"], [("allele freq", r["allele_freq"])],
                       "Natural Selection & Drift", "Generation", "Allele frequency")

    def _build_logistic_sim(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Logistic Growth")
        params = ttk.Frame(f); params.pack(anchor="w", padx=10, pady=10)
        self._sim_params(params, [
            ("N0", "log_n0", "10"),
            ("Carrying capacity", "log_k", "500"),
            ("Growth rate", "log_r", "0.5"),
            ("Days", "log_days", "50"),
        ])
        ttk.Button(f, text="Run & plot", command=self._run_logistic).pack(padx=10)

    def _run_logistic(self):
        from simulation.population_simulator import LogisticGrowthSimulator
        v = self.vars
        r = LogisticGrowthSimulator().run(n0=float(v["log_n0"].get()),
                                          carrying_capacity=float(v["log_k"].get()),
                                          rate=float(v["log_r"].get()),
                                          days=int(v["log_days"].get()))
        self._plot_sim(r["time"], [("population", r["population"])],
                       "Logistic Growth", "Time", "Population")

    def _plot_sim(self, x, series, title, xlabel, ylabel):
        for w in self.sim_fig_frame.winfo_children():
            w.destroy()
        fig, ax = plt.subplots(figsize=(8, 5))
        for name, ys in series:
            ax.plot(x, ys, marker="o", markersize=2, label=name)
        ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        ax.legend(); ax.grid(True, alpha=0.3)
        canvas = FigureCanvasTkAgg(fig, master=self.sim_fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # -------------------------------------------------------------- biosafety
    def _build_biosafety_tab(self):
        frame = self._tab_biosafety
        nb = ttk.Notebook(frame)
        nb.pack(fill="both", expand=True, padx=5, pady=5)
        self._build_bsl_tab(nb)
        self._build_pathogen_screen_tab(nb)
        self._build_waste_tab(nb)

    def _build_bsl_tab(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="BSL Classification")
        row = ttk.Frame(f); row.pack(anchor="w", padx=10, pady=10)
        ttk.Label(row, text="Organism:").pack(side="left")
        self.bsl_organism = tk.StringVar(value="Escherichia coli K-12")
        ttk.Entry(row, textvariable=self.bsl_organism, width=40).pack(side="left", padx=5)
        ttk.Button(f, text="Classify", command=self._classify_bsl).pack(anchor="w", padx=10)
        self.bsl_out = scrolledtext.ScrolledText(f, height=14, font=("Consolas", 10))
        self.bsl_out.pack(fill="both", expand=True, padx=10, pady=10)

    def _classify_bsl(self):
        from biosafety_hazards.bsl_classifier import BSLClassifier
        result = BSLClassifier.classify(self.bsl_organism.get())
        self.bsl_out.delete("1.0", "end")
        self.bsl_out.insert("end", json.dumps(result, indent=2, default=str))

    def _build_pathogen_screen_tab(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Pathogen Screening")
        ttk.Label(f, text="Sequence to screen:").pack(anchor="w", padx=10, pady=(10, 0))
        self.path_input = tk.Text(f, height=4, width=100)
        self.path_input.pack(fill="x", padx=10, pady=5)
        ttk.Label(f, text="Annotation (optional):").pack(anchor="w", padx=10)
        self.path_annot = tk.Text(f, height=2, width=100)
        self.path_annot.pack(fill="x", padx=10, pady=5)
        ttk.Button(f, text="Screen", command=self._screen_pathogen).pack(anchor="w", padx=10, pady=5)
        self.path_out = scrolledtext.ScrolledText(f, height=10, font=("Consolas", 10))
        self.path_out.pack(fill="both", expand=True, padx=10, pady=10)

    def _screen_pathogen(self):
        from biosafety_hazards.pathogen_screening import PathogenScreening
        seq = self.path_input.get("1.0", "end").strip()
        ann = self.path_annot.get("1.0", "end").strip()
        ps = PathogenScreening()
        result = ps.screen_sequence(seq) if seq else {}
        if ann:
            result["annotation_screen"] = ps.screen_annotation(ann)
        self.path_out.delete("1.0", "end")
        self.path_out.insert("end", json.dumps(result, indent=2, default=str))

    def _build_waste_tab(self, nb):
        f = ttk.Frame(nb); nb.add(f, text="Waste & Decon")
        row = ttk.Frame(f); row.pack(anchor="w", padx=10, pady=10)
        ttk.Label(row, text="Waste type:").pack(side="left")
        self.waste_type = tk.StringVar(value="solid")
        ttk.Combobox(row, textvariable=self.waste_type, width=20,
                     values=["standard", "liquid", "prion_waste"]).pack(side="left", padx=5)
        ttk.Button(f, text="Autoclave cycle", command=self._autoclave_cycle).pack(anchor="w", padx=10, pady=5)
        row2 = ttk.Frame(f); row2.pack(anchor="w", padx=10, pady=10)
        ttk.Label(row2, text="Target pathogen:").pack(side="left")
        self.dis_target = tk.StringVar(value="spores")
        ttk.Entry(row2, textvariable=self.dis_target, width=20).pack(side="left", padx=5)
        ttk.Button(row2, text="Recommend disinfectant", command=self._rec_disinfectant).pack(side="left", padx=5)
        self.waste_out = scrolledtext.ScrolledText(f, height=12, font=("Consolas", 10))
        self.waste_out.pack(fill="both", expand=True, padx=10, pady=10)

    def _autoclave_cycle(self):
        from biosafety_hazards.waste_disposal import WasteDisposal
        result = WasteDisposal.autoclave_cycle(self.waste_type.get())
        self.waste_out.delete("1.0", "end")
        self.waste_out.insert("end", json.dumps(result, indent=2, default=str))

    def _rec_disinfectant(self):
        from biosafety_hazards.waste_disposal import WasteDisposal
        result = WasteDisposal.recommend_disinfectant(self.dis_target.get())
        self.waste_out.delete("1.0", "end")
        self.waste_out.insert("end", f"Recommended for '{self.dis_target.get()}': {result}")

    # -------------------------------------------------------------- status
    def _build_status_tab(self):
        frame = self._tab_status
        ttk.Button(frame, text="Refresh status", command=self._refresh_status).pack(pady=10)
        self.status_out = scrolledtext.ScrolledText(frame, font=("Consolas", 10))
        self.status_out.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_status()

    def _refresh_status(self):
        try:
            ai = self._get_ai()
            status = {
                "ai_engine": ai.status(),
                "agents_loaded": list(self.agents),
                "load_in_progress": self._load_thread.is_alive(),
                "python": sys.version.split()[0],
                "platform": sys.platform,
                "working_dir": os.getcwd(),
            }
        except Exception as e:
            status = {"error": str(e), "agents_loaded": list(self.agents)}
        self.status_out.delete("1.0", "end")
        self.status_out.insert("end", json.dumps(status, indent=2, default=str))

    # -------------------------------------------------------------- helpers
    def _label_entry_grid(self, frame, fields):
        if not hasattr(self, "vars"):
            self.vars = {}
        for i, (label, key, default) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=3, sticky="e")
            var = tk.StringVar(value=default)
            ttk.Entry(frame, textvariable=var, width=12).grid(row=i, column=1, padx=5, pady=3)
            self.vars[key] = var

    def _get_seq(self):
        seq = self.seq_input.get("1.0", "end").strip().replace(" ", "").upper()
        if not seq:
            self._set_tools_output("[Enter a sequence first]")
            return ""
        return seq

    def _get_two_seqs(self):
        s1 = self.seq_input.get("1.0", "end").strip().replace(" ", "").upper()
        s2 = self.seq_input2.get("1.0", "end").strip().replace(" ", "").upper()
        if not s1 or not s2:
            self._set_tools_output("[Enter both sequences]")
            return "", ""
        return s1, s2

    def _set_tools_output(self, text):
        self.tools_output.delete("1.0", "end")
        self.tools_output.insert("end", text)

    def _append_chat(self, text):
        self.chat_output.insert("end", text + "\n")
        self.chat_output.see("end")

    def _run_async(self, fn):
        t = threading.Thread(target=self._safe_run, args=(fn,), daemon=True)
        t.start()

    def _safe_run(self, fn):
        try:
            fn()
        except Exception as e:
            self.root.after(0, lambda: self._append_chat(f"[ERROR] {e}\n"))

    def _load_agents(self):
        from agents.biology_agent import BiologyAgent
        from agents.geneticist_agent import GeneticistAgent
        from agents.cell_agent import CellAgent
        from agents.simulation_agent import SimulationAgent
        from agents.research_agent import ResearchAgent
        from agents.optimization_agent import OptimizationAgent
        from agents.project_agent import ProjectAgent
        from ai_core.ai_engine import AIEngine
        ai = AIEngine()
        for name, cls in [("biology", BiologyAgent), ("geneticist", GeneticistAgent),
                          ("cell", CellAgent), ("simulation", SimulationAgent),
                          ("research", ResearchAgent), ("optimization", OptimizationAgent),
                          ("project", ProjectAgent)]:
            try:
                self.agents[name] = cls(ai)
            except Exception as e:
                print(f"Failed to load {name} agent: {e}", file=sys.stderr)

    def _get_ai(self):
        from ai_core.ai_engine import AIEngine
        return AIEngine()

    def _wait_agent(self, name):
        self._load_thread.join(timeout=15)
        return self.agents[name]


def launch():
    root = tk.Tk()
    BiologyUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch()
