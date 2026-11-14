"""
Pytest configuration file to ensure the project root is in sys.path during test collection
and persistent cache for matplotlib to eliminate font scan overhead.
"""

import os
import sys

# Add project root directory to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure writable matplotlib cache directory
mpl_cache = os.path.join(PROJECT_ROOT, ".matplotlib_cache")
os.makedirs(mpl_cache, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_cache
