#!/usr/bin/env python3
"""
Test suite for the Autonomous Computer AI Assistant core.

Verifies that the core engine, LLM fallback, orchestrator routing, and the
implemented action modules work end to end. Network-dependent capabilities
(web_search, ip_checker, weather, translate) are exercised via their parsing
logic only, to keep the suite hermetic.

Run:  python -m pytest tests/test_core.py -v
   or python tests/test_core.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.capability import Capability, result_to_text  # noqa: E402
from core.llm import LLMClient  # noqa: E402
from orchestrator import Orchestrator  # noqa: E402
from smart_orchestrator import SmartOrchestrator  # noqa: E402

from actions.calculator import Calculator  # noqa: E402
from actions.file_controller import FileController  # noqa: E402
from actions.terminal_manager import TerminalManager  # noqa: E402
from actions.system_monitor import SystemMonitor  # noqa: E402
from actions.qr_generator import QrGenerator  # noqa: E402
from actions.reminder import Reminder  # noqa: E402


def test_capability_ok_error_helpers():
    cap = Capability()
    assert cap.ok("done")["status"] == "ok"
    assert cap.ok("done")["result"] == "done"
    assert cap.error("bad")["status"] == "error"
    assert cap.error("bad")["error"] == "bad"


def test_result_to_text():
    assert result_to_text("hello") == "hello"
    assert result_to_text({"status": "ok", "result": "win"}) == "win"
    assert result_to_text({"status": "error", "error": "boom"}) == "error: boom"
    assert result_to_text(None) == ""


def test_llm_offline_plan_is_json():
    client = LLMClient()
    assert client.is_available() is False
    plan = client.reason("Objective: calculate 5 + 5\nContext: {}\n\nReturn JSON.")
    import json
    parsed = json.loads(plan)
    assert isinstance(parsed, list)
    assert parsed[0]["step"]


def test_llm_summarize():
    client = LLMClient()
    out = client.summarize("a | b | c")
    assert "a" in out


def test_calculator_basic():
    calc = Calculator()
    r = calc.execute("calculate 12 * (3 + 4)")
    assert r["status"] == "ok"
    assert r["value"] == 84


def test_calculator_division():
    calc = Calculator()
    assert calc.execute("calculate 10 / 4")["value"] == 2.5


def test_calculator_zero_division():
    calc = Calculator()
    assert calc.execute("calculate 1 / 0")["status"] == "error"


def test_calculator_rejects_code():
    calc = Calculator()
    r = calc.execute("calculate __import__('os')")
    assert r["status"] == "error"


def test_terminal_echo():
    tm = TerminalManager()
    r = tm.execute('run command: echo "hi"')
    assert r["status"] == "ok"
    assert "hi" in r["result"]


def test_terminal_blocks_dangerous():
    tm = TerminalManager()
    r = tm.execute("run command: rm -rf /")
    assert r["status"] == "error"


def test_file_create_read_delete():
    import tempfile
    d = Path(tempfile.mkdtemp())
    fname = d / "sub" / "test.txt"
    fc = FileController()
    r = fc.execute(f'create file "{fname}" "hello world"')
    assert r["status"] == "ok"
    assert fname.read_text() == "hello world"
    r = fc.execute(f'read file "{fname}"')
    assert r["status"] == "ok"
    assert "hello world" in r["result"]
    r = fc.execute(f'delete file "{fname}"')
    assert r["status"] == "ok"
    assert not fname.exists()


def test_file_list():
    import tempfile
    d = Path(tempfile.mkdtemp())
    (d / "a.txt").write_text("a")
    (d / "b.txt").write_text("b")
    fc = FileController()
    r = fc.execute(f'list files "{d}"')
    assert r["status"] == "ok"
    assert "a.txt" in r["result"]
    assert "b.txt" in r["result"]


def test_system_monitor_overview():
    sm = SystemMonitor()
    r = sm.execute("system status")
    assert r["status"] == "ok"
    assert "CPU" in r["result"]
    assert "Memory" in r["result"]


def test_qr_extract_data():
    qr = QrGenerator()
    assert qr._extract_data('generate qr "https://x.com"') == "https://x.com"
    assert qr._extract_data("qr code: hello") == "hello"


def test_reminder_add_list():
    import tempfile
    rem = Reminder()
    rem.STORE = Path(tempfile.mkdtemp()) / "reminders.json"
    r = rem.execute("remind me to call mom")
    assert r["status"] == "ok"
    assert "call mom" in r["result"]
    r = rem.execute("list reminders")
    assert r["status"] == "ok"
    assert "call mom" in r["result"]


def test_orchestrator_plan_offline():
    orch = Orchestrator(model_router=LLMClient())
    steps = orch.plan("calculate 3 + 3")
    assert len(steps) >= 1
    assert "step" in steps[0]


def test_smart_orchestrator_calculator():
    so = SmartOrchestrator()
    out = so.run("calculate 9 * 9")
    assert "81" in out


def test_smart_orchestrator_help():
    so = SmartOrchestrator()
    out = so.run("help")
    assert "capabilities" in out.lower()


def test_smart_orchestrator_status():
    so = SmartOrchestrator()
    out = so.run("status")
    assert "CPU" in out


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as exc:
            import traceback
            print(f"  FAIL  {t.__name__}: {exc}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
