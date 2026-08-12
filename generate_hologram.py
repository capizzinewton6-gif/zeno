#!/usr/bin/env python3
"""
generate_hologram.py - scaffold the TONY STARK HOLOGRAM OS.

Builds the full modular capability-based architecture for a holographic
artificial-intelligence operating environment, following the same convention as
the repo's existing build_structure.py: every capability module is an
independent package implementing the standard `execute(task, context)` contract.

The generated project lives under TONY_STARK_HOLOGRAM/ and is runnable:

    python3 TONY_STARK_HOLOGRAM/main.py            # interactive workspace
    python3 TONY_STARK_HOLOGRAM/main.py --task "..."  # single command
    python3 TONY_STARK_HOLOGRAM/main.py --no-daemons # skip daemons
    python3 TONY_STARK_HOLOGRAM/main.py --skip-boot    # skip boot sequence

Run this generator once to (re)create the whole tree:

    python3 generate_hologram.py
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path("/workspace/project/zeno/TONY_STARK_HOLOGRAM")

# --------------------------------------------------------------------------- #
# Catalogue: package -> {filename: description}
# --------------------------------------------------------------------------- #

PACKAGES: Dict[str, Dict[str, str]] = {
    "holographic_display": {
        "spatial_renderer.py": "3D holographic rendering.",
        "depth_renderer.py": "Z-axis depth rendering.",
        "parallax_engine.py": "Horizontal/vertical/full parallax.",
        "lightfield_renderer.py": "Light-field generation.",
        "volumetric_renderer.py": "Volumetric object rendering.",
        "transparency_engine.py": "Opacity/translucency control.",
        "lighting_engine.py": "Dynamic lighting and reflections.",
        "shadow_engine.py": "Dynamic holographic shadows.",
        "material_renderer.py": "Metal, glass, carbon-fiber materials.",
        "optical_effects.py": "Refraction, dispersion, HDR, DOF.",
        "display_manager.py": "Controls holographic display hardware.",
    },
    "gesture_control": {
        "hand_tracker.py": "3D hand tracking.",
        "skeleton_tracker.py": "Finger/joint tracking.",
        "gesture_recognizer.py": "Gesture classification.",
        "pinch_controller.py": "Air-pinch interaction.",
        "raycast_controller.py": "Finger-based pointing.",
        "two_hand_controller.py": "Two-handed manipulation.",
        "air_drawing.py": "3D air drawing.",
        "gesture_macros.py": "Custom gesture commands.",
        "tremor_filter.py": "Gesture stabilization.",
        "sensitivity_manager.py": "Adaptive gesture sensitivity.",
    },
    "spatial_computing": {
        "room_scanner.py": "3D room/environment scanning.",
        "spatial_mapper.py": "Environmental mesh generation.",
        "surface_anchor.py": "Table/wall/floor anchoring.",
        "spatial_anchor_manager.py": "Persistent spatial positions.",
        "obstacle_detector.py": "Real-world obstacle detection.",
        "occlusion_engine.py": "Real/virtual object occlusion.",
        "boundary_manager.py": "Safe spatial boundaries.",
        "physics_grounding.py": "Virtual object/floor interaction.",
        "room_persistence.py": "Restore hologram locations.",
        "multi_room_sync.py": "Networked spatial synchronization.",
    },
    "interaction": {
        "voice_interface.py": "Sends voice commands to existing AI.",
        "gaze_tracking.py": "Eye/gaze tracking.",
        "proximity_detector.py": "User proximity detection.",
        "spatial_audio.py": "3D positional audio.",
        "virtual_keyboard.py": "Floating keyboard.",
        "virtual_buttons.py": "Interactive holographic controls.",
        "object_manipulator.py": "Grab/rotate/scale objects.",
        "object_deformation.py": "Interactive object deformation.",
        "multimodal_input.py": "Voice + gesture + gaze.",
    },
    "holographic_objects": {
        "object_manager.py": "Create/delete/manage holograms.",
        "model_loader.py": "Load 3D models.",
        "model_converter.py": "Convert supported 3D formats.",
        "object_transform.py": "Position/rotation/scaling.",
        "animation_controller.py": "Object animation.",
        "exploded_view.py": "Exploded mechanical assemblies.",
        "measurement_tools.py": "Spatial measurements.",
        "object_library.py": "Reusable holographic models.",
    },
    "visualization": {
        "holographic_dashboard.py": "Floating information dashboards.",
        "graph_renderer.py": "3D graphs.",
        "chart_renderer.py": "Scientific/technical charts.",
        "diagram_renderer.py": "Technical diagrams.",
        "blueprint_renderer.py": "3D blueprint visualization.",
        "architecture_renderer.py": "Building/system visualization.",
        "data_visualizer.py": "Data visualization.",
        "simulation_visualizer.py": "Simulation visualization.",
    },
    "scientific_visualization": {
        "molecular_viewer.py": "3D molecular structures.",
        "anatomy_viewer.py": "3D biological structures.",
        "physics_visualizer.py": "Physical systems.",
        "chemistry_visualizer.py": "Chemical systems.",
        "biology_visualizer.py": "Biological systems.",
        "equation_visualizer.py": "3D mathematical equations.",
        "simulation_viewer.py": "Scientific simulations.",
    },
    "engineering": {
        "cad_viewer.py": "CAD model visualization.",
        "assembly_viewer.py": "Mechanical assembly visualization.",
        "component_inspector.py": "Component information.",
        "stress_visualizer.py": "Stress/force visualization.",
        "airflow_visualizer.py": "Aerodynamic visualization.",
        "thermal_visualizer.py": "Heat distribution visualization.",
        "collision_checker.py": "Component collision checking.",
        "digital_twin.py": "Live engineering-system visualization.",
    },
    "telepresence": {
        "volumetric_capture.py": "3D person/object capture.",
        "point_cloud_stream.py": "Live point-cloud streaming.",
        "avatar_renderer.py": "3D avatar rendering.",
        "spatial_stream.py": "Spatial data transmission.",
        "telepresence_manager.py": "Holographic communication.",
    },
    "hardware": {
        "depth_camera.py": "LiDAR/ToF/stereo camera interface.",
        "camera_manager.py": "Camera management.",
        "projector_controller.py": "Projection hardware interface.",
        "spatial_light_modulator.py": "SLM interface.",
        "optical_calibration.py": "Optical alignment/calibration.",
        "sensor_manager.py": "Hardware sensor management.",
        "thermal_manager.py": "Hardware thermal monitoring.",
        "safety_interlock.py": "Hardware safety shutdown.",
    },
    "rendering": {
        "render_engine.py": "Main real-time renderer.",
        "point_cloud_renderer.py": "Point-cloud rendering.",
        "gaussian_splat_renderer.py": "3D Gaussian splatting.",
        "ray_tracing.py": "Ray-traced rendering.",
        "fft_engine.py": "FFT acceleration.",
        "lod_manager.py": "Level-of-detail management.",
        "occlusion_culling.py": "Rendering optimization.",
        "gpu_acceleration.py": "GPU rendering acceleration.",
    },
    "security": {
        "user_authentication.py": "User authentication.",
        "biometric_lock.py": "Face/eye authentication interface.",
        "holographic_watermark.py": "Dynamic holographic signatures.",
        "encrypted_channel.py": "Encrypted communications.",
        "session_security.py": "Session protection.",
        "tamper_detection.py": "Hardware/software tamper detection.",
    },
    "applications": {
        "holographic_browser.py": "Web content as spatial interfaces.",
        "holographic_files.py": "3D file/workspace visualization.",
        "holographic_terminal.py": "Floating terminal.",
        "holographic_communication.py": "Communication interface.",
        "holographic_maps.py": "3D maps and geographic visualization.",
        "holographic_control.py": "Computer/system controls.",
        "holographic_workspace.py": "Persistent spatial desktop.",
    },
    "ai_bridge": {
        "api_client.py": "Connects to YOUR existing AI.",
        "command_router.py": "Sends user commands to your AI.",
        "response_handler.py": "Receives AI responses.",
        "event_bridge.py": "AI <-> hologram events.",
        "capability_interface.py": "Exposes holographic controls to your AI.",
    },
    "persistence": {
        "spatial_memory.py": "Saves hologram positions.",
        "scene_manager.py": "Saves complete holographic scenes.",
        "object_state.py": "Saves object states.",
        "configuration.py": "Hologram configuration.",
    },
    "safety": {
        "spatial_safety.py": "Safe movement boundaries.",
        "hardware_safety.py": "Hardware protection.",
        "eye_safety.py": "Optical safety interface.",
        "collision_safety.py": "Physical collision prevention.",
        "emergency_shutdown.py": "Emergency system shutdown.",
    },
}


def _camel_class(filename: str) -> str:
    """3d_model_generator.py -> _3dModelGenerator (matches repo convention)."""
    stem = filename[:-3] if filename.endswith(".py") else filename
    parts = stem.split("_")
    name = "".join(p[:1].upper() + p[1:] for p in parts if p)
    if name and name[0].isdigit():
        name = "_" + name
    return name


def module_source(package: str, filename: str, description: str) -> str:
    cls = _camel_class(filename)
    stem = filename[:-3]
    title = f"{package} - {stem}"
    bar = "=" * max(len(title), 40)
    return textwrap.dedent(
        f'''\
        """
        {title}
        {bar}
        {description}

        Independent {package} module for the Tony Stark Hologram OS.
        Implements the standard execute(task, context) capability contract.
        """

        from typing import Any, Dict, Optional


        class {cls}:
            """{description}"""

            def __init__(self, config: Optional[Dict[str, Any]] = None):
                self.config = config or {{}}
                self.name = "{stem}"
                self.description = "{description}"

            def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
                """Execute a task with this capability (stub until hardware-backed)."""
                return {{"module": self.name, "package": "{package}", "task": task, "status": "stub"}}

            def get_name(self) -> str:
                return self.name

            def get_description(self) -> str:
                return self.description
        '''
    )


def package_init_source(package: str, files: List[str]) -> str:
    names = ", ".join(_camel_class(f) for f in files)
    quoted_names = ", ".join(f'"{_camel_class(f)}"' for f in files)
    return textwrap.dedent(
        f'''\
        """{package} package - auto-registers its capability modules."""

        from typing import Any, Dict, List

        # Per-module imports (kept explicit so a failing import does not break
        # the whole package).
        {'\n        '.join(f"from .{f[:-3]} import {_camel_class(f)}" for f in files) if files else "pass"}


        def list_modules() -> List[str]:
            """Return the capability names registered in this package."""
            return [
                {'\n                '.join(f'"{f[:-3]}",' for f in files) if files else ''}
            ]


        def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
            """Instantiate every module in this package and return name->instance."""
            return {{
                name: cls(config=config)
                for name, cls in (
                    {'\n                    '.join(f'("{f[:-3]}", {_camel_class(f)}),' for f in files) if files else ''}
                )
            }}


        __all__ = ["list_modules", "instantiate_all", {quoted_names}]
        '''
    )


# --------------------------------------------------------------------------- #
# Top-level functional files
# --------------------------------------------------------------------------- #

MAIN_PY = r'''#!/usr/bin/env python3
"""
TONY STARK HOLOGRAM OS - main entry point.

