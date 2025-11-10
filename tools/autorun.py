"""Simple autorun watcher that restarts main.py when Python files change.

Usage: run this in the project root virtualenv (where `python` points to your env):
    python tools/autorun.py

It requires the `watchdog` package (added to requirements.txt).
The script watches the current workspace recursively for .py changes and restarts
`python main.py` whenever a file is created/modified/deleted.
"""
import subprocess
import sys
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_SCRIPT = PROJECT_ROOT / "main.py"
PY_EXE = sys.executable


class RestartHandler(PatternMatchingEventHandler):
    def __init__(self, restart_callback):
        super().__init__(patterns=["*.py"], ignore_directories=True, case_sensitive=False)
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        # Debounce rapid consecutive events
        self.restart_callback()


class ProcessManager:
    def __init__(self):
        self.proc = None
        self._last_restart = 0

    def start(self):
        if not MAIN_SCRIPT.exists():
            print(f"Error: main script not found at {MAIN_SCRIPT}")
            return
        print(f"Starting {MAIN_SCRIPT} using {PY_EXE}")
        self.proc = subprocess.Popen([PY_EXE, str(MAIN_SCRIPT)])

    def stop(self):
        if self.proc and self.proc.poll() is None:
            print("Stopping process...")
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except Exception:
                self.proc.kill()
        self.proc = None

    def restart(self):
        # simple time-based debounce: do not restart more than once per 0.5s
        now = time.time()
        if now - self._last_restart < 0.5:
            return
        self._last_restart = now
        print("Restarting application due to file change...")
        self.stop()
        self.start()


def main():
    mgr = ProcessManager()
    mgr.start()

    observer = Observer()
    handler = RestartHandler(mgr.restart)
    observer.schedule(handler, path=str(PROJECT_ROOT), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
    finally:
        observer.stop()
        observer.join()
        mgr.stop()


if __name__ == "__main__":
    main()
