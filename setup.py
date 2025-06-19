"""
Setup-Konfiguration für KitaMap Berlin.

Dieses Setup-Skript ermöglicht die Installation des KitaMap Berlin Projekts
als Python-Paket mit allen notwendigen Abhängigkeiten.

Author: Silas Pignotti
Date: 2024
"""

from setuptools import setup, find_packages

# Lese README für die lange Beschreibung
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lese Requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kitamap-berlin",
    version="1.0.0",
    author="Silas Pignotti",
    author_email="silas.pignotti@example.com",
    description="GIS-basierte Analyse der Kindertagesstätten-Versorgung in Berlin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SilasPignotti/KitaMap_Berlin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kitamap=kitamap.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.geojson", "*.json", "*.csv"],
    },
    keywords="gis, geospatial, berlin, kindergartens, analysis, carto, openstreetmap",
    project_urls={
        "Bug Reports": "https://github.com/SilasPignotti/KitaMap_Berlin/issues",
        "Source": "https://github.com/SilasPignotti/KitaMap_Berlin",
        "Documentation": "https://github.com/SilasPignotti/KitaMap_Berlin#readme",
    },
) 