Boots the arc reactor, spatially scans the room, raises the holographic grid,
materialises the telemetry dashboard, greets the user, then exposes the
interactive holographic workspace.

Usage:
    python main.py                  # full boot + interactive workspace
    python main.py --task "..."     # single command
    python main.py --skip-boot      # skip the boot animation
    python main.py --no-daemons     # skip background daemons
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from typing import Optional

from core.arc_reactor import ArcReactor
from core.hologram_grid import HologramGrid
from core.startup import StartupSequence
from core.telemetry_dashboard import TelemetryDashboard
from core.workspace import HolographicWorkspace
from ui import HolographicUI


def parse_args():
    p = argparse.ArgumentParser(description="Tony Stark Hologram OS")
    p.add_argument("--task", "-t", type=str, default=None, help="Single command to execute")
    p.add_argument("--skip-boot", action="store_true", help="Skip the boot sequence")
    p.add_argument("--no-daemons", action="store_true", help="Skip background daemons")
    p.add_argument("--user", type=str, default="Operator", help="User display name")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    return p.parse_args()


def boot_sequence(user: str, ui: "HolographicUI"):
    """Run the cinematic startup experience."""
    reactor = ArcReactor(ui=ui)
    grid = HologramGrid(ui=ui)
    dashboard = TelemetryDashboard(ui=ui)
    boot = StartupSequence(reactor=reactor, grid=grid, dashboard=dashboard, ui=ui)
    boot.run(user=user)


