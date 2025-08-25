#!/usr/bin/env python3
"""
KitaMap Berlin - Main Entry Point

Berlin Daycare Center Spatial Analysis and Coverage Assessment.

This is the main entry point for the KitaMap Berlin project, which analyzes
daycare center distribution, coverage, and accessibility in Berlin.

Usage:
    python main.py                    # Run complete analysis
    python main.py --help            # Show help options
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

if __name__ == "__main__":
    # Import and run the analysis CLI
    import run_analysis
    run_analysis.main()