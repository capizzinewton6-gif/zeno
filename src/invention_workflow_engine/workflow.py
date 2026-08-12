"""End-to-end autonomous invention workflow engine.

Executes the full sequence:
  1. Interpret invention request
  2. Research scientific literature and patents
  3. Generate invention concepts
  4. Evaluate feasibility
  5. Design mechanical systems
  6. Design electrical/electronic systems
  7. Generate software and firmware
  8. Create engineering calculations
  9. Launch Paint and generate all schematics automatically
 10. Save blueprint images
 11. Launch Notepad and generate all engineering documents automatically
 12. Save documentation files
 13. Generate BOM, testing plans, and manufacturing plans
 14. Organize project folders
 15. Create a final ZIP invention package
 16. Present the completed package to the user
"""

from __future__ import annotations

import os
import shutil
import zipfile
from typing import Callable

from ai_core.ai_engine import AIEngine
from ai_core.knowledge_engine import KnowledgeEngine
from research import PatentSearch, WebSearch
from invention import IdeaGenerator, ConceptDeveloper, FeasibilityAnalyzer, RequirementsDefiner
from engineering import MechanicalEngineering, ElectricalEngineering, ElectronicsEngineering
from materials import MaterialSelector
from prototyping import BillOfMaterials, AssemblyPlanner
from manufacturing import ManufacturingPlanner, CostEstimator
from project import ReportGenerator, Documentation
from tools import FileManager
from src.painter_automation import PainterAutomation
from src.notepad_automation import NotepadAutomation