def start_daemons(workspace: HolographicWorkspace):
    """Background telemetry / safety / ai-bridge loops."""
    threads = []

    def loop(fn, name, interval):
        while True:
            try:
                fn()
            except Exception as exc:
                print(f"[daemon:{name}] error: {exc}", file=sys.stderr)
            time.sleep(interval)

    specs = [
        (workspace.dashboard.refresh, "telemetry", 5),
        (workspace.tick_safety, "safety", 2),
    ]
    for fn, name, interval in specs:
        t = threading.Thread(target=loop, args=(fn, name, interval), daemon=True, name=f"daemon-{name}")
        t.start()
        threads.append(t)
    print("[main] background daemons started:", [t.name for t in threads])
    return threads


def main():
    args = parse_args()
    ui = HolographicUI(verbose=args.verbose)

    if not args.skip_boot:
        boot_sequence(args.user, ui)
    else:
        print("[boot] skipped")

    workspace = HolographicWorkspace(ui=ui)

    if not args.no_daemons:
        start_daemons(workspace)

    if args.task:
        result = workspace.execute(args.task)
        ui.speak(result)
        return

    ui.run_workspace(workspace)


if __name__ == "__main__":
    main()
'''


UI_PY = r'''#!/usr/bin/env python3
"""Holographic UI - text/ANSI front-end for the Tony Stark Hologram OS."""

