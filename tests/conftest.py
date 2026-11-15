"""
Pytest configuration file to ensure the project root is in sys.path during test collection
and persistent cache for matplotlib to eliminate font scan overhead.
"""

import os
import sys

# Prevent OpenMP runtime conflict on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Add project root directory to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Preload sklearn to initialize OpenMP before subtests
try:
    import sklearn
except Exception:
    pass

# Configure writable matplotlib cache directory
mpl_cache = os.path.join(PROJECT_ROOT, ".matplotlib_cache")
os.makedirs(mpl_cache, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_cache
