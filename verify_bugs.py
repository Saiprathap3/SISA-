import os
import runpy
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
runpy.run_path("backend/verify_bugs.py", run_name="__main__")