from __future__ import annotations

import os
import sys
import time
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.text import Text

    _CONSOLE = Console()
    _HAS_RICH = True
except ImportError:  # pragma: no cover - rich is a declared dependency
    _CONSOLE = None
    _HAS_RICH = False


_ARC = r"""
        .  . *  .   *   .     *    .    *   .
      *   .    .  *   .    *   .   .   *    .
    .   *   .   (  ARC REACTOR  )   .   *   .
      *   .    .  *   .    *   .   .   *    .
        .  *  .   *   .     *    .    *   .
"""


class HolographicUI:
    """Cyan-tinted, panel-wrapped console output + REPL."""

    CYAN = "bright_cyan"
    AMBER = "yellow"
    GREEN = "green"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    # -- low level helpers --------------------------------------------------
    def _emit(self, text: str, style: Optional[str] = None):
        if _HAS_RICH:
            _CONSOLE.print(text, style=style)
        else:
            print(text)

    def panel(self, body: str, title: str = "J.A.R.V.I.S.", style: Optional[str] = None):
        if _HAS_RICH:
            _CONSOLE.print(Panel.fit(body, title=title, border_style=style or self.CYAN))
        else:
            print(f"\n--- {title} ---\n{body}\n")

    def speak(self, text: str):
        """Voice-style line (rendered as quoted, stylised text)."""
        self._emit(f'\u201c{text}\u201d', self.GREEN)

    def banner(self, text: str):
        self._emit(text, self.CYAN)

    def warn(self, text: str):
        self._emit(f"[!] {text}", self.AMBER)

    # -- animation pieces ---------------------------------------------------
    def arc_reactor(self):
        self._emit(_ARC, self.CYAN)

    def progress(self, label: str, total: int = 100, sleep: float = 0.01):
        if _HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.percentage:>3.0f}%"),
                console=_CONSOLE,
                transient=False,
            ) as prog:
                task = prog.add_task(label, total=total)
                for i in range(total):
                    prog.update(task, advance=1)
                    time.sleep(sleep)
        else:
            sys.stdout.write(f"{label}: ")
            for i in range(total):
                sys.stdout.write("#" if i % 10 == 0 else ".")
                sys.stdout.flush()
                time.sleep(sleep)
            sys.stdout.write(" done\n")

    def grid(self):
        """Render a holographic floor grid."""
        lines = []
        for i in range(7):
            line = "  " + "   ".join(f"{(i*7+j)%10}" for j in range(23))
            lines.append(line)
        grid_txt = "\n".join(lines)
        self.panel(grid_txt, title="SPATIAL GRID", style=self.CYAN)

    # -- REPL ----------------------------------------------------------------
    def run_workspace(self, workspace):
        self.banner("=" * 60)
        self.banner("  TONY STARK HOLOGRAM OS - WORKSPACE ONLINE")
        self.banner("  Type 'help' for commands, 'exit' to power down.")
        self.banner("=" * 60)
        while True:
            try:
                cmd = input("\nholo> ").strip()
            except (EOFError, KeyboardInterrupt):
                self.banner("\n[power] hologram offline.")
                break
            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit", "power down"):
                self.speak("Powering down. Goodbye, Operator.")
                break
            result = workspace.execute(cmd)
            if isinstance(result, dict):
                self.panel(
                    "\n".join(f"{k}: {v}" for k, v in result.items()),
                    title="RESULT",
                    style=self.CYAN,
                )
            else:
                self.speak(str(result))
