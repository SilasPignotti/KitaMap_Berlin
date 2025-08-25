# Jupyter Notebooks - KitaMap Berlin

This directory contains Jupyter notebooks for exploratory data analysis and methodology documentation.

## Notebook Overview

### 01_daycare_data_processing.ipynb
**Main Goal**: Processing and capacity estimation for daycare data from OpenStreetMap

**Core Tasks**:
- Data integration of OSM daycare data and Berlin district boundaries
- Capacity estimation for missing values using:
  - Area-based regression for polygon geometries
  - District-specific median estimation for point geometries
- Data validation and scaling to target capacity
- Export of final dataset

**Output**: `../data/processed/daycare_centers_processed.geojson`

### 02_demographic_forecasting.ipynb
**Main Goal**: Demographic analysis and demand forecasting

**Core Tasks**:
- Analysis of population development by districts
- Time series modeling with Prophet and Exponential Smoothing
- Forecast of daycare demand until 2034
- Identification of coverage gaps

**Output**: `../data/processed/population_forecast_2024_2034.csv`

### 03_district_analysis.ipynb
**Main Goal**: District data preparation and spatial analysis

**Core Tasks**:
- Geometric preparation of district boundaries
- Spatial aggregation of daycare data by districts
- Calculation of coverage metrics
- Preparation for CARTO visualization

**Output**: Multiple files in `../data/external/` for visualization

## Usage

The notebooks should be used in the specified order, as later notebooks build upon the outputs of earlier ones.

### Prerequisites
```bash
# Install dependencies
pip install -r ../requirements.txt

# Start Jupyter
jupyter notebook
```

### Data Structure
After project restructuring, paths are organized as follows:
- Raw data: `../data/raw/`
- Processed data: `../data/processed/`
- Analysis results: `../data/results/`
- External exports: `../data/external/`