# KitaMap Berlin - Daycare Center Spatial Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GIS](https://img.shields.io/badge/GIS-GeoPandas-orange.svg)]()
[![Analysis](https://img.shields.io/badge/Analysis-Complete-brightgreen.svg)]()

> **Comprehensive spatial analysis of daycare center coverage in Berlin using GIS technology, including demographic forecasting until 2034**

**🌐 [View Interactive Dashboard](https://pinea.app.carto.com/map/81885962-c7a8-4639-8124-372e0caa6e60)**

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/KitaMap_Berlin.git
cd KitaMap_Berlin

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the complete analysis
python main.py

# 4. Explore Jupyter notebooks
jupyter notebook notebooks/
```

## Project Overview

KitaMap Berlin is a comprehensive data-driven project analyzing the spatial distribution and accessibility of daycare centers in Berlin. The project combines modern GIS technologies with advanced analytical methods to provide evidence-based insights for urban planning and policy decisions.

### Key Features

- **📊 Coverage Analysis**: District-level assessment of current daycare availability
- **🔮 Demographic Forecasting**: Population-based demand prediction until 2034
- **📍 Gap Identification**: Detection of underserved areas and hotspots
- **🚶‍♀️ Accessibility Analysis**: Walking-distance catchment area calculations  
- **🌱 Environmental Integration**: Proximity analysis to green spaces and water areas
- **📱 Interactive Visualization**: Web-based dashboard with CARTO integration

## Technology Stack

### 🐍 Core Technologies
- **Python 3.8+** - Primary programming language
- **GeoPandas** - Spatial data analysis and manipulation
- **Pandas & NumPy** - Data processing and numerical computations
- **Shapely** - Geometric operations and spatial calculations

### 🗺 GIS & Mapping
- **CARTO** - Interactive web-based visualization platform
- **OpenStreetMap** - Base map data and point-of-interest extraction
- **OpenRouteService API** - Isochrone and routing calculations
- **OSMium** - High-performance OSM data processing

### 📊 Analysis & Forecasting
- **Prophet** - Time series forecasting for demographic predictions
- **Statsmodels** - Statistical modeling and regression analysis
- **Scikit-learn** - Machine learning utilities
- **Matplotlib & Seaborn** - Statistical visualizations

### 💻 Development Environment
- **Jupyter Notebooks** - Interactive analysis and documentation
- **TQDM** - Progress bars for long-running operations
- **Python-dotenv** - Environment variable management

## Project Structure

```
KitaMap_Berlin/
├── 📄 README.md                  # Projektdokumentation  
├── 📄 LICENSE                    # MIT-Lizenz
├── 📄 pyproject.toml            # Python-Projekt-Konfiguration
├── 📄 requirements.txt           # Python-Abhängigkeiten
│
├── 📂 src/                      # Quellcode-Verzeichnis
│   ├── data_processing/         # Datenverarbeitung
│   │   ├── __init__.py
│   │   └── kita_data_processor.py
│   ├── analysis/                # Analysefunktionen  
│   │   ├── __init__.py
│   │   ├── catchment_area.py
│   │   └── green_water_area.py
│   └── utils/                   # Hilfsfunktionen
│       ├── __init__.py
│       └── geo_utils.py
│
├── 📊 notebooks/                # Jupyter Notebooks für explorative Analyse
│   ├── 01_data_preparation_kitas.ipynb
│   ├── 02_demographic_analysis.ipynb
│   ├── 03_data_preparation_bezirke.ipynb
│   └── README.md                # Notebook-Übersicht
│
├── 📁 data/                     # Datenverzeichnis
│   ├── raw/                     # Rohdaten (unverändert)
│   │   ├── berlin-latest.osm.pbf
│   │   ├── entwicklung_2015_2024.csv
│   │   └── kitas_osm.geojson
│   ├── processed/               # Verarbeitete Zwischendaten
│   │   ├── bezirke_processed.geojson
│   │   ├── kitas_processed.geojson
│   │   └── prognose_2024_2034.csv
│   ├── results/                 # Finale Analyseergebnisse
│   │   ├── isochrones.geojson
│   │   ├── berlin_green_areas.geojson
│   │   └── berlin_water_areas.geojson
│   └── external/                # Externe/Export-Daten (CARTO etc.)
│       ├── kita_versorgung_basis.geojson
│       ├── kita_versorgung_kategorie_2024.geojson
│       └── kita_versorgung_trend_2024_2034.geojson
│
├── 📖 docs/                     # Dokumentation
│   ├── index.md
│   ├── methodology.md           # Methodenbeschreibung
│   └── api_reference.md         # Code-Dokumentation
│
├── 🧪 tests/                    # Tests
│   ├── __init__.py
│   ├── test_catchment_area.py
│   └── test_data_processing.py
│
└── 🎨 assets/                   # Zusätzliche Ressourcen
    ├── images/                  # Screenshots, Diagramme
    └── config/                  # Konfigurationsdateien
        └── settings.yml
```

## Usage Examples

### Command Line Analysis
```bash
# Run complete spatial analysis
python main.py

# Extract only OSM areas (green spaces, water bodies)
python main.py --osm-only

# Generate isochrones only (requires API key)
python main.py --isochrones-only --api-key YOUR_ORS_KEY
```

### Jupyter Notebooks
The project includes three main analysis notebooks:

1. **`01_daycare_data_processing.ipynb`** - Data cleaning and capacity estimation
2. **`02_demographic_forecasting.ipynb`** - Population predictions using time series
3. **`03_district_analysis.ipynb`** - Spatial analysis and coverage assessment

### API Configuration
For catchment area analysis, set your OpenRouteService API key:
```bash
export OPENROUTESERVICE_API_KEY="your_api_key_here"
```

## Data Sources

| Source | Description | Usage |
|--------|-------------|-------|
| **OpenStreetMap** | Daycare locations and metadata | Geocoding, facility data extraction |
| **Berlin Geoportal** | Administrative boundaries | District boundaries, spatial references |
| **Berlin Statistics Office** | Demographic data | Population forecasts and trends |
| **OpenRouteService** | Routing and accessibility | Isochrone calculations, walking distances |

## Methodology

### 1. Data Collection & Processing
- Automated extraction of daycare locations from OpenStreetMap
- Capacity estimation using area-based regression and district-specific medians  
- Integration of demographic data at district level

### 2. Spatial Analysis
- **Catchment Areas**: 500m walking-distance isochrones around facilities
- **Accessibility Analysis**: Route-based calculations via OpenRouteService API
- **Coverage Assessment**: District-level availability metrics

### 3. Forecasting
- **Time Series Modeling**: Prophet-based population predictions until 2034
- **Demand Estimation**: Future daycare needs based on demographic trends
- **Gap Analysis**: Identification of supply-demand mismatches

### 4. Visualization
- **Interactive Dashboard**: CARTO-powered web visualization
- **Statistical Graphics**: Analysis reports with Matplotlib/Seaborn
- **Jupyter Integration**: Reproducible analysis workflows

## Key Results

### Current Coverage (2024)
- **Over-supplied Districts**: Charlottenburg-Wilmersdorf, Steglitz-Zehlendorf  
- **Under-supplied Districts**: Neukölln, Marzahn-Hellersdorf
- **Critical Areas**: 15 identified hotspots with significant coverage gaps

### 2034 Forecast
- **Population Growth**: +8.5% in target age groups (0-6 years)
- **Additional Demand**: ~2,500 new daycare spots required
- **Priority Areas**: 8 districts requiring urgent intervention

## Applications

- **Urban Planning**: Evidence-based location planning for new facilities
- **Policy Making**: Data-driven resource allocation decisions  
- **Research**: Methodological framework for similar urban analyses
- **Public Transparency**: Clear visualization of service coverage

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/SilasPignotti/KitaMap_Berlin.git
cd KitaMap_Berlin

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run analysis
python main.py
```

## Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Silas Pignotti**
- GitHub: [@SilasPignotti](https://github.com/SilasPignotti)
- Project: [KitaMap Berlin](https://github.com/SilasPignotti/KitaMap_Berlin)

## Acknowledgments

- **OpenStreetMap Community** for comprehensive geospatial data
- **Berlin Geoportal** for administrative boundaries
- **Berlin Statistics Office** for demographic data
- **CARTO** for visualization platform
- **OpenRouteService** for routing and accessibility APIs

---