'''


SETUP_PY = r'''#!/usr/bin/env python3
"""
setup.py - installs dependencies, creates runtime directories and config.

Run:  python setup.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIREMENTS = [
    "rich>=13.0.0",
    "psutil>=5.9.0",
    "numpy>=1.24.0",
    "requests>=2.31.0",
    "google-generativeai>=0.8.0",
    "pyyaml>=6.0",
]

RUNTIME_DIRS = ["logs", "scenes", "memory"]


def install_deps():
    print("[setup] installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *REQUIREMENTS])


def ensure_dirs():
    for d in RUNTIME_DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"[setup] ensured directory: {d}")


def ensure_config():
    cfg = ROOT / "config"
    cfg.mkdir(parents=True, exist_ok=True)
    defaults = {
        "settings.json": {
            "user": "Operator",
            "boot_sequence": True,
            "spatial_audio": True,
            "particle_effects": True,
        },
        "hardware.json": {
            "depth_camera": {"type": "auto", "enabled": True},
            "projector": {"type": "auto", "brightness": 1.0},
            "safety_interlock": True,
        },
        "display.json": {
            "resolution": [3840, 2160],
            "parallax": "full",
            "lightfield": True,
            "target_fps": 60,
        },
        "ai_keys.json": {"gemini_api_key": "", "model_25": "gemini-2.5-flash", "model_15": "gemini-1.5-flash"},
    }
    for name, data in defaults.items():
        path = cfg / name
        if not path.exists():
            path.write_text(json.dumps(data, indent=2))
            print(f"[setup] wrote default config: {name}")
        else:
            print(f"[setup] config exists: {name}")


def main():
    ensure_dirs()
    ensure_config()
    if "--no-deps" not in sys.argv:
        install_deps()
    print("[setup] complete. Run:  python main.py")


if __name__ == "__main__":
    main()
'''


REQUIREMENTS_TXT = """\
# Tony Stark Hologram OS dependencies
rich>=13.0.0
psutil>=5.9.0
numpy>=1.24.0
requests>=2.31.0
google-generativeai>=0.8.0
pyyaml>=6.0
"""


# --------------------------------------------------------------------------- #
# Core engine (genuinely functional) - generated into core/
# --------------------------------------------------------------------------- #

CORE_FILES: Dict[str, str] = {
    "__init__.py": '"""core - functional engine for the Hologram OS."""\n',
    "arc_reactor.py": r'''"""Arc reactor - power core with boot animation."""

from __future__ import annotations

import time
from typing import Optional


class ArcReactor:
    """Powers on the holographic stack and reports power state."""

    def __init__(self, ui=None, capacity: float = 8.0):
        self.ui = ui
        self.capacity = capacity  # gigajoules
        self.level = 0.0
        self.online = False

    def power_on(self):
        if self.ui:
            self.ui.arc_reactor()
        steps = 40
        for i in range(steps + 1):
            self.level = self.capacity * (i / steps)
            time.sleep(0.02)
        self.online = True
        if self.ui:
            self.ui.speak(f"Arc reactor online at {self.level:.1f} GJ capacity.")

    def status(self) -> dict:
        return {
            "online": self.online,
            "level_gj": round(self.level, 2),
            "capacity_gj": self.capacity,
            "load_pct": round(100 * (self.level / self.capacity), 1) if self.capacity else 0,
        }

    def execute(self, task: str, context=None):
        if task in ("power_on", "on", "boot"):
            self.power_on()
            return self.status()
        if task in ("status", "report"):
            return self.status()
        return {"module": "arc_reactor", "task": task, "status": "unknown"}
''',
    "hologram_grid.py": r'''"""Holographic floor grid - the spatial canvas."""

from __future__ import annotations

from typing import Optional


class HologramGrid:
    """Raises and configures the holographic reference grid."""

    def __init__(self, ui=None, cells: int = 16):
        self.ui = ui
        self.cells = cells
        self.visible = False

    def raise_grid(self):
        if self.ui:
            self.ui.grid()
        self.visible = True
        if self.ui:
            self.ui.speak(f"Holographic grid materialised - {self.cells}x{self.cells} cells.")

    def lower_grid(self):
        self.visible = False
        if self.ui:
            self.ui.speak("Holographic grid lowered.")

    def status(self) -> dict:
        return {"grid_visible": self.visible, "cells": self.cells}

    def execute(self, task: str, context=None):
        if task in ("raise", "show", "on"):
            self.raise_grid()
            return self.status()
        if task in ("lower", "hide", "off"):
            self.lower_grid()
            return self.status()
        return {"module": "hologram_grid", "task": task, "status": "unknown"}
''',
    "telemetry_dashboard.py": r'''"""Telemetry dashboard - live system stats."""

from __future__ import annotations

from typing import Optional

try:
    import psutil

    _HAS_PSUTIL = True
except ImportError:  # pragma: no cover
    psutil = None
    _HAS_PSUTIL = False


class TelemetryDashboard:
    """Materialises a floating panel of live hardware/scene telemetry."""

    def __init__(self, ui=None):
        self.ui = ui
        self.holograms = 0

    def _snapshot(self) -> dict:
        if _HAS_PSUTIL:
            vm = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=None)
            return {
                "cpu_pct": cpu,
                "mem_pct": vm.percent,
                "mem_used_gb": round(vm.used / 1e9, 2),
                "mem_total_gb": round(vm.total / 1e9, 2),
                "holograms": self.holograms,
            }
        return {"cpu_pct": -1, "mem_pct": -1, "mem_used_gb": -1, "mem_total_gb": -1, "holograms": self.holograms}

    def materialise(self):
        snap = self._snapshot()
        if self.ui:
            body = (
                f"CPU        : {snap['cpu_pct']:5.1f} %\n"
                f"Memory     : {snap['mem_pct']:5.1f} %  "
                f"({snap['mem_used_gb']} / {snap['mem_total_gb']} GB)\n"
                f"Holograms  : {snap['holograms']}"
            )
            self.ui.panel(body, title="TELEMETRY DASHBOARD", style=self.ui.CYAN if self.ui else None)
        return snap

    def refresh(self):
        """Daemon tick - silently refresh snapshot (no print to avoid spam)."""
        self._snapshot()

    def add_hologram(self, n: int = 1):
        self.holograms += n

    def execute(self, task: str, context=None):
        if task in ("show", "materialise", "status"):
            return self.materialise()
        return {"module": "telemetry_dashboard", "task": task, "status": "unknown"}
''',
    "startup.py": r'''"""Startup sequence - orchestrates the cinematic boot experience."""

from __future__ import annotations

from typing import Optional


class StartupSequence:
    """Drives: arc reactor -> room scan -> grid -> dashboard -> greeting."""

    def __init__(self, reactor, grid, dashboard, ui=None):
        self.reactor = reactor
        self.grid = grid
        self.dashboard = dashboard
        self.ui = ui

    def run(self, user: str = "Operator"):
        # 1. Arc reactor powers on.
        self.reactor.power_on()
        # 2. Room spatially scanned.
        if self.ui:
            self.ui.progress("Scanning spatial environment", total=100, sleep=0.01)
            self.ui.speak("Spatial scan complete. Environment mapped.")
        # 3. Holographic grid appears.
        self.grid.raise_grid()
        # 4. Telemetry dashboard materialises.
        self.dashboard.materialise()
        # 5. Voice greets the user.
        if self.ui:
            self.ui.speak(f"Good evening, {user}. All systems are operational and at your service.")
        return {
            "reactor": self.reactor.status(),
            "grid": self.grid.status(),
            "boot": "complete",
        }

    def execute(self, task: str, context=None):
        if task in ("boot", "run", "start"):
            user = (context or {}).get("user", "Operator")
            return self.run(user=user)
        return {"module": "startup", "task": task, "status": "unknown"}
''',
    "workspace.py": r'''"""Holographic workspace - the interactive command surface."""

from __future__ import annotations

import importlib
from typing import Any, Dict, Optional

from core.arc_reactor import ArcReactor
from core.hologram_grid import HologramGrid
from core.telemetry_dashboard import TelemetryDashboard


class HolographicWorkspace:
    """Central brain that routes holographic commands to capability packages."""

    PACKAGES = [
        "holographic_display",
        "gesture_control",
        "spatial_computing",
        "interaction",
        "holographic_objects",
        "visualization",
        "scientific_visualization",
        "engineering",
        "telepresence",
        "hardware",
        "rendering",
        "security",
        "applications",
        "ai_bridge",
        "persistence",
        "safety",
    ]

    def __init__(self, ui=None):
        self.ui = ui
        self.reactor = ArcReactor(ui=None)
        self.reactor.online = True
        self.grid = HologramGrid(ui=None)
        self.dashboard = TelemetryDashboard(ui=ui)
        self.registry: Dict[str, Any] = {}
        self._load_packages()

    def _load_packages(self):
        for pkg in self.PACKAGES:
            try:
                mod = importlib.import_module(pkg)
                instances = mod.instantiate_all(config={})
                for name, inst in instances.items():
                    self.registry[f"{pkg}.{name}"] = inst
            except Exception as exc:
                if self.ui:
                    self.ui.warn(f"package {pkg} failed to load: {exc}")

    def help(self) -> dict:
        return {
            "commands": "help | status | list | scan | dashboard | arc | grid | <package.module> <task>",
            "packages": ", ".join(self.PACKAGES),
            "modules": len(self.registry),
        }

    def execute(self, command: str, context: Optional[Dict[str, Any]] = None) -> Any:
        cmd = command.strip()
        low = cmd.lower()

        # Built-ins.
        if low in ("help", "?"):
            return self.help()
        if low in ("status",):
            return {
                "reactor": self.reactor.status(),
                "grid": self.grid.status(),
                "modules_loaded": len(self.registry),
            }
        if low in ("list", "modules"):
            return {"modules": sorted(self.registry.keys())}
        if low in ("scan",):
            if self.ui:
                self.ui.progress("Scanning spatial environment", total=100, sleep=0.01)
            self.grid.raise_grid()
            return {"scan": "complete", "grid": self.grid.status()}
        if low in ("dashboard", "telemetry"):
            return self.dashboard.materialise()
        if low in ("arc", "reactor"):
            return self.reactor.status()
        if low in ("grid",):
            return self.grid.status()

        # Route "<package.module> <task>" or "<module> <task>".
        parts = cmd.split(maxsplit=1)
        target = parts[0]
        task = parts[1] if len(parts) > 1 else "execute"
        inst = self.registry.get(target)
        if inst is None:
            # try matching by suffix
            matches = [k for k in self.registry if k.endswith("." + target) or k.split(".")[-1] == target]
            if len(matches) == 1:
                inst = self.registry[matches[0]]
            elif matches:
                return {"ambiguity": matches}
        if inst is not None:
            try:
                result = inst.execute(task, context)
                self.dashboard.add_hologram(1)
                return result
            except Exception as exc:
                return {"error": str(exc), "module": target}

        return {
            "error": "unknown command",
            "command": cmd,
            "hint": "type 'help' for available commands, 'list' for modules",
        }

    def tick_safety(self):
        """Daemon safety tick - placeholder for safety package polling."""
        safety = self.registry.get("safety.emergency_shutdown")
        if safety is not None:
            try:
                safety.execute("tick")
            except Exception:
                pass
''',
}


# --------------------------------------------------------------------------- #
# Config files
# --------------------------------------------------------------------------- #

CONFIG_FILES: Dict[str, str] = {
    "settings.json": json.dumps(
        {
            "user": "Operator",
            "boot_sequence": True,
            "spatial_audio": True,
            "particle_effects": True,
            "transparent_panels": True,
            "arc_reactor_capacity_gj": 8.0,
        },
        indent=2,
    ),
    "hardware.json": json.dumps(
        {
            "depth_camera": {"type": "auto", "enabled": True, "range_m": 5.0},
            "projector": {"type": "auto", "brightness": 1.0, "refresh_hz": 60},
            "spatial_light_modulator": {"enabled": True, "cells": 4096},
            "safety_interlock": True,
            "thermal_limit_c": 75,
        },
        indent=2,
    ),
    "display.json": json.dumps(
        {
            "resolution": [3840, 2160],
            "parallax": "full",
            "lightfield": True,
            "volumetric": True,
            "target_fps": 60,
            "depth_layers": 32,
        },
        indent=2,
    ),
}


# --------------------------------------------------------------------------- #
# Builder
# --------------------------------------------------------------------------- #

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build():
    print(f"[generate] target root: {ROOT}")
    ROOT.mkdir(parents=True, exist_ok=True)

    # 1. capability packages
    module_count = 0
    for pkg, files in PACKAGES.items():
        pkg_dir = ROOT / pkg
        pkg_dir.mkdir(parents=True, exist_ok=True)
        names = sorted(files.keys())
        for fname, desc in files.items():
            write_file(pkg_dir / fname, module_source(pkg, fname, desc))
            module_count += 1
        write_file(pkg_dir / "__init__.py", package_init_source(pkg, names))
    print(f"[generate] wrote {module_count} capability modules across {len(PACKAGES)} packages")

    # 2. core engine
    for fname, src in CORE_FILES.items():
        write_file(ROOT / "core" / fname, src)
    print(f"[generate] wrote {len(CORE_FILES)} core engine files")

    # 3. top-level entry points
    write_file(ROOT / "main.py", MAIN_PY)
    write_file(ROOT / "ui.py", UI_PY)
    write_file(ROOT / "setup.py", SETUP_PY)
    print("[generate] wrote main.py, ui.py, setup.py")

    # 4. config
    cfg_dir = ROOT / "config"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    for name, data in CONFIG_FILES.items():
        write_file(cfg_dir / name, data + "\n")
    print(f"[generate] wrote {len(CONFIG_FILES)} config files")

    # 5. requirements
    write_file(ROOT / "requirements.txt", REQUIREMENTS_TXT)
    print("[generate] wrote requirements.txt")

    print(f"\n[generate] DONE. {module_count} modules, {len(PACKAGES)} packages, core engine + entry points.")
    print(f"[generate] Run:  cd {ROOT} && python main.py --no-daemons --skip-boot")


if __name__ == "__main__":
    build()