class InventionWorkflowEngine:
    def __init__(self, engine: AIEngine | None = None,
                 file_manager: FileManager | None = None,
                 progress: Callable[[str], None] | None = None):
        self.engine = engine or AIEngine()
        self.file_manager = file_manager or FileManager()
        self.progress = progress or (lambda msg: None)
        # Capability modules
        self.knowledge = KnowledgeEngine(self.engine.primary)
        self.patent = PatentSearch(self.engine.secondary, self.engine.primary)
        self.web = WebSearch(self.engine.primary)
        self.idea_gen = IdeaGenerator(self.engine.primary)
        self.concept_dev = ConceptDeveloper(self.engine.primary)
        self.feasibility = FeasibilityAnalyzer(self.engine.primary)
        self.requirements = RequirementsDefiner(self.engine.primary)
        self.mechanical = MechanicalEngineering(self.knowledge)
        self.electrical = ElectricalEngineering(self.knowledge)
        self.electronics = ElectronicsEngineering(self.knowledge)
        self.material_selector = MaterialSelector(self.engine.primary)
        self.bom = BillOfMaterials(self.engine.primary)
        self.assembly = AssemblyPlanner(self.engine.primary)
        self.manufacturing = ManufacturingPlanner(self.engine.primary)
        self.cost = CostEstimator(self.engine.primary)
        self.docs = Documentation(self.engine.primary)
        self.reports = ReportGenerator(self.engine.primary)

    def _set_progress(self, fn):
        self.progress = fn or self.progress

    def run(self, request: str, package_name: str | None = None) -> dict:
        """Execute the full invention workflow and return a package summary."""
        self._log("1. Interpreting invention request")
        concept = self.engine.reason(
            f"Interpret this invention request and produce a clear concept: {request}",
            system="You are a world-class inventor.")

        package_name = package_name or self._safe_name(concept) or self._safe_name(request) or "invention"
        project_dir = self.file_manager.project_dir(package_name)
        blueprints_dir = self.file_manager.subfolder(package_name, "blueprints")
        docs_dir = self.file_manager.subfolder(package_name, "documentation")
        calc_dir = self.file_manager.subfolder(package_name, "calculations")
        sim_dir = self.file_manager.subfolder(package_name, "simulations")
        src_dir = self.file_manager.subfolder(package_name, "source_code")

        self._log("2. Researching scientific literature and patents")
        patent_summary = self.patent.search(concept)
        research = self.web.research(concept)
        self._save(docs_dir, "research_and_patents.txt",
                   f"RESEARCH\n{research}\n\nPATENT SEARCH\n{patent_summary}")

        self._log("3. Generating invention concepts")
        concepts = self.idea_gen.generate(concept)
        self._save(docs_dir, "concepts.txt", concepts)

        self._log("4. Evaluating feasibility")
        feasibility = self.feasibility.analyze(concept)
        self._save(docs_dir, "feasibility_analysis.txt", feasibility)
        requirements = self.requirements.define(concept)
        self._save(docs_dir, "requirements.txt", requirements)

        self._log("5. Designing mechanical systems")
        mechanical_design = self.mechanical.design_mechanism(f"{concept}: {request}")
        self._save(docs_dir, "mechanical_design.txt", mechanical_design)

        self._log("6. Designing electrical and electronic systems")
        electrical_design = self.electrical.power_system(f"{concept}: {request}")
        electronics_design = self.electronics.design_circuit(f"{concept}: {request}")
        self._save(docs_dir, "electrical_design.txt",
                   f"ELECTRICAL\n{electrical_design}\n\nELECTRONICS\n{electronics_design}")

        self._log("7. Generating software and firmware")
        software = self.engine.reason(
            f"Design software/firmware architecture for: {concept}",
            system="You are an embedded software architect.")
        self._save(src_dir, "firmware_outline.txt", software)

        self._log("8. Creating engineering calculations")
        calcs = self.engine.reason(
            f"Perform key engineering calculations (structural, thermal, "
            f"electrical) for: {concept}",
            system="You are an engineering calculations engineer.")
        self._save(calc_dir, "calculations.txt", calcs)

        self._log("9. Launching Paint and generating all schematics")
        painter = PainterAutomation(output_dir=blueprints_dir)
        painter.launch_paint()
        shapes = self._shapes_for(concept)
        blueprint_paths = painter.generate_all_views({"default": shapes})
        painter.close_paint()

        self._log("11. Launching Notepad and generating all documents")
        notepad = NotepadAutomation(output_dir=docs_dir)
        notepad.launch_notepad()
        doc_paths = notepad.generate_all(concept)
        notepad.close_notepad()

        self._log("13. Generating BOM, testing plans, and manufacturing plans")
        bom_text = self.bom.generate(concept)
        self._save(project_dir, "bill_of_materials.csv", bom_text)
        test_plan = self.engine.reason(
            f"Create a testing plan for: {concept}",
            system="You are a test engineer.")
        self._save(docs_dir, "testing_plan.txt", test_plan)
        mfg_plan = self.manufacturing.plan(concept)
        self._save(docs_dir, "manufacturing_plan.txt", mfg_plan)
        cost_est = self.cost.estimate(concept)
        self._save(docs_dir, "cost_estimation.txt", cost_est)

        self._log("14. Generating project summary report")
        report = self.reports.generate(package_name)
        summary_path = self._save(project_dir, "project_summary.md", report)

        self._log("15. Creating final ZIP invention package")
        zip_path = shutil.make_archive(
            os.path.join(self.file_manager.root, package_name + "_invention_package"),
            "zip", project_dir)

        self._log("16. Package complete")
        return {
            "concept": concept,
            "package_name": package_name,
            "project_dir": project_dir,
            "blueprints": blueprint_paths,
            "documents": doc_paths,
            "summary": summary_path,
            "zip_package": zip_path,
            "file_count": len(self.file_manager.list_files(package_name)),
        }

    def _safe_name(self, concept: str) -> str:
        """Derive a filesystem-safe package name from the concept text.

        Skips stub header lines and prompt echoes, using the first
        meaningful content line. Strips leading instruction templates
        (text before a colon) so stub-mode echoed prompts still yield a
        clean name.
        """
        skip_prefixes = ("interpret", "generate", "research", "design",
                         "perform", "create", "write", "analyze", "provide",
                         "turn", "decompose", "identify", "develop", "produce")
        for line in concept.splitlines():
            line = line.strip().strip(" -*()[]").strip()
            if not line:
                continue
            low = line.lower()
            if "offline stub" in low or low.startswith("configure ") or "gemini" in low:
                continue
            if low.startswith("request:"):
                line = line.split(":", 1)[1].strip()
                if not line:
                    continue
                low = line.lower()
            # Strip an instruction template prefix: "Do X: actual content".
            if ":" in line:
                before, after = line.split(":", 1)
                if before.strip().lower().split(" ", 1)[0] in skip_prefixes and after.strip():
                    line = after.strip()
                    low = line.lower()
            if not line:
                continue
            # Skip lines that merely echo an instruction prompt with no payload.
            first_word = low.split(" ", 1)[0].rstrip(":")
            if first_word in skip_prefixes:
                continue
            safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in line)
            name = safe.strip().replace(" ", "_")[:50]
            if name:
                return name
        return "invention"

    def _shapes_for(self, concept: str) -> list[dict]:
        # Default placeholder shapes representing the invention envelope.
        return [
            {"kind": "rect", "x": 2, "y": 2, "w": 6, "h": 4, "label": "Main Body"},
            {"kind": "circle", "x": 3, "y": 7, "r": 0.8, "label": "Port A"},
            {"kind": "circle", "x": 7, "y": 7, "r": 0.8, "label": "Port B"},
            {"kind": "line", "x1": 2, "y1": 2, "x2": 8, "y2": 6, "label": ""},
        ]

    def _save(self, directory: str, filename: str, content) -> str:
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        if isinstance(content, (list, tuple)):
            content = "\n".join(str(c) for c in content)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _log(self, message: str):
        self.progress(message)